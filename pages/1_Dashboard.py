import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Invoices Processed", "128")
col2.metric("Avg Confidence", "91%")
col3.metric("Suppliers Onboarded", "42")
col4.metric("Scope 3 Coverage", "63%")

st.divider()

st.subheader("Recent Activity")

st.table({
    "Event": [
        "Invoice processed",
        "Supplier reliability updated",
        "Invoice approved"
    ],
    "When": [
        "2 mins ago",
        "15 mins ago",
        "1 hour ago"
    ]
})
