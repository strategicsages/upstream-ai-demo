import streamlit as st

st.set_page_config(
    page_title="Upstream AI",
    page_icon="🌍",
    layout="wide"
)

# ---- LANDING PAGE ONLY ----
st.title("🌍 Upstream AI")
st.caption("Scope 3 Intelligence Platform")

st.markdown(
    """
### 👋 Welcome

Upstream AI is your **command center** for supplier data ingestion, validation,
and Scope 3 emissions intelligence.

**What you can do here:**
- 📤 Convert messy supplier invoices into structured JSON
- 🏭 Track supplier data quality & reliability
- 🧠 Generate audit-ready intelligence for ESG & ERP systems

👉 Use the **left navigation** to explore the platform.
"""
)

st.info(
    "Start with **Dashboard** to view live supplier health and data confidence.",
    icon="📊"
)
