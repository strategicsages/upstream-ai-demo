import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PIL import Image
from pdf2image import convert_from_bytes
import io
import json

# Load API key
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

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Upload Invoice", "Review Queue", "Audit Log"])

if "review_queue" not in st.session_state:
    st.session_state.review_queue = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if page == "Upload Invoice":

    st.subheader("📤 Upload Supplier Invoice (PDF or Image)")
    uploaded = st.file_uploader("Upload invoice", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded:

        if uploaded.type == "application/pdf":
            file_bytes = uploaded.read()
            converted = pdf_to_image(file_bytes)
            invoice_img = Image.open(converted)
        else:
            invoice_img = Image.open(uploaded)

        st.image(invoice_img, caption="Uploaded Invoice", width=500)

        st.markdown("---")
        st.write("### 🔍 Extracting data with GPT-4o…")

        buf = io.BytesIO()
        invoice_img.save(buf, format="PNG")
        buf.seek(0)
        img_bytes = buf.getvalue()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """
You are Upstream AI, a compliance-grade extraction agent.
Return ONLY this JSON:
{
  "energy_usage_kwh": number | null,
  "billing_period": {
    "start_date": string | null,
    "end_date": string | null
  },
  "utility_provider": string | null,
  "country": string | null,
  "raw_text_snippet": string | null,
  "confidence": number
}
                """},
                {"role": "user",
                 "content": [
                     {"type": "input_text", "text": "Extract all required fields from this invoice."},
                     {"type": "input_image", "image": img_bytes}
                 ]}
            ],
            temperature=0
        )

        extracted = json.loads(response.choices[0].message["content"])

        st.json(extracted, expanded=False)

        st.session_state.review_queue.append({
            "image": invoice_img,
            "data": extracted
        })

        st.session_state.audit_log.append(
            f"Uploaded invoice — Confidence {extracted['confidence']}"
        )

        st.success("Extraction complete! Added to Review Queue.")

elif page == "Review Queue":

    st.subheader("📝 Human Review Queue")

    if len(st.session_state.review_queue) == 0:
        st.info("No invoices pending review.")
    else:
        for idx, item in enumerate(st.session_state.review_queue):

            st.markdown(f"### Invoice #{idx+1}")

            col1, col2 = st.columns(2)

            with col1:
                st.image(item["image"], caption="Invoice Preview", width=400)

            with col2:
                editable = st.text_area(
                    "Extracted JSON (editable):",
                    json.dumps(item["data"], indent=2),
                    height=300
                )

                edited_json = json.loads(editable)

                confidence = edited_json.get("confidence", 0)

                if confidence >= 90:
                    st.success(f"Confidence: {confidence} (Auto-Approve)")
                elif confidence >= 70:
                    st.warning(f"Confidence: {confidence} (Needs Review)")
                else:
                    st.error(f"Confidence: {confidence} (Low)")

                approve = st.button(f"Approve #{idx+1}")
                flag = st.button(f"Flag #{idx+1}")
                reject = st.button(f"Request Resubmission #{idx+1}")

                if approve:
                    st.success("Invoice Approved & Synced.")
                    st.session_state.audit_log.append(f"Approved invoice #{idx+1}")
                    st.session_state.review_queue.pop(idx)
                    st.experimental_rerun()

                if flag:
                    st.warning("Flagged for review.")
                    st.session_state.audit_log.append(f"Flagged invoice #{idx+1}")

                if reject:
                    st.error("Returned to supplier for resubmission.")
                    st.session_state.audit_log.append(f"Requested resubmission #{idx+1}")
                    st.session_state.review_queue.pop(idx)
                    st.experimental_rerun()

elif page == "Audit Log":
    st.subheader("📚 Audit Log")
    if len(st.session_state.audit_log) == 0:
        st.info("No audit events yet.")
    else:
        for i, log in enumerate(st.session_state.audit_log):
            st.write(f"{i+1}. {log}")
