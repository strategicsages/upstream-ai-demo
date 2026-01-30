import streamlit as st
import pandas as pd
import random
import time
if "suppliers_df" not in st.session_state:
    st.session_state.suppliers_df = df.copy()
# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Supplier Intelligence", layout="wide")

st.title("🧠 Supplier Intelligence")
st.caption("Agent-driven supplier enablement and data quality improvement")

st.divider()

# ---------------- SUPPLIER DATA ----------------
suppliers_data = [
    ("Arvind Ltd", "India", "Textiles"),
    ("Li & Fung", "Hong Kong", "Textiles"),
    ("Tata Steel", "India", "Steel"),
    ("Maersk Line", "Denmark", "Logistics"),
    ("Foxconn", "Taiwan", "Electronics"),
    ("BASF SE", "Germany", "Chemicals"),
]

rows = []
for name, country, category in suppliers_data:
    confidence = random.randint(55, 95)
    invoices = random.randint(5, 60)

    rows.append({
        "Supplier Name": name,
        "Country": country,
        "Category": category,
        "Invoices Processed": invoices,
        "Avg. AI Confidence": confidence
    })

df = pd.DataFrame(rows)

# ---------------- AGENT LOGIC ----------------
def supplier_enablement_agent(supplier):
    confidence = supplier["Avg. AI Confidence"]

    if confidence < 70:
        return {
            "Supplier Maturity": "Low",
            "Recommended Path": "Hybrid (AI + Human)",
            "Diagnosis": "Low-quality submissions and inconsistent formats",
            "AI Actions": [
                "Invoice templates",
                "Mobile-friendly submission guide"
            ],
            "Human Actions": [
                "Onboarding call",
                "Data readiness training"
            ],
            "Expected Confidence Uplift": "+15–20%"
        }

    elif confidence < 85:
        return {
            "Supplier Maturity": "Medium",
            "Recommended Path": "AI-led Enablement",
            "Diagnosis": "Partially structured but inconsistent",
            "AI Actions": [
                "Automated validation tips",
                "Confidence feedback loop"
            ],
            "Human Actions": [],
            "Expected Confidence Uplift": "+8–12%"
        }

    else:
        return {
            "Supplier Maturity": "High",
            "Recommended Path": "Monitor Only",
            "Diagnosis": "Reliable and consistent data",
            "AI Actions": ["No action required"],
            "Human Actions": [],
            "Expected Confidence Uplift": "+2–3%"
        }

# ---------------- UI ----------------
st.subheader("Supplier Network Overview")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("🧠 Run Supplier Enablement Agent")

selected_supplier = st.selectbox(
    "Select a supplier",
    df["Supplier Name"]
)

if st.button("Run Enablement Agent"):
    supplier_row = df[df["Supplier Name"] == selected_supplier].iloc[0]

    with st.spinner("Agent reasoning about supplier capability..."):
        time.sleep(1.5)
        result = supplier_enablement_agent(supplier_row)

    st.success("Agent recommendation ready")
    st.json(result)
