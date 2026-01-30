import streamlit as st
import json
import re
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Supplier Intelligence", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧠 Supplier Intelligence")
st.caption("AI-driven supplier recommendations & enablement decisions")

# ---------------- SAFE JSON EXTRACTOR ----------------
def extract_json_safe(text):
    """
    Extracts the first valid JSON object from model output.
    Prevents crashes from stray text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in output")
    return json.loads(match.group())

# ---------------- MOCK SUPPLIER DATA (DEMO SAFE) ----------------
suppliers = [
    {
        "supplier_name": "Maersk Line",
        "category": "Logistics",
        "country": "Denmark",
        "avg_ai_confidence": 93,
        "invoices_processed": 46,
        "null_field_rate": 0.04,
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
selected_supplier = st.selectbox("Select Supplier", supplier_names)

supplier_context = next(
    s for s in suppliers if s["supplier_name"] == selected_supplier
)

# ---------------- DISPLAY CONTEXT ----------------
st.subheader("📊 Supplier Context")
st.json(supplier_context)

# ---------------- RUN AGENT ----------------
if st.button("Run Supplier Intelligence Agent"):
    with st.spinner("Analyzing supplier performance..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise Supplier Intelligence Agent.\n"
                        "You MUST return ONLY valid JSON.\n"
                        "NO markdown. NO explanations. NO commentary.\n"
                        "Violating format breaks the system."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Evaluate the supplier below and decide next actions.

Supplier Context:
{json.dumps(supplier_context, indent=2)}

Return STRICT JSON with EXACTLY this schema:

{{
  "supplier_tier": "Preferred | Monitor | Enablement Required",
  "risk_summary": string,
  "recommended_action": "AI-only | Hybrid | Human-led",
  "enablement_plan": [string, string, string],
  "business_impact": string
}}
"""
                }
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content

        try:
            result = extract_json_safe(raw_output)
        except Exception:
            st.error("❌ Agent returned invalid output")
            st.subheader("Raw Model Output (Debug)")
            st.code(raw_output)
            st.stop()

        # ---------------- SHOW RESULTS ----------------
        st.subheader("🧠 Agent Recommendation")
        st.json(result)

        # Optional visual emphasis
        tier = result.get("supplier_tier", "")
        if tier == "Preferred":
            st.success("🌟 Preferred Supplier")
        elif tier == "Monitor":
            st.warning("⚠️ Supplier Requires Monitoring")
        else:
            st.error("🚨 Supplier Requires Enablement")
