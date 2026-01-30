import streamlit as st
import pandas as pd
import json
import base64
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Upload Invoice", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📤 Upload Invoice")
st.caption("Messy invoices → structured Scope 3 JSON")

# ---------------- SESSION STATE ----------------
if "supplier_registry" not in st.session_state:
    st.session_state.supplier_registry = {}

# ---------------- SIDEBAR: SUPPLIER MAPPING ----------------
with st.sidebar:
    st.subheader("➕ Add Supplier Mapping")

    supplier_name = st.text_input("Supplier Name")
    utility_provider = st.text_input("Utility Provider")

    if st.button("Save Mapping"):
        if supplier_name and utility_provider:
            st.session_state.supplier_registry[utility_provider] = supplier_name
            st.success("Mapping saved")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload invoice (PNG, JPG, PDF)",
    type=["png", "jpg", "jpeg", "pdf"]
)

# ---------------- LAYOUT ----------------
left, right = st.columns([1, 2])

# ---------------- IMAGE PREVIEW ----------------
if uploaded_file:
    with left:
        st.subheader("🖼 Invoice Preview")
        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, use_container_width=True)
        else:
            st.info("PDF uploaded (preview skipped)")

# ---------------- EXTRACTION FUNCTION ----------------

import base64
import json
import re

def extract_invoice(file):
    encoded = base64.b64encode(file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a compliance-grade extraction agent. "
                    "Extract ONLY values clearly visible in the invoice. "
                    "Return STRICT JSON only. "
                    "Return null if unclear. "
                    "Do NOT add any commentary."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract invoice data in this JSON format:\n"
                            "{"
                            "\"energy_usage_kwh\": number | null,"
                            "\"billing_period\": {\"start_date\": string | null, \"end_date\": string | null},"
                            "\"utility_provider\": string | null,"
                            "\"country\": string | null,"
                            "\"raw_text_snippet\": string | null,"
                            "\"confidence\": number"
                            "}"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    raw = response.choices[0].message.content

    # Defensive JSON extraction (important)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON returned by model")

    return json.loads(match.group())


# ---------------- RUN EXTRACTION ----------------
if uploaded_file and st.button("Run AI Extraction"):
    with st.spinner("Extracting invoice data…"):
        try:
            data = extract_invoice(uploaded_file)

            utility = data.get("utility_provider")
            supplier = st.session_state.supplier_registry.get(
                utility, "AUTO-CREATED SUPPLIER"
            )

            data["mapped_supplier"] = supplier

            st.success("Invoice extracted successfully")

            # ---------------- OUTPUT ----------------
            with right:
                st.subheader("📦 Extraction Output")

                view = st.radio(
                    "View format",
                    ["Table View", "Raw JSON"],
                    horizontal=True
                )

                if view == "Raw JSON":
                    st.json(data)
                else:
                    df = pd.DataFrame([data])
                    st.dataframe(df, use_container_width=True)

                # ---------------- EXPORTS ----------------
                st.download_button(
                    "⬇️ Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name="scope3_invoice.json"
                )

                st.download_button(
                    "⬇️ Download CSV",
                    data=pd.DataFrame([data]).to_csv(index=False),
                    file_name="scope3_invoice.csv"
                )

        except Exception as e:
            st.error("Extraction failed")
            st.exception(e)
