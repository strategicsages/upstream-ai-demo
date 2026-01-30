import streamlit as st
import base64
import json
import re
from openai import OpenAI

st.title("📤 Upload Invoice")
st.caption("Messy invoices → structured Scope 3 data")

# --- OpenAI Client ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Ensure supplier data exists ---
if "suppliers_df" not in st.session_state:
    st.error("Supplier data not initialized. Please visit Dashboard first.")
    st.stop()

df = st.session_state.suppliers_df

# --- JSON safety helper ---
def extract_json_safely(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None

# --- UI ---
company = st.selectbox(
    "Receiving Company (Data Consumer)",
    ["Nike", "Apple", "Unilever", "Custom"]
)

supplier = st.selectbox("Supplier", df["Supplier Name"])

uploaded_file = st.file_uploader(
    "Upload invoice (PNG, JPG, PDF)",
    ["png", "jpg", "jpeg", "pdf"]
)

# --- File encoder ---
def encode_file(file):
    return base64.b64encode(file.read()).decode("utf-8")

# --- Run extraction ---
if uploaded_file and st.button("Run AI Invoice Extraction"):
    with st.spinner("Extracting invoice using AI…"):
        file_b64 = encode_file(uploaded_file)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Upstream AI. "
                        "Return ONLY valid JSON. No explanations. "
                        "Schema:\n"
                        "{\n"
                        '  "energy_usage_kwh": number|null,\n'
                        '  "billing_period": {\n'
                        '    "start_date": string|null,\n'
                        '    "end_date": string|null\n'
                        "  },\n"
                        '  "utility_provider": string|null,\n'
                        '  "country": string|null,\n'
                        '  "confidence": number\n'
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all fields from this invoice."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{file_b64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0
        )

    raw_text = response.choices[0].message.content
    extracted = extract_json_safely(raw_text)

    if not extracted:
        st.error("❌ AI could not produce valid structured data.")
        st.markdown("**Raw model output (for audit):**")
        st.code(raw_text)
        st.stop()

    # --- Defaults to prevent crashes ---
    extracted.setdefault("confidence", 0)
    extracted.setdefault("energy_usage_kwh", None)
    extracted.setdefault(
        "billing_period",
        {"start_date": None, "end_date": None}
    )

    st.success("✅ Invoice extracted successfully")
    st.json(extracted)

    # --- Update supplier metrics ---
    confidence = extracted["confidence"]

    df.loc[df["Supplier Name"] == supplier, "Invoices Processed"] += 1
    df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] = int(
        (df.loc[df["Supplier Name"] == supplier, "Avg. AI Confidence"] + confidence) / 2
    )

    st.info(f"Supplier **{supplier}** updated for **{company}**")
