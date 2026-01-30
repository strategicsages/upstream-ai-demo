import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Upstream AI | Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------------------------
# MOCK SUPPLIER NETWORK (MATCHES Suppliers.py LOGIC)
# -------------------------------------------------
def generate_supplier_network():
    suppliers = [
        ("Maersk Line", "Logistics", 90),
        ("DHL Supply Chain", "Logistics", 88),
        ("FedEx Logistics", "Logistics", 92),
        ("Foxconn", "Electronics", 78),
        ("TSMC", "Semiconductors", 95),
        ("Samsung Electronics", "Components", 91),
        ("BASF", "Chemicals", 86),
        ("Dow Chemical", "Chemicals", 83),
        ("Tata Steel", "Steel", 80),
        ("ArcelorMittal", "Steel", 84),
    ]

    rows = []
    for name, category, base_conf in suppliers:
        invoices = random.randint(5, 120)
        confidence = max(5, min(99, base_conf + random.randint(-12, 8)))

        if confidence > 90:
            status = "Verified"
        elif confidence > 80:
            status = "Check"
        else:
            status = "Review"

        rows.append({
            "Supplier": name,
            "Category": category,
            "Invoices": invoices,
            "AI Confidence": confidence,
            "Status": status
        })

    return pd.DataFrame(rows)

df = generate_supplier_network()

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("Upstream AI — Supplier Intelligence Dashboard")
st.caption("Live operational view of supplier data quality, processing health, and risk signals")

st.divider()

# -------------------------------------------------
# NETWORK HEALTH METRICS
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Suppliers Tracked",
    len(df)
)

c2.metric(
    "Invoices Processed",
    f"{df['Invoices'].sum():,}"
)

c3.metric(
    "Suppliers Requiring Review",
    len(df[df["Status"] == "Review"])
)

c4.metric(
    "Avg Network AI Confidence",
    f"{int(df['AI Confidence'].mean())}%"
)

st.divider()

# -------------------------------------------------
# RISK & ATTENTION PANEL
# -------------------------------------------------
st.subheader("⚠️ Suppliers Needing Attention")

risk_df = df[df["Status"] != "Verified"] \
    .sort_values(by=["AI Confidence", "Invoices"], ascending=[True, False]) \
    .head(5)

if risk_df.empty:
    st.success("All suppliers are operating within acceptable confidence thresholds.")
else:
    st.dataframe(
        risk_df[["Supplier", "Category", "Invoices", "AI Confidence", "Status"]],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -------------------------------------------------
# RECENT SYSTEM ACTIVITY (SIMULATED AUDIT FEED)
# -------------------------------------------------
st.subheader("🧾 Recent System Activity")

activity = [
    ("Invoice uploaded", "DHL Supply Chain"),
    ("Manual review triggered", "Foxconn"),
    ("Invoice processed successfully", "TSMC"),
    ("Low confidence detected", "Tata Steel"),
    ("Supplier score updated", "BASF"),
]

activity_rows = []
for action, supplier in activity:
    activity_rows.append({
        "Time": (datetime.now() - timedelta(minutes=random.randint(2, 90))).strftime("%H:%M"),
        "Event": action,
        "Supplier": supplier
    })

activity_df = pd.DataFrame(activity_rows)

st.dataframe(
    activity_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------
# GUIDED NEXT ACTIONS
# -------------------------------------------------
st.subheader("🚀 What would you like to do next?")

a1, a2, a3 = st.columns(3)

with a1:
    st.button("📤 Upload New Invoice", use_container_width=True)

with a2:
    st.button("🏭 Review Suppliers", use_container_width=True)

with a3:
    st.button("📊 Open Supplier Intelligence", use_container_width=True)
