import streamlit as st
import json
import re
import random
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="VeroFlow: Supplier Intelligence", page_icon="🧠", layout="wide")

# Get API Key from Streamlit Secrets
# Ensure you have .streamlit/secrets.toml set up with OPENAI_API_KEY
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧠 VeroFlow Supplier Intelligence")
st.markdown("### Agentic Risk Assessment & Automated Enablement")

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

# ---------------- EXPANDED MOCK DATA (20 Suppliers) ----------------
# Real-world names with synthetic risk profiles
suppliers = [
    {"supplier_name": "Maersk Line", "category": "Logistics", "country": "Denmark", "avg_ai_confidence": 93, "invoices_processed": 146, "null_field_rate": 0.04, "tech_maturity": "high"},
    {"supplier_name": "Arvind Ltd", "category": "Textiles", "country": "India", "avg_ai_confidence": 61, "invoices_processed": 9, "null_field_rate": 0.42, "tech_maturity": "low"},
    {"supplier_name": "Foxconn Tech", "category": "Electronics", "country": "Taiwan", "avg_ai_confidence": 88, "invoices_processed": 312, "null_field_rate": 0.08, "tech_maturity": "high"},
    {"supplier_name": "Viet Textile Co", "category": "Textiles", "country": "Vietnam", "avg_ai_confidence": 45, "invoices_processed": 4, "null_field_rate": 0.65, "tech_maturity": "low"},
    {"supplier_name": "DHL Supply Chain", "category": "Logistics", "country": "Germany", "avg_ai_confidence": 91, "invoices_processed": 89, "null_field_rate": 0.05, "tech_maturity": "high"},
    {"supplier_name": "Tata Steel", "category": "Raw Materials", "country": "India", "avg_ai_confidence": 82, "invoices_processed": 56, "null_field_rate": 0.12, "tech_maturity": "medium"},
    {"supplier_name": "Shenzhou Intl", "category": "Textiles", "country": "China", "avg_ai_confidence": 74, "invoices_processed": 23, "null_field_rate": 0.25, "tech_maturity": "medium"},
    {"supplier_name": "BASF SE", "category": "Chemicals", "country": "Germany", "avg_ai_confidence": 89, "invoices_processed": 77, "null_field_rate": 0.06, "tech_maturity": "high"},
    {"supplier_name": "Li & Fung", "category": "Sourcing", "country": "Hong Kong", "avg_ai_confidence": 85, "invoices_processed": 210, "null_field_rate": 0.10, "tech_maturity": "high"},
    {"supplier_name": "Gildan Activewear", "category": "Apparel", "country": "Canada", "avg_ai_confidence": 79, "invoices_processed": 45, "null_field_rate": 0.18, "tech_maturity": "medium"},
    {"supplier_name": "Small Batch Weavers", "category": "Textiles", "country": "Bangladesh", "avg_ai_confidence": 32, "invoices_processed": 2, "null_field_rate": 0.78, "tech_maturity": "low"},
    {"supplier_name": "Nippon Steel", "category": "Raw Materials", "country": "Japan", "avg_ai_confidence": 88, "invoices_processed": 67, "null_field_rate": 0.07, "tech_maturity": "high"},
    {"supplier_name": "Cemex", "category": "Construction", "country": "Mexico", "avg_ai_confidence": 76, "invoices_processed": 34, "null_field_rate": 0.22, "tech_maturity": "medium"},
    {"supplier_name": "Amcor", "category": "Packaging", "country": "Australia", "avg_ai_confidence": 84, "invoices_processed": 92, "null_field_rate": 0.11, "tech_maturity": "high"},
    {"supplier_name": "WestRock", "category": "Packaging", "country": "USA", "avg_ai_confidence": 87, "invoices_processed": 105, "null_field_rate": 0.09, "tech_maturity": "high"},
    {"supplier_name": "Evergreen Marine", "category": "Logistics", "country": "Taiwan", "avg_ai_confidence": 90, "invoices_processed": 58, "null_field_rate": 0.06, "tech_maturity": "high"},
    {"supplier_name": "Pou Chen Corp", "category": "Footwear", "country": "Taiwan", "avg_ai_confidence": 78, "invoices_processed": 88, "null_field_rate": 0.15, "tech_maturity": "medium"},
    {"supplier_name": "Yue Yuen Industrial", "category": "Footwear", "country": "Hong Kong", "avg_ai_confidence": 75, "invoices_processed": 76, "null_field_rate": 0.19, "tech_maturity": "medium"},
    {"supplier_name": "Lenzing AG", "category": "Raw Materials", "country": "Austria", "avg_ai_confidence": 83, "invoices_processed": 44, "null_field_rate": 0.13, "tech_maturity": "high"},
    {"supplier_name": "SABIC", "category": "Chemicals", "country": "Saudi Arabia", "avg_ai_confidence": 80, "invoices_processed": 62, "null_field_rate": 0.14, "tech_maturity": "medium"}
]

