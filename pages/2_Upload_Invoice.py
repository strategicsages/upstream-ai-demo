import streamlit as st
import pandas as pd
import json
import base64
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📤 Upload Invoice")
st.caption("Messy invoices → structured Scope 3 data")

# ---- DEMO COMPANIES ----
company = st.selectbox("Receiving Company (Data Consumer)", ["Nike", "Unilever", "Apple"])

# ---- SUPPLIERS ----
if st.session_state.suppliers_df is None:
    st.session_state.suppliers_df = pd.DataFrame(columns=[
        "Supplier Name", "Category", "Country",
        "Invoices Processed", "Avg. AI Confidence",
        "Data Reliability", "Status"
    ])

df = st.session_state.suppliers_df
supplier_declared = st.selectbox(
    "Declared Supplier",
    options=list(df["Supplier Name"]) + ["➕ Add new supplier"]
)

# ---- FILE UPLOAD ----
file = st.file_uploader("Upload invoice (PNG, JPG, PDF)", type=["png", "jpg", "jpeg", "pdf"])

if st.button("Run AI Invoice Extraction") and file:
    with st.spinner("Extracting invoice data..."):

        img_bytes = file.read()
        img_b64 = base64.b64encode(img_bytes).decode()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Extract ONLY valid JSON:
{
 "energy_usage_kwh": number|null,
 "billing_period": {"start_date": string|null, "end_date": string|null},
 "utility_provider": string|null,
 "country": string|null,
 "confidence": number
}"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract Scope 3 invoice data."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                    ]
                }
            ],
            temperature=0
        )

        extracted = json.loads(response.choices[0].message.content)
        st.success("Invoice extracted successfully")
        st.json(extracted)

        # ---- AUTO SUPPLIER CREATION ----
        if supplier_declared == "➕ Add new supplier":
            supplier_name = extracted.get("utility_provider", "Unknown Supplier")
            new_row = {
                "Supplier Name": supplier_name,
                "Category": "Auto-detected",
                "Country": extracted.get("country"),
                "Invoices Processed": 1,
                "Avg. AI Confidence": int(extracted["confidence"] * 100),
                "Data Reliability": int(extracted["confidence"] * 100),
                "Status": "⚠️ Review"
            }
            st.session_state.suppliers_df = pd.concat(
                [df, pd.DataFrame([new_row])], ignore_index=True
            )
            final_supplier = supplier_name
        else:
            final_supplier = supplier_declared
            idx = df[df["Supplier Name"] == final_supplier].index[0]
            df.at[idx, "Invoices Processed"] += 1
            df.at[idx, "Avg. AI Confidence"] = int(extracted["confidence"] * 100)

        # ---- CONFIDENCE ROUTING ----
        if extracted["confidence"] < 0.8:
            alert = f"Low confidence invoice from {final_supplier} ({int(extracted['confidence']*100)}%)"
            st.session_state.alerts.append(alert)
            st.warning("Routed to Supplier Intelligence Agent")

        # ---- SAVE INVOICE ----
        st.session_state.invoices.append({
            "company": company,
            "supplier": final_supplier,
            "data": extracted
        })
