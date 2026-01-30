import streamlit as st

st.title("📊 Dashboard")

df = st.session_state.get("suppliers_df")

if df is None:
    st.info("No supplier data yet.")
    st.stop()

st.subheader("⚠️ Low Confidence Suppliers")
low = df[df["Avg. AI Confidence"] < 75]

if low.empty:
    st.success("All suppliers healthy")
else:
    st.dataframe(low[["Supplier Name", "Avg. AI Confidence", "Status"]])
