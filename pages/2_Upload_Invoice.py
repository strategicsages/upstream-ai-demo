import streamlit as st
import random

st.title("📤 Upload Invoice")

df = st.session_state.suppliers_df

company = st.selectbox(
    "Receiving Company",
    ["Nike","Apple","Unilever","Custom"]
)

supplier = st.selectbox("Supplier", df["Supplier Name"])

file = st.file_uploader("Upload invoice", ["png","jpg","pdf"])

if file:
    if st.button("Run AI Extraction"):
        confidence = random.randint(60,95)
        df.loc[df["Supplier Name"] == supplier, "Invoices Processed"] += 1
        df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] = confidence

        st.success("Invoice processed")
        st.json({
            "supplier": supplier,
            "confidence": confidence,
            "company": company
        })

st.divider()

with st.expander("➕ Add New Supplier"):
    name = st.text_input("Supplier Name")
    category = st.selectbox("Category", ["Logistics","Textiles","Electronics","Steel"])
    country = st.text_input("Country")

    if st.button("Add Supplier"):
        st.session_state.suppliers_df.loc[len(df)] = [
            name, category, country, 0, 0, 0
        ]
        st.success("Supplier added")
