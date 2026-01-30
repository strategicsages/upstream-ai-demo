import streamlit as st
import pandas as pd

# ---- GLOBAL SESSION STATE ----
if "suppliers_df" not in st.session_state:
    st.session_state.suppliers_df = None

if "processed_data" not in st.session_state:
    st.session_state.processed_data = []

st.set_page_config(
    page_title="Upstream AI",
    page_icon="🌍",
    layout="wide"
)

# ------------------ SIDEBAR UTILITIES ------------------
with st.sidebar:
    st.header("🛠️ Utilities")
    
    # System Status
    st.success("System Status: ● Online")
    
    st.markdown("---")
    
    # Quick Settings / Toggles
    st.subheader("Preferences")
    enable_notifications = st.checkbox("Enable Alerts", value=True)
    auto_refresh = st.checkbox("Auto-refresh Dashboard", value=False)
    
    st.markdown("---")
    
    # Documentation / Help
    st.markdown("### 📚 Resources")
    st.markdown(
        """
        - [User Guide](https://streamlit.io)
        - [Compliance Standards (GHG)](https://ghgprotocol.org)
        - [Contact Support](mailto:support@upstream.ai)
        """
    )
    
    st.divider()
    st.caption("Upstream AI v1.0.2")

# ------------------ HEADER ------------------
col_logo, col_title = st.columns([1, 12])

with col_logo:
    st.markdown("## 🌍") 

with col_title:
    st.title("Upstream AI")
    st.caption("The Operating System for Scope 3 Decarbonization")

# ------------------ VALUE PROP (Hero Section) ------------------
st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("📥 Ingest")
    st.info("**Universal Adapter**\n\nUpload messy PDFs, Excel, or images. We extract audit-ready data instantly.")

with c2:
    st.subheader("🧠 Intelligence")
    st.warning("**Risk Engine**\n\nAuto-detect anomalies, validate against benchmarks, and score supplier maturity.")

with c3:
    st.subheader("📈 Impact")
    st.success("**Decarbonize**\n\nTrack tCO2e reductions and automate regulatory reporting (SB 253/CSRD).")

st.markdown("---")

# ------------------ DYNAMIC DASHBOARD / QUICK ACTIONS ------------------

# Check if we have data to show a summary
has_data = st.session_state.suppliers_df is not None or len(st.session_state.processed_data) > 0

if has_data:
    st.subheader("⚡ Quick Actions")
else:
    st.subheader("🚀 Get Started")

# Action Grid using Containers for "Card" look
ac1, ac2, ac3, ac4 = st.columns(4)

with ac1:
    with st.container(border=True):
        st.markdown("#### 📤 Upload")
        st.caption("Process new invoices")
        st.page_link("pages/2_Upload_Invoice.py", label="Go to Upload", icon="📄", use_container_width=True)

with ac2:
    with st.container(border=True):
        st.markdown("#### 📊 Insights")
        st.caption("View network health")
        st.page_link("pages/1_Dashboard.py", label="Open Dashboard", icon="📈", use_container_width=True)

with ac3:
    with st.container(border=True):
        st.markdown("#### 🏭 Network")
        st.caption("Manage Suppliers")
        st.page_link("pages/3_Suppliers.py", label="View Suppliers", icon="🏢", use_container_width=True)

with ac4:
    with st.container(border=True):
        st.markdown("#### 🧠 Agent")
        st.caption("Run Intelligence")
        st.page_link("pages/4_Supplier_Intelligence.py", label="Run Analysis", icon="🤖", use_container_width=True)

# ------------------ RECENT ACTIVITY / NEXT STEPS ------------------
st.markdown("###") # Spacer

if has_data:
    st.subheader("🕒 Recent Activity")
    # Show mini feed based on session state data
    if len(st.session_state.processed_data) > 0:
        latest = st.session_state.processed_data[-1]
        mapped_name = latest.get('mapped_supplier', 'Unknown Supplier')
        conf = latest.get('confidence_score', 0)
        st.info(f"🆕 **Processed Invoice:** {mapped_name} (Confidence: {conf}%)")
        
        if len(st.session_state.processed_data) > 1:
            prev = st.session_state.processed_data[-2]
            prev_name = prev.get('mapped_supplier', 'Unknown Supplier')
            st.caption(f"Previously: {prev_name}")
            
    elif st.session_state.suppliers_df is not None:
        count = len(st.session_state.suppliers_df)
        st.info(f"✅ **Network Status:** {count} suppliers actively tracked.")
    else:
        st.info("System initialized. Ready for data.")
else:
    st.subheader("🧭 Guided Onboarding")
    st.info(
        "**Step 1:** Navigate to **Upload Invoice** to ingest your first supplier document.\n\n"
        "**Step 2:** The **Ingestion hub** will extract the data and map it to a supplier.\n\n"
        "**Step 3:** View the **Dashboard** to see your Scope 3 supplychain submissions and performance."
    )
