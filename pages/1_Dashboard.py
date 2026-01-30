import streamlit as st
import pandas as pd
import random

st.set_page_config(layout="wide")
st.title("📊 Dashboard")

# ---- INIT SUPPLIERS ----
if "suppliers_df" not in st.session_state:
    suppliers = [
        ("Maersk Line","Denmark","Logistics"),
        ("DHL Supply Chain","Germany","Logistics"),
        ("Foxconn","Taiwan","Electronics"),
        ("Arvind Ltd","India","Textiles"),
        ("Tata Steel","India","Steel"),
        ("BASF","Germany","Chemicals"),
        ("Infosys","India","IT Services"),
        ("Accenture","Ireland","Consulting"),
    ]
    rows = []
    for s,c,cat in suppliers:
        conf = random.randint(60,95)
        rows.append({
            "Supplier Name": s,
            "Category": cat,
            "Country": c,
            "Invoices Processed": random.randint(5,40),
            "Avg. AI Confidence": conf,
            "Data Reliability": random.randint(60,99),
        })
    st.session_state.suppliers_df = pd.DataFrame(rows)

df = st.session_state.suppliers_df

# ---- METRICS ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Suppliers", len(df))
c2.metric("Invoices", df["Invoices Processed"].sum())
c3.metric("Avg Confidence", f"{int(df['Avg. AI Confidence'].mean())}%")
c4.metric("At Risk", len(df[df["Avg. AI Confidence"] < 70]))

st.divider()
st.subheader("Suppliers Requiring Attention")
st.dataframe(df[df["Avg. AI Confidence"] < 70], use_container_width=True, hide_index=True)
