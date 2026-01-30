import streamlit as st
import pandas as pd
import json
import re
from openai import OpenAI
from io import BytesIO

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Upload Invoice", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📤 Upload Invoice")
st.caption("Messy invoices → structured Scope 3 data")

# ------------------ SESSION STATE ------------------
if "supplier_registry" not in st.session_state:
    st.session_state.supplier_registry = {
        "HSBC VN": "DHL Supply Chain",
        "Vietnam Power": "Maersk Line"
    }

if "extracted_rows" not in st.session_state:
    st.session_state.extracted_rows = []

# ------------------ ADD SUPPLIER (TOP RIGHT) ------------------
with st.sidebar:
    st.subheader("➕ Add Supplier Mapping")

    new_supplier = st.text_input("Supplier Name")
    utility_provider = st.text_input("Utility Provider")

    if st.button("Save Mapping"):
        if new_supplier and utility_provider:
            st.session_state.supplier_registry[utility_provider] = new_supplier
            st.success("Supplier mapping added")

# ------------------ FILE UPLOAD ------------------
uploaded_files = st.file_uploader(
    "Upload invoices (PDF, images, handwritten)",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True
)

# ------------------ JSON EXTRACTOR ------------------
def extract_json_safe(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    return json.loads(match.group())

# ------------------ RUN EXTRACTION ------------------
if uploaded_files and st.button("Run AI Extraction"):

    st.session_state.extracted_rows = []

    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):

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
                            "Extract invoice data and return JSON with:\n"
                            "utility_provider\n"
                            "country\n"
                            "energy_usage_kwh\n"
                            "billing_start\n"
                            "billing_end\n"
                            "confidence (0-1)"
                        )
                    }
                ]
            )

            raw = response.choices[0].message.content

            try:
                data = extract_json_safe(raw)
            except:
                st.error(f"Failed to parse {file.name}")
                st.code(raw)
                continue

            supplier = st.session_state.supplier_registry.get(
                data["utility_provider"],
                "NEW SUPPLIER (AUTO-CREATED)"
            )

            row = {
                "File": file.name,
                "Utility Provider": data["utility_provider"],
                "Mapped Supplier": supplier,
                "Country": data["country"],
                "Energy Usage (kWh)": data["energy_usage_kwh"],
                "Billing Start": data["billing_start"],
                "Billing End": data["billing_end"],
                "Confidence": data["confidence"]
            }

            st.session_state.extracted_rows.append(row)

    st.success("Extraction complete")

# ------------------ RESULTS ------------------
if st.session_state.extracted_rows:

    df = pd.DataFrame(st.session_state.extracted_rows)

    st.subheader("📄 Extracted Data")
    st.dataframe(df, use_container_width=True)

    # JSON EXPORT
    st.subheader("📦 Export")

    st.download_button(
        "⬇️ Download JSON",
        data=json.dumps(st.session_state.extracted_rows, indent=2),
        file_name="scope3_output.json"
    )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name="scope3_output.csv"
    )

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        "⬇️ Download Excel",
        data=buffer.getvalue(),
        file_name="scope3_output.xlsx"
    )
