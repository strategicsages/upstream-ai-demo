import streamlit as st
import json
import re
from openai import OpenAI

st.set_page_config(page_title="Upload Invoice", layout="wide")

st.title("📤 Upload Invoice")
st.markdown("Messy invoices → structured Scope 3 data")

# ------------------ CONFIG ------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------ LOAD SUPPLIERS ------------------
df = st.session_state.get("suppliers_df")

if df is None or df.empty:
    st.error("No suppliers found. Add suppliers first.")
    st.stop()

# ------------------ FORM ------------------
col1, col2 = st.columns(2)

with col1:
    receiving_company = st.selectbox(
        "Receiving Company (Data Consumer)",
        ["Nike", "Apple", "Unilever", "Tesla"]
    )

with col2:
    supplier = st.selectbox(
        "Supplier",
        sorted(df["Supplier Name"].unique())
    )

uploaded = st.file_uploader(
    "Upload invoice (PNG, JPG, PDF)",
    type=["png", "jpg", "jpeg", "pdf"]
)

# ------------------ EXTRACTOR ------------------
def safe_extract_json(text):
    """
    Extracts JSON even if model adds text around it.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    return json.loads(match.group())

# ------------------ RUN EXTRACTION ------------------
if uploaded and st.button("Run AI Invoice Extraction"):

    with st.spinner("Extracting invoice data with AI…"):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract structured invoice data. "
                        "Return ONLY valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Extract energy or logistics invoice data. "
                        "Return JSON with keys:\n"
                        "energy_usage_kwh (number)\n"
                        "billing_period {start_date, end_date}\n"
                        "utility_provider (string)\n"
                        "country (string)\n"
                        "confidence (0-1 float)"
                    )
                }
            ]
        )

        raw_text = response.choices[0].message.content

        try:
            extracted = safe_extract_json(raw_text)
        except Exception as e:
            st.error("AI returned invalid JSON")
            st.code(raw_text)
            st.stop()

    # ------------------ SUCCESS ------------------
    st.success("Invoice extracted successfully")
    st.json(extracted)

    # ------------------ UPDATE SUPPLIER ------------------
    idx = df[df["Supplier Name"] == supplier].index[0]

    df.at[idx, "Invoices Processed"] += 1
    df.at[idx, "Avg. AI Confidence"] = int(extracted["confidence"] * 100)

    df.at[idx, "Status"] = (
        "✅ Verified"
        if extracted["confidence"] > 0.85
        else "⚠️ Review"
    )

    st.session_state.suppliers_df = df

    st.info(
        f"Supplier **{supplier}** updated for **{receiving_company}**"
    )
