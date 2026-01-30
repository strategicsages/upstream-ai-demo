import streamlit as st
import json
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Supplier Intelligence", layout="wide")
st.title("🧠 Supplier Intelligence")

# ---- Mock supplier list for demo ----
suppliers = [
    {
        "supplier_name": "Maersk Line",
        "category": "Logistics",
        "country": "Denmark",
        "avg_ai_confidence": 92,
        "invoices_processed": 48,
        "null_field_rate": 0.05,
        "tech_maturity": "high"
    },
    {
        "supplier_name": "Arvind Ltd",
        "category": "Textiles",
        "country": "India",
        "avg_ai_confidence": 61,
        "invoices_processed": 9,
        "null_field_rate": 0.42,
        "tech_maturity": "low"
    }
]

supplier_names = [s["supplier_name"] for s in suppliers]
selected = st.selectbox("Select Supplier", supplier_names)

supplier_context = next(s for s in suppliers if s["supplier_name"] == selected)

st.subheader("Supplier Context")
st.json(supplier_context)

if st.button("Run Supplier Intelligence Agent"):
    with st.spinner("Analyzing supplier…"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise Supplier Intelligence Agent for Scope 3 programs."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Given the following supplier data, evaluate reliability and recommend next actions.

Supplier Context:
{json.dumps(supplier_context, indent=2)}

Return STRICT JSON with:
- supplier_tier
- risk_summary
- recommended_action
- enablement_plan (array)
- business_impact
"""
                }
            ],
            temperature=0
        )

        raw = response.choices[0].message.content
        result = json.loads(raw)

        st.subheader("Agent Recommendation")
        st.json(result)
