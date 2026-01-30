import streamlit as st

st.title("🏭 Suppliers")

st.table({
    "Supplier": ["Supplier A", "Supplier B", "Supplier C"],
    "Country": ["India", "Vietnam", "Mexico"],
    "Invoices": [12, 7, 5],
    "Avg Confidence": ["92%", "85%", "78%"],
    "Reliability": [88, 74, 81]
})
