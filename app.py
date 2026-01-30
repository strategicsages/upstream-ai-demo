import streamlit as st
import pandas as pd

# ---- GLOBAL SESSION STATE ----
if "suppliers_df" not in st.session_state:
    st.session_state.suppliers_df = None

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "invoices" not in st.session_state:
    st.session_state.invoices = []


st.set_page_config(
    page_title="Upstream AI",
    page_icon="🌍",
    layout="wide"
)

# ------------------ HEADER ------------------
st.title("🌍 Upstream AI")
st.caption("Scope 3 Intelligence Platform")

st.markdown(
    """
Upstream AI helps companies **ingest, validate, and operationalize**
supplier-provided data for Scope 3 emissions reporting.

This is your **control plane** for supplier data quality and intelligence.
"""
)

st.divider()

# ------------------ QUICK ACTIONS ------------------
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/1_Dashboard.py", label="📊 View Dashboard", use_container_width=True)
    st.page_link("pages/2_Upload_Invoice.py", label="📤 Upload Supplier Document", use_container_width=True)

with col2:
    st.page_link("pages/3_Suppliers.py", label="🏭 Manage Suppliers", use_container_width=True)
    st.page_link("pages/4_Supplier_Intelligence.py", label="🧠 Supplier Intelligence", use_container_width=True)

with col3:
    st.button("👤 Profile", disabled=True)
    st.button("⚙️ Settings", disabled=True)
    st.button("🧾 Audit Logs", disabled=True)

st.caption("Profile, Settings, and Audit Logs are coming soon.")

st.divider()

# ------------------ GUIDED NEXT STEP ------------------
st.subheader("🧭 Suggested Next Step")

st.info(
    "Start by uploading a **supplier invoice or document** to see how Upstream AI "
    "extracts structured, audit-ready data in real time.",
    icon="👉"
)
