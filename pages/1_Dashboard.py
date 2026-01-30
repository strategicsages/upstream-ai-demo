import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Upstream AI – System Overview")

df = st.session_state.get("suppliers_df")

if df is None:
    st.info("Waiting for supplier data…")
    st.stop()

# ------------------ TOP METRICS ------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Suppliers Tracked", len(df))
c2.metric("Invoices Processed", int(df["Invoices Processed"].sum()))
c3.metric("Avg AI Confidence", f"{int(df['Avg. AI Confidence'].mean())}%")
c4.metric(
    "Suppliers at Risk",
    int((df["Avg. AI Confidence"] < 75).sum())
)

st.divider()

# ------------------ LIVE SYSTEM FEED ------------------
st.subheader("🔁 Live System Activity")

st.markdown("""
- 📤 **Upload Invoice** updates supplier confidence in real time  
- 🧠 **Supplier Intelligence** activates below confidence thresholds  
- 📊 **Dashboard** reflects network health instantly  
- 🔗 **Integrations** export structured Scope 3 data downstream
""")

st.divider()

# ------------------ ALERTS ------------------
st.subheader("⚠️ Active Alerts")

low = df[df["Avg. AI Confidence"] < 75]

if low.empty:
    st.success("No suppliers require intervention")
else:
    for _, s in low.iterrows():
        st.warning(
            f"{s['Supplier Name']} – Confidence {s['Avg. AI Confidence']}%"
        )

st.divider()

# ------------------ RECENT SUPPLIERS ------------------
st.subheader("📦 Recently Updated Suppliers")
st.dataframe(
    df.sort_values("Invoices Processed", ascending=False)
      .head(8)[
        ["Supplier Name", "Invoices Processed", "Avg. AI Confidence", "Status"]
      ],
    use_container_width=True
)
