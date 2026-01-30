import streamlit as st
import base64
import json
from openai import OpenAI

st.title("📤 Upload Invoice")
st.caption("Messy invoices → structured Scope 3 data")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

df = st.session_state.suppliers_df

# --- Select receiving company ---
company = st.selectbox(
    "Receiving Company (Data Consumer)",
    ["Nike", "Apple", "Unilever", "Custom"]
)

# --- Supplier selection ---
supplier = st.selectbox(
    "Supplier",
    list(df["Supplier Name"]) + ["➕ Add New Supplier"]
)

if supplier == "➕ Add New Supplier":
    new_name = st.text_input("New Supplier Name")
    new_category = st.selectbox("Category", ["Logistics", "Textiles", "Electronics", "Steel"])
    new_country = st.text_input("Country")

    if st.button("Add Supplier"):
        st.session_state.suppliers_df.loc[len(df)] = [
            new_name, new_category, new_country, 0, 0, 0
        ]
        st.success("Supplier added. Select it above.")
        st.stop()

# --- Upload invoice ---
file = st.file_uploader("Upload invoice (image or PDF)", ["png", "jpg", "jpeg", "pdf"])

def encode_file(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

if file and st.button("Run AI Invoice Extraction"):
    with st.spinner("Extracting invoice using AI..."):
        img_b64 = encode_file(file)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Upstream AI.
Extract ONLY valid JSON:

{
  "energy_usage_kwh": number|null,
  "billing_period": {
    "start_date": string|null,
    "end_date": string|null
  },
  "utility_provider": string|null,
  "country": string|null,
  "confidence": number
}
"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all fields from this invoice."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0
        )

        extracted = json.loads(response.choices[0].message.content)

    st.success("Invoice extracted successfully")
    st.json(extracted)

    # --- Update supplier metrics ---
    confidence = extracted.get("confidence", 0)

    df.loc[df["Supplier Name"] == supplier, "Invoices Processed"] += 1
    df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] = int(
        (df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] + confidence) / 2
    )

    st.info(f"Supplier **{supplier}** updated for **{company}**")
