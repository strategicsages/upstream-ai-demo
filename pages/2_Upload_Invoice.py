import streamlit as st
if "suppliers_df" not in st.session_state:
    st.session_state.suppliers_df = df.copy()
st.title("📤 Upload Invoice")

uploaded_file = st.file_uploader(
    "Upload supplier invoice (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    st.success("Invoice uploaded successfully")

    st.subheader("🧠 Agent Workflow Status")
    st.markdown("""
    ✔ Extraction Agent  
    ✔ Validation Agent  
    ✔ Intelligence Agent  
    ⏳ Enablement Agent (planned)
    """)

    st.subheader("Extracted Output (JSON)")
    st.code("""
{
  "energy_usage_kwh": 1312,
  "billing_period": {
    "start_date": "2024-01-15",
    "end_date": "2024-02-15"
  },
  "utility_provider": "Bright Energy",
  "confidence": 90
}
""", language="json")

    st.button("Add to Review Queue")
    st.button("Add to Supplier Record")
