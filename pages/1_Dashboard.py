import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Dashboard")
st.caption("Live view of supplier data quality and ingestion health")

# Initialize supplier state
if "suppliers_df" not in st.session_state:
    st.session_state.suppliers_df = pd.DataFrame([
        {"Supplier Name": "Arvind Ltd", "Category": "Textiles", "Country": "India", "Invoices Processed": 12, "Avg. AI Confidence": 62},
        {"Supplier Name": "Maersk Line", "Category": "Logistics", "Country": "Denmark", "Invoices Processed": 45, "Avg. AI Confidence": 92},
        {"Supplier Name": "Foxconn", "Category": "Electronics", "Country": "Taiwan", "Invoices Processed": 28, "Avg. AI Confidence": 85},
    ])

df = st.session_state.suppliers_df

c1, c2, c3, c4 = st.columns(4)
c1.metric("Suppliers", len(df))
c2.metric("Invoices Processed", df["Invoices Processed"].sum())
c3.metric("Avg AI Confidence", f"{int(df['Avg. AI Confidence'].mean())}%")
c4.metric("Suppliers at Risk", len(df[df["Avg. AI Confidence"] < 70]))

st.divider()
st.subheader("Suppliers Needing Attention")
st.dataframe(df[df["Avg. AI Confidence"] < 70], use_container_width=True, hide_index=True)
