import streamlit as st
from openai import OpenAI
from PIL import Image
from pdf2image import convert_from_bytes
import io
import base64
import json

# --------------------------------------------------------
# INITIALIZE OPENAI CLIENT FROM STREAMLIT SECRETS
# --------------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Upstream AI", layout="wide")
st.title("⚡ Upstream AI — Scope 3 Invoice Extractor")

# --------------------------------------------------------
# HELPERS
# --------------------------------------------------------
def pdf_to_image(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    buf = io.BytesIO()
    images[0].save(buf, format="PNG")
    buf.seek(0)
    return buf

def encode_image(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# --------------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------------
page = st.sidebar.radio("Navigation", ["Upload Invoice", "Review Queue", "Audit Log"])

if "review_queue" not in st.session_state:
    st.session_state.review_queue = []
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

# ========================================================
# PAGE 1 — UPLOAD INVOICE
# ========================================================
if page == "Upload Invoice":

    st.subheader("📤 Upload Supplier Invoice")
    file = st.file_uploader("Upload PNG / JPG / PDF", type=["png", "jpg", "jpeg", "pdf"])

    if file:

        # Convert PDF → Image
        if file.type == "application/pdf":
            invoice_image = Image.open(pdf_to_image(file.read()))
        else:
            invoice_image = Image.open(file)

        st.image(invoice_image, width=450)

        st.write("### 🔍 Extracting fields using Upstream AI…")

        img_b64 = encode_image(invoice_image)

        # --------------------------------------------------------
        # 🔥 FINAL WORKING CHAT.COMPLETIONS CALL
        # (correct multimodal schema for your SDK)
        # --------------------------------------------------------
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Upstream AI. Extract ONLY this JSON:

{
  "energy_usage_kwh": number|null,
  "billing_period": {
    "start_date": string|null,
    "end_date": string|null
  },
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

        # Parse output
      # Parse output
raw = response.choices[0].message.content
extracted = json.loads(raw)
st.json(extracted)


        # Save for human review
        st.session_state.review_queue.append({
            "image": invoice_image,
            "data": extracted
        })

        st.session_state.audit_log.append("Uploaded invoice")

        st.success("Extraction complete! Added to Review Queue.")


# ========================================================
# PAGE 2 — REVIEW QUEUE
# ========================================================
elif page == "Review Queue":

    st.subheader("📝 Human Review Queue")

    if len(st.session_state.review_queue) == 0:
        st.info("No invoices pending review.")
    else:
        for idx, item in enumerate(st.session_state.review_queue):

            st.image(item["image"], width=400)

            editable = st.text_area(
                "Extracted JSON (editable):",
                json.dumps(item["data"], indent=2),
                height=260
            )

            edited_json = json.loads(editable)
            conf = edited_json.get("confidence", 0)

            if conf >= 90:
                st.success(f"Confidence: {conf}")
            elif conf >= 70:
                st.warning(f"Confidence: {conf}")
            else:
                st.error(f"Confidence: {conf}")

            if st.button(f"Approve #{idx+1}"):
                st.success("Approved & synced")
                st.session_state.review_queue.pop(idx)
                st.session_state.audit_log.append(f"Approved invoice #{idx+1}")
                st.experimental_rerun()

            if st.button(f"Reject #{idx+1}"):
                st.error("Rejected")
                st.session_state.review_queue.pop(idx)
                st.session_state.audit_log.append(f"Rejected invoice #{idx+1}")
                st.experimental_rerun()


# ========================================================
# PAGE 3 — AUDIT LOG
# ========================================================
elif page == "Audit Log":

    st.subheader("📚 Audit Log")
    for i, log in enumerate(st.session_state.audit_log):
        st.write(f"{i+1}. {log}")
