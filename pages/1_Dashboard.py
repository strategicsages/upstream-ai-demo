import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Supplier Intelligence Dashboard")

df = st.session_state.get("suppliers_df")

if df is None:
    st.info("Upload invoices to start populating supplier intelligence.")
    st.stop()

# ---- ALERTS ----
st.subheader("🚨 Live Alerts")
if st.session_state.alerts:
    for alert in st.session_state.alerts[-3:]:
        st.error(alert)
else:
    st.success("No critical supplier issues detected")

# ---- METRICS ----
c1, c2, c3 = st.columns(3)
c1.metric("Suppliers Tracked", len(df))
c2.metric("Invoices Processed", int(df["Invoices Processed"].sum()))
c3.metric("Avg AI Confidence", f"{int(df['Avg. AI Confidence'].mean())}%")

st.divider()

# ---- TABLE ----
st.subheader("Supplier Health Overview")
st.dataframe(df, use_container_width=True)