# Sidebar for selection
with st.sidebar:
    st.header("🔎 Select Supplier")
    supplier_names = [s["supplier_name"] for s in suppliers]
    selected_supplier = st.selectbox("Choose a supplier to analyze:", supplier_names)

    supplier_context = next(
        s for s in suppliers if s["supplier_name"] == selected_supplier
    )
    
    st.markdown("---")
    st.markdown("**Supplier Profile:**")
    st.write(f"📍 **Country:** {supplier_context['country']}")
    st.write(f"🏭 **Category:** {supplier_context['category']}")
    st.write(f"💻 **Tech Maturity:** {supplier_context['tech_maturity'].title()}")

# ---------------- MAIN UI ----------------

# 1. Context Display
st.subheader(f"📊 Analyzing: {selected_supplier}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Invoices Processed", supplier_context['invoices_processed'])
col2.metric("AI Confidence", f"{supplier_context['avg_ai_confidence']}%")
col3.metric("Data Gap Rate", f"{int(supplier_context['null_field_rate']*100)}%")
col4.metric("Tech Maturity", supplier_context['tech_maturity'].title())

st.divider()

# ---------------- AGENT ORCHESTRATION ----------------

if st.button("🚀 Run Intelligence Agents"):
    
    # --- AGENT 1: RISK ASSESSOR ---
    with st.status("🕵️ Agent 1: Assessing Supplier Risk...", expanded=True) as status:
        st.write("Reading supplier history...")
        st.write("Evaluating data quality gaps...")
        
        response_risk = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Supplier Risk Agent. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": f"""
                    Evaluate this supplier:
                    {json.dumps(supplier_context)}

                    Return JSON schema:
                    {{
                      "supplier_tier": "Preferred | Monitor | Enablement Required",
                      "risk_summary": "1 sentence on why",
                      "risk_score": 1-100
                    }}
                    """
                }
            ],
            temperature=0
        )
        risk_result = extract_json_safe(response_risk.choices[0].message.content)
        st.write("✅ Risk Assessment Complete")
        status.update(label="Agent 1: Complete", state="complete", expanded=False)

    # Display Agent 1 Results
    c1, c2 = st.columns([1, 2])
    with c1:
        tier = risk_result.get("supplier_tier", "")
        if tier == "Preferred":
            st.success(f"🌟 **{tier}**")
        elif tier == "Monitor":
            st.warning(f"⚠️ **{tier}**")
        else:
            st.error(f"🚨 **{tier}**")
    with c2:
        st.info(f"**Risk Insight:** {risk_result.get('risk_summary')}")

    # --- AGENT 2: ENABLEMENT SPECIALIST ---
    st.divider()
    
    with st.status("🛠️ Agent 2: Designing Enablement Plan...", expanded=True) as status2:
        st.write("Analyzing pain points based on tech maturity...")
        st.write("Matching resources to risk profile...")
        
        response_enablement = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Supplier Enablement Agent. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": f"""
                    Create an enablement plan for this supplier based on their risk profile.
                    
                    Supplier Context: {json.dumps(supplier_context)}
                    Risk Assessment: {json.dumps(risk_result)}

                    Return JSON schema:
                    {{
                      "pain_points": ["point1", "point2"],
                      "improvement_areas": ["area1", "area2"],
                      "recommended_resources": {{
                        "tool": "AI Agent Assistant | Bulk Upload Tool | API Integration",
                        "support_level": "Self-Serve | Hybrid | Dedicated Human Manager",
                        "action_plan": "1 sentence description"
                      }}
                    }}
                    """
                }
            ],
            temperature=0.3
        )
        enablement_result = extract_json_safe(response_enablement.choices[0].message.content)
        st.write("✅ Plan Generated")
        status2.update(label="Agent 2: Complete", state="complete", expanded=True)

    # Display Agent 2 Results
    st.subheader("🛠️ Recommended Enablement Strategy")
    
    # Card Layout for the Plan
    plan = enablement_result
    res = plan.get("recommended_resources", {})

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 🚩 Pain Points & Improvements")
        for point in plan.get("pain_points", []):
            st.write(f"🔴 {point}")
        for area in plan.get("improvement_areas", []):
            st.write(f"🟢 **Improvement:** {area}")

    with col_b:
        st.markdown("#### 🎁 Resource Package")
        
        # Dynamic Icon based on Support Level
        support = res.get("support_level", "Hybrid")
        icon = "🤖" if "Self" in support else "🤝" if "Hybrid" in support else "👨‍💼"
        
        st.info(f"""
        **Tool:** {res.get('tool')}
        
        **Support:** {icon} {support}
        
        **Action:** {res.get('action_plan')}
        """)

    # Visual "Send" Button
    if st.button(f"📧 Send {res.get('support_level')} Enablement Kit to {selected_supplier}"):
        st.toast(f"Enablement Kit sent to {selected_supplier}!", icon="🚀")
