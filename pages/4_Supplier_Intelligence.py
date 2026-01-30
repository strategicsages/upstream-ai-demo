import streamlit as st

st.title("📊 Supplier Intelligence")

st.subheader("Supplier A")

st.metric("Reliability Score", "88 / 100")
st.progress(0.88)

st.subheader("AI Insight")
st.info(
    "Supplier A consistently submits high-quality invoices with "
    "clear billing periods and minimal review intervention."
)
