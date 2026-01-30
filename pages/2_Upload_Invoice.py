import streamlit as st
import random

st.title("📤 Upload Supplier Invoice")
st.caption("Messy documents → structured data")

supplier = st.selectbox(
    "Select Supplier",
    st.session_state.suppliers_df["Supplier Name"]
)

uploaded = st.file_uploader("Upload invoice", type=["png", "jpg", "pdf"])

if uploaded:
    st.image(uploaded, caption="Uploaded Document", width=250)

    if st.button("Run AI Extraction"):
        confidence = random.randint(60, 95)

        df = st.session_state.suppliers_df
        df.loc[df["Supplier Name"] == supplier, "Invoices Processed"] += 1
        df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] = int(
            (df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] + confidence) / 2
        )

        st.success("Invoice processed and supplier updated")
        st.json({
            "supplier": supplier,
            "confidence": confidence,
            "status": "added to supplier record"
        })
