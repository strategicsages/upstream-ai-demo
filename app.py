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
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.set_page_config(page_title="Upstream AI", layout="wide")
st.title("⚡ Upstream AI — Invoice Extraction (Stable Version)")


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


# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Upload Invoice", "Review Queue", "Audit Log"])

if "review_queue" not in st.session_state:
    st.session_state.review_queue = []
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []


# =======================
# PAGE 1 — UPLOAD INVOICE
# =======================
if page == "Upload Invoice":

    st.subheader("📤 Upload Invoice")
    uploaded = st.file_uploader("Upload file", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded:

        if uploaded.type == "application/pdf":
            invoice_image = Image.open(pdf_to_image(uploaded.read()))
        else:
            invoice_image = Image.open(uploaded)

        st.image(invoice_image, width=450)

        img_b64 = encode_image(invoice_image)

        st.write("### Extracting data...")

        # ⭐ FINAL WORKING CHAT COMPLETIONS CALL ⭐
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a structured invoice extraction agent.
Extract ONLY this JSON:
{
  "energy_usage_kwh": number|null,
  "billing_period": {"start_date": string|null, "end_date": string|null},
  "utility_provider": string|null,
  "country": string|null,
  "raw_text_snippet": string|null,
  "confidence": number
}
"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract fields from this invoice."},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/png;base64,{img_b64}"
                        }
                    ],
                }
            ],
            temperature=0
        )

        extracted_json = json.loads(response.choices[0].message["content"])

        st.json(extracted_json)

        st.session_state.review_queue.append({
            "image": invoice_image,
            "data": extracted_json
        })

        st.session_state.audit_log.append("Uploaded invoice")

        st.success("Extraction completed!")


# =======================
# PAGE 2 — REVIEW QUEUE
# =======================
elif page == "Review Queue":

    st.subheader("📝 Review Queue")

    if len(st.session_state.review_queue) == 0:
        st.info("Nothing pending.")
    else:
        for idx, item in enumerate(st.session_state.review_queue):

            st.image(item["image"], width=300)

            editable = st.text_area(
                "Extracted JSON",
                value=json.dumps(item["data"], indent=2),
                height=280
            )

            if st.button(f"Approve #{idx+1}"):
                st.success("Approved")
                st.session_state.review_queue.pop(idx)
                st.experimental_rerun()

            if st.button(f"Reject #{idx+1}"):
                st.error("Rejected")
                st.session_state.review_queue.pop(idx)
                st.experimental_rerun()


# =======================
# PAGE 3 — AUDIT LOG
# =======================
elif page == "Audit Log":
    st.subheader("📚 Audit Log")
    st.write(st.session_state.audit_log)
