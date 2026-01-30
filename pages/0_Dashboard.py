import streamlit as st
import pandas as pd
import random

st.set_page_config(layout="wide")

st.title("📊 Dashboard")

st.caption("Live operational view of supplier data ingestion and quality")

# ---------------- MOCK METRICS (derived logic) ----------------
TOTAL_SUPPLIERS = 60
TOTAL_INVOICES = random.randint(1200, 2400)
AVG_CONFIDENCE = random.randint(82, 91)
AT_RISK = random.randint(6, 14)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Suppliers Tracked", TOTAL_SUPPLIERS)
c2.metric("Invoices Processed", TOTAL_INVOICES)
c3.metric("Avg AI Confidence", f"{AVG_CONFIDENCE}%")
c4.metric("Suppliers at Risk", AT_RISK)

st.divider()

# ---------------- RECENT ACTIVITY ----------------
st.subheader("Recent Activity")

activity = pd.DataFrame({
    "Supplier": random.sample([
        "Maersk Line", "Tata Steel", "Foxconn", "Li & Fung",
        "BASF SE", "DHL Supply Chain", "Arvind Ltd"
    ], 5),
    "Document Type": ["Invoice", "Utility Bill", "Freight Doc", "Invoice", "Invoice"],
    "AI Confidence": [92, 88, 74, 95, 81],
    "Status": ["Verified", "Verified", "Review", "Verified", "Check"]
})

st.dataframe(activity, use_container_width=True, hide_index=True)

st.divider()

# ---------------- CTA ----------------
st.subheader("Next Actions")

col1, col2 = st.columns(2)

with col1:
    st.success("Upload new supplier documents to improve coverage.")
    st.page_link("pages/2_Upload_Invoice.py", label="📤 Upload Invoice")

with col2:
    st.warning("Review suppliers with low confidence scores.")
    st.page_link("pages/5_Supplier_Intelligence.py", label="🧠 View Supplier Intelligence")
