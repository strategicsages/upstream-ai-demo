import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PIL import Image
from pdf2image import convert_from_bytes
import io
import base64
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Upstream AI", layout="wide")
st.title("⚡ Upstream AI — Scope 3 Invoice Extraction Agent")

def pdf_to_image(file_bytes):
    images = convert_from_bytes(file_bytes)
    buf = io.BytesIO()
    images[0].save(buf, format="PNG")
    buf.seek(0)
    return buf

def encode_image(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Upload Invoice", "Review Queue", "Audit Log"])

if "review_queue" not in st.session_state:
    st.session_state.review_queue = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if page == "Upload Invoice":

    st.subheader("📤 Upload Supplier Invoice")
    uploaded = st.file_uploader("Upload invoice", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded:

        # Convert PDF → image
        if uploaded.type == "application/pdf":
            invoice_image = Image.open(pdf_to_image(uploaded.read()))
        else:
            invoice_image = Image.open(uploaded)

        st.image(invoice_image, width=500)

        st.markdown("---")
        st.write("### 🔍 Extracting data…")

        img_b64 = encode_image(invoice_image)

        # ---------------------------
        # 💡 FIXED, VALID API CALL
        # ---------------------------
        response = client.responses.create(
            model="gpt-4.1-mini",    # SAFE MODEL FOR STREAMLIT CLOUD
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": """
You are Upstream AI. Return ONLY this JSON:

{
  "energy_usage_kwh": number|null,
  "billing_period": { "start_date": string|null, "end_date": string|null },
  "utility_provider": string|null,
  "country": string|null,
  "raw_text_snippet": string|null,
  "confidence": number
}
"""
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Extract structured fields from this invoice."},
                        {"type": "input_image", "image": img_b64}
                    ]
                }
            ],
            max_output_tokens=600
        )

        extracted = json.loads(response.output_text)

        st.json(extracted)

        st.session_state.review_queue.append({
            "image": invoice_image,
            "data": extracted
        })

        st.session_state.audit_log.append(
            f"Uploaded invoice (confidence {extracted['confidence']})"
        )

        st.success("Extraction complete! Added to Review Queue.")

elif page == "Review Queue":

    st.subheader("📝 Human Review Queue")

    if len(st.session_state.review_queue) == 0:
        st.info("No invoices pending review.")
    else:
        for idx, item in enumerate(st.session_state.review_queue):

            st.markdown(f"## Invoice #{idx+1}")

            col1, col2 = st.columns(2)

            with col1:
                st.image(item["image"], width=400)

            with col2:
                editable = st.text_area(
                    "Extracted JSON (editable):",
                    json.dumps(item["data"], indent=2),
                    height=300
                )

                edited_json = json.loads(editable)
                confidence = edited_json.get("confidence", 0)

                if confidence >= 90:
                    st.success("High confidence")
                elif confidence >= 70:
                    st.warning("Needs Review")
                else:
                    st.error("Low Confidence")

                if st.button(f"Approve #{idx+1}"):
                    st.success("Synced to ERP")
                    st.session_state.review_queue.pop(idx)
                    st.experimental_rerun()

                if st.button(f"Flag #{idx+1}"):
                    st.warning("Flagged")
                    st.session_state.audit_log.append(f"Flagged invoice #{idx+1}")

                if st.button(f"Request Resubmission #{idx+1}"):
                    st.error("Requested resubmission")
                    st.session_state.review_queue.pop(idx)
                    st.experimental_rerun()

elif page == "Audit Log":
    st.subheader("📚 Audit Log")
    for i, log in enumerate(st.session_state.audit_log):
        st.write(f"{i+1}. {log}")
