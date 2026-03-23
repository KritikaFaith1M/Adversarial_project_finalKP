import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torchvision import models
from torchvision.utils import save_image
import os
import json
import time
import ipfshttpclient
from pathlib import Path
import hashlib

# -------------------------------
# 1️⃣ CONFIGURATION
# -------------------------------
device = torch.device("cpu")
epsilon = 0.1
num_images = 500
max_attempts = 2000

classes = ('plane','car','bird','cat','deer','dog','frog','horse','ship','truck')

# Directories
Path("attacks/saved_images").mkdir(parents=True, exist_ok=True)
Path("audit_logs").mkdir(parents=True, exist_ok=True)

# -------------------------------
# 2️⃣ CONNECT TO IPFS
# -------------------------------
try:
    client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")
    print("✅ Connected to IPFS")
except Exception as e:
    print("❌ IPFS not connected. Proceeding without upload.", e)
    client = None

# -------------------------------
# 3️⃣ HELPER FUNCTIONS
# -------------------------------
mean = torch.tensor([0.5,0.5,0.5]).view(3,1,1)
std = torch.tensor([0.5,0.5,0.5]).view(3,1,1)

def normalize(img): return (img-mean)/std
def denormalize(img): return img*std + mean

def compute_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def upload_to_ipfs(file_path):
    if client:
        try:
            res = client.add(file_path, pin=True)
            return res["Hash"], f"https://ipfs.io/ipfs/{res['Hash']}"
        except Exception as e:
            print(f"❌ IPFS upload failed for {file_path}: {e}")
            return "IPFS_FAILED", None
    return "IPFS_NOT_AVAILABLE", None

def fgsm_attack(image, epsilon, grad):
    perturbed = denormalize(image) + epsilon * grad.sign()
    perturbed = torch.clamp(perturbed,0,1)
    return normalize(perturbed)

# -------------------------------
# 4️⃣ LOAD MODEL
# -------------------------------
model = models.resnet18(weights=None)
model.conv1 = nn.Conv2d(3,64,kernel_size=3,stride=1,padding=1,bias=False)
model.maxpool = nn.Identity()
model.fc = nn.Linear(model.fc.in_features, 10)

try:
    model.load_state_dict(torch.load("models/saved/cifar_model.pth", map_location=device, weights_only=True))
    model.to(device)
    model.eval()
    print("✅ Model loaded successfully")
except FileNotFoundError:
    print("❌ Model not found at 'models/saved/cifar_model.pth'")
    exit()

# -------------------------------
# 5️⃣ DATA LOADER
# -------------------------------
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])

testset = torchvision.datasets.CIFAR10(root="./dataset", train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=True)

# -------------------------------
# 6️⃣ ATTACK LOOP
# -------------------------------
count = 0
success = 0
attempts = 0

print(f"🚀 Starting FGSM attack on {num_images} images...")

for image, label in testloader:
    attempts += 1
    if attempts > max_attempts: break
    if count >= num_images: break

    image, label = image.to(device), label.to(device)
    image.requires_grad = True

    output = model(image)
    _, pre_pred = torch.max(output,1)
    if pre_pred.item() != label.item(): continue  # skip wrong predictions

    # Compute gradients
    loss = F.cross_entropy(output,label)
    model.zero_grad()
    loss.backward()

    # Perturb
    perturbed = fgsm_attack(image, epsilon, image.grad.data)

    # Predict adversarial
    output_adv = model(perturbed)
    _, post_pred = torch.max(output_adv,1)

    # Paths
    orig_path = f"attacks/saved_images/original_{count+1}.png"
    adv_path = f"attacks/saved_images/adv_{count+1}.png"

    save_image(denormalize(image), orig_path)
    save_image(denormalize(perturbed), adv_path)

    # Compute hash & check existing log
    file_hash = compute_hash(adv_path)
    log_path = f"audit_logs/log_{count+1}.json"
    if Path(log_path).exists():
        print(f"⚠️ Log {log_path} exists. Skipping duplicate.")
        count += 1
        continue

    # Upload to IPFS
    ipfs_cid, ipfs_url = upload_to_ipfs(adv_path)

    # Stats
    conf_before = torch.max(F.softmax(output,dim=1)).item()
    conf_after = torch.max(F.softmax(output_adv,dim=1)).item()
    is_success = pre_pred.item() != post_pred.item()
    status = "SUCCESS" if is_success else "FAILED"

    # Log
    log_data = {
        "timestamp": time.ctime(),
        "image_index": count+1,
        "attack_method": "FGSM",
        "epsilon": epsilon,
        "original_label": classes[pre_pred.item()],
        "adversarial_label": classes[post_pred.item()],
        "confidence_before": conf_before,
        "confidence_after": conf_after,
        "status": status,
        "content_hash": ipfs_cid if ipfs_cid.startswith(("Qm","bafy")) else "INVALID",
        "ipfs_url": ipfs_url,
        "storage": "IPFS" if ipfs_cid.startswith(("Qm","bafy")) else "LOCAL"
    }

    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=4)

    if is_success: success += 1
    count += 1

    if count % 50 == 0:
        print(f"📊 Progress: {count}/{num_images} | Success Rate: {100*success/count:.2f}%")

# -------------------------------
# 7️⃣ FINAL SUMMARY
# -------------------------------
print("\n" + "="*30)
print(f"✅ Processing Complete")
print(f"🖼️ Images Processed: {count}")
print(f"🎯 Successful Attacks: {success}")
print(f"📈 Overall Success Rate: {100*success/count:.2f}%")
print(f"📂 Audit Trail saved in 'audit_logs/'")
print("="*30)