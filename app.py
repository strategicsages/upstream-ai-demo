import streamlit as st

st.set_page_config(
    page_title="Upstream AI",
    page_icon="🌍",
    layout="wide"
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🌍 Upstream AI")
    st.caption("Scope 3 Intelligence Platform")

    st.markdown("---")

    st.page_link("1_Dashboard.py", label="📊 Dashboard")
    st.page_link("2_Upload_Invoice.py", label="📤 Upload Invoice")
    st.page_link("3_Suppliers.py", label="🏭 Suppliers")
    st.page_link("4_Supplier_Intelligence.py", label="🧠 Supplier Intelligence")

    st.markdown("---")
    st.caption("Utilities")

    st.page_link("Settings.py", label="⚙️ Settings")
    st.page_link("Profile.py", label="👤 Profile")
    st.page_link("Audit_Logs.py", label="📜 Audit Logs")

# ---------- LANDING ----------
st.markdown(
    """
    ### 👋 Welcome to Upstream AI  
    Your command center for supplier data ingestion, validation, and Scope 3 intelligence.

    👉 Start with **Dashboard** to see live supplier health.
    """
)
