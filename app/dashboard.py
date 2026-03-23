import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
from PIL import Image
from pathlib import Path

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Adversarial Attack Detection using Blockchain Audit",
    layout="wide",
    page_icon="🛡️"
)

# -------------------------
# Background & CSS Styling
# -------------------------
bg_path = r"C:\Users\kriti\Desktop\adversarial-project - Copy\bgimage2.png"
if os.path.exists(bg_path):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("file://{bg_path}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .overlay {{
            background-color: rgba(0,0,0,0.55);
            padding: 20px;
            border-radius: 15px;
        }}
        .main {{ font-family: 'Segoe UI', sans-serif; color: #ffffff; }}
        [data-testid="stSidebar"] {{ background-color: #161b22; color: #ffffff; padding-top: 2rem; }}
        [data-testid="stSidebar"] h2 {{ font-size: 1.8rem; font-weight: 700; }}
        [data-testid="stSidebar"] .css-1d391kg {{ font-size: 1rem; font-weight: 500; color: #ffd700; }}
        .card {{ background-color: rgba(30,33,48,0.85); padding: 15px; border-radius: 12px; border: 1px solid #31333f; margin-bottom: 15px; }}
        .card h3 {{ color: #ffd700; font-size: 1.2rem; margin-bottom: 5px; }}
        .card p {{ color: #ffffff; font-size: 1rem; }}
        .stButton>button {{ background-color: #00ff41; color: #0e1117; font-weight: bold; font-size: 1.1rem; border-radius: 10px; padding: 0.5rem 1rem; margin-top: 10px; }}
        h1 {{ font-size: 3rem; font-weight: 700; color: #ffd700; text-align: center; }}
        h2 {{ font-size: 1.8rem; font-weight: 600; color: #ffffff; }}
        h3 {{ font-size: 1.2rem; color: #ffffff; }}
        .status-success {{ color: #00ff41; font-weight: bold; font-size: 1.2rem; }}
        .status-fail {{ color: #ff4b4b; font-weight: bold; font-size: 1.2rem; }}
        .alert-danger {{ background-color:#ff4b4b; color:white; padding:10px; border-radius:10px; font-weight:bold; font-size:1.2rem; text-align:center; }}
        div[data-testid="stExpander"] {{ border: 1px solid #31333f; border-radius: 10px; background-color: #161b22; margin-bottom: 10px; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# Helper Functions
# -------------------------
def cols(n):
    return st.columns(n)

def load_image(path, max_size=(300,300)):
    if path and os.path.exists(path):
        img = Image.open(path)
        img.thumbnail(max_size)
        return img
    return None

def get_image_path(folder, prefix, idx):
    path = os.path.join(folder, f"{prefix}_{idx}.png")
    return path if os.path.exists(path) else None

@st.cache_data
def load_logs_cached(log_folder, image_folder):
    logs = []
    for file in os.listdir(log_folder):
        if file.endswith(".json"):
            try:
                with open(os.path.join(log_folder, file), "r") as f:
                    log = json.load(f)
                    logs.append(log)
            except:
                pass
    return sorted(logs, key=lambda x: x.get('image_index', 0)) if logs else []

def check_cid_in_logs(file_cid, logs):
    for log in logs:
        if log.get("content_hash") == file_cid:
            return log
    return None

# -------------------------
# Load Logs
# -------------------------
log_folder = "audit_logs"
image_folder = "attacks/saved_images"
Path(log_folder).mkdir(exist_ok=True)
logs_data = load_logs_cached(log_folder, image_folder)

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.title("Audit Center")
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Home", "📊 Dashboard", "📜 Logs"], index=0, label_visibility="collapsed")
    st.markdown("---")
    if logs_data:
        st.success(f"System Online: {len(logs_data)} Logs")
    else:
        st.warning("System Offline: No Logs Found")
    st.caption("Adversarial Audit System v4.0")

# -------------------------
# Home Page
# -------------------------
if page == "🏠 Home":
    st.markdown('<div class="overlay">', unsafe_allow_html=True)
    st.markdown("<h1>🛡️ Adversarial Attack Detection using Blockchain Audit</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>🔍 Model Audited</h3>
            <p>ResNet-18 trained on CIFAR-10 dataset</p>
        </div>
        <div class='card'>
            <h3>⚡ Attack Vector</h3>
            <p>Fast Gradient Sign Method (FGSM)</p>
        </div>
        <div class='card'>
            <h3>🔐 Integrity Proof</h3>
            <p>Adversarial images stored on IPFS, CID linked to blockchain</p>
        </div>
        <div class='card'>
            <h3>🛠️ Instructions</h3>
            <p>1. Generate attack logs in /audit_logs folder</p>
            <p>2. Explore metrics & comparisons in Dashboard</p>
            <p>3. Export logs from Logs page</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Dashboard Page
# -------------------------
elif page == "📊 Dashboard":
    st.markdown('<div class="overlay">', unsafe_allow_html=True)
    st.title("📊 Adversarial Dashboard")
    
    # Upload & Verify via CID
    st.subheader("📤 Upload & Verify Image via CID")
    uploaded_file = st.file_uploader("Upload an image to verify")
    if uploaded_file:
        from ipfshttpclient import Client
        try:
            client = Client()
            cid_res = client.add_bytes(uploaded_file.read())
            uploaded_file.seek(0)
            file_cid = cid_res
            st.write(f"🖋 CID of uploaded file: `{file_cid}`")
            matched_log = check_cid_in_logs(file_cid, logs_data)
            if matched_log:
                st.markdown(f"<div class='alert-danger'>⚠️ ALERT! This file matches Audit #{matched_log.get('image_index')}: {matched_log.get('original_label')} ➔ {matched_log.get('adversarial_label')}</div>", unsafe_allow_html=True)
            else:
                st.success("✅ SAFE: File CID not found in previous audits")
        except Exception as e:
            st.error(f"❌ IPFS Error: {e}")
    
    st.divider()
    
    total_logs = len(logs_data)
    success_count = sum(1 for log in logs_data if log.get("status")=="SUCCESS")
    success_rate = (success_count/total_logs*100) if total_logs>0 else 0

    m1, m2, m3 = cols(3)
    m1.metric("📄 Total Audits", total_logs)
    m2.metric("⚠️ Successful Flips", success_count)
    m3.metric("🎯 Success Rate", f"{success_rate:.1f}%")
    
    st.divider()
    
    # Charts & Filters
    col_chart, col_filter = st.columns([3,1])
    with col_chart:
        if logs_data:
            df = pd.DataFrame(logs_data)
            fig = px.pie(df, names='status', hole=0.5, 
                         color='status', color_discrete_map={'SUCCESS':'#00ff41', 'FAILED':'#ff4b4b'})
            fig.update_layout(
                margin=dict(t=10,b=10,l=10,r=10), 
                showlegend=True, 
                paper_bgcolor='rgba(0,0,0,0)', 
                font_color="white"
            )
            st.plotly_chart(fig, use_container_width=True)
    with col_filter:
        st.markdown("### 🔎 Filter Reports")
        search_query = st.text_input("Search by Original Label", placeholder="e.g., dog, car")
    
    st.divider()
    
    # Attack Gallery
    st.subheader("🖼️ Attack Forensic Gallery")
    filtered_logs = [l for l in logs_data if search_query.lower() in str(l.get("original_label","")).lower()] if search_query else logs_data
    logs_per_page = 10
    total_pages = (len(filtered_logs)-1)//logs_per_page + 1 if filtered_logs else 1
    page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page_number-1)*logs_per_page
    end_idx = start_idx + logs_per_page
    for log in filtered_logs[start_idx:end_idx]:
        idx = log.get("image_index")
        status = log.get("status")
        orig_img = load_image(get_image_path(image_folder, "original", idx))
        adv_img = load_image(get_image_path(image_folder, "adv", idx))
        exp_label = f"Audit #{idx} | {log.get('original_label')} ➔ {log.get('adversarial_label')} [{status}]"
        
        with st.expander(exp_label):
            c1, c2 = cols(2)
            with c1:
                st.markdown("**Side-by-Side**")
                i1, i2 = cols(2)
                with i1:
                    if orig_img: st.image(orig_img, caption="Original")
                    else: st.error("Original Image Missing")
                with i2:
                    if adv_img: st.image(adv_img, caption="Adversarial")
                    else: st.error("Adversarial Image Missing")
            
            with c2:
                st.markdown("**Attack Details**")
                st.write(f"Before Confidence: {log.get('confidence_before',0):.2%}")
                st.write(f"After Confidence: {log.get('confidence_after',0):.2%}")
                color_class = "status-success" if status=="SUCCESS" else "status-fail"
                st.markdown(f"**Result:** <span class='{color_class}'>{status}</span>", unsafe_allow_html=True)
                st.markdown("**🔐 Forensic Chain (CID)**")
                st.code(f"{log.get('content_hash')}")
                if log.get("ipfs_url") and log.get("content_hash") != "INVALID":
                    st.markdown(f"[🌐 Open IPFS Proof]({log.get('ipfs_url')})")
                else:
                    st.caption("IPFS link unavailable")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Logs Page
# -------------------------
elif page == "📜 Logs":
    st.markdown('<div class="overlay">', unsafe_allow_html=True)
    st.title("📜 Full Audit Trail")
    if logs_data:
        df_logs = pd.DataFrame(logs_data)
        display_cols = ["image_index","original_label","adversarial_label","status","confidence_before","confidence_after","content_hash"]
        st.dataframe(df_logs[display_cols], use_container_width=True)
        csv_data = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Audit Report (CSV)", csv_data, file_name="adversarial_audit_report.csv", mime="text/csv")
    else:
        st.warning("No logs to display.")
    st.markdown('</div>', unsafe_allow_html=True)