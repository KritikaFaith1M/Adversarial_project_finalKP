import json
import os
from web3 import Web3

# CONNECT GANACHE
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    raise Exception("❌ Start Ganache first")

print("✅ Connected to Ganache")

# LOAD CONTRACT
with open("blockchain/contract_info.json", "r") as f:
    contract_info = json.load(f)

contract = w3.eth.contract(
    address=contract_info["address"],
    abi=contract_info["abi"]
)

account = w3.eth.accounts[0]

# LOAD LOGS
log_folder = "audit_logs"
files = [f for f in os.listdir(log_folder) if f.endswith(".json")]

print(f"📂 Found {len(files)} logs")

# STORE
for file in files:
    with open(os.path.join(log_folder, file), "r") as f:
        log = json.load(f)

    cid = log["content_hash"]

    print("📡 Storing:", cid)

    try:
        tx_hash = contract.functions.storeHash(cid).transact({
            "from": account
        })

        w3.eth.wait_for_transaction_receipt(tx_hash)

        print("✅ Stored")

    except Exception as e:
        print("❌ Error:", e)

# FINAL COUNT
count = contract.functions.getAuditCount().call()
print("📊 Total Stored:", count)