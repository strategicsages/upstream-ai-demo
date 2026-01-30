import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Upstream AI Command Center", page_icon="📊", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 8px;
        color: black;
    }
    div[data-testid="metric-container"] label {
        color: #6c757d; 
    }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA INITIALIZATION (The "Glue") ----------------
def init_data():
    """Generates cohesive mock data linking Suppliers, Invoices, and Risk"""
    if "dashboard_data" not in st.session_state:
        
        # 1. Suppliers (The Entities)
        suppliers = [
            {"name": "Maersk Line", "country": "Denmark", "risk": "Preferred", "maturity": "High"},
            {"name": "Arvind Ltd", "country": "India", "risk": "Enablement Required", "maturity": "Low"},
            {"name": "Foxconn Tech", "country": "Taiwan", "risk": "Monitor", "maturity": "High"},
            {"name": "Viet Textile Co", "country": "Vietnam", "risk": "Enablement Required", "maturity": "Low"},
            {"name": "DHL Supply Chain", "country": "Germany", "risk": "Preferred", "maturity": "High"},
            {"name": "Tata Steel", "country": "India", "risk": "Monitor", "maturity": "Medium"},
            {"name": "Shenzhou Intl", "country": "China", "risk": "Monitor", "maturity": "Medium"},
            {"name": "BASF SE", "country": "Germany", "risk": "Preferred", "maturity": "High"},
        ]
        
        # 2. Invoices (The Activity)
        invoices = []
        today = datetime.now()
        for s in suppliers:
            # Generate random invoice count based on maturity
            count = random.randint(5, 50) if s["maturity"] == "High" else random.randint(1, 10)
            base_conf = 95 if s["maturity"] == "High" else 65
            
            for _ in range(count):
                date_offset = random.randint(0, 30)
                inv_date = today - timedelta(days=date_offset)
                
                # Confidence fluctuation
                conf = min(100, max(40, base_conf + random.randint(-15, 5)))
                
                invoices.append({
                    "supplier": s["name"],
                    "date": inv_date.strftime("%Y-%m-%d"),
                    "amount": random.uniform(1000, 50000),
                    "confidence": conf,
                    "kwh": random.uniform(500, 10000),
                    "status": "Processed" if conf > 80 else "Human Review"
                })
        
        st.session_state.dashboard_data = {
            "suppliers": pd.DataFrame(suppliers),
            "invoices": pd.DataFrame(invoices)
        }

init_data()

df_suppliers = st.session_state.dashboard_data["suppliers"]
df_invoices = st.session_state.dashboard_data["invoices"]

# ---------------- HEADER ----------------
c1, c2 = st.columns([3, 1])
with c1:
    st.title("📊 Upstream AI Command Center")
    st.caption(f"System Status: ● Online | Last Sync: {datetime.now().strftime('%H:%M:%S')}")
with c2:
    # Mock Date Filter
    st.selectbox("Time Range", ["Last 30 Days", "Last Quarter", "Year to Date"])

st.divider()

# ---------------- TOP METRICS (KPIs) ----------------
# Calculating live metrics
total_suppliers = len(df_suppliers)
total_invoices = len(df_invoices)
avg_confidence = int(df_invoices["confidence"].mean())
total_carbon = int(df_invoices["kwh"].sum() * 0.45 / 1000) # Mock factor 0.45 kg/kWh -> Metric Tons
at_risk = len(df_suppliers[df_suppliers["risk"] == "Enablement Required"])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Active Suppliers", total_suppliers, "+2 this week")
m2.metric("Invoices Ingested", total_invoices, "+12% vs last mo")
m3.metric("Data Confidence", f"{avg_confidence}%", "Target: 90%")
m4.metric("Carbon Tracked (tCO2e)", f"{total_carbon} t", "Scope 3")
m5.metric("Suppliers 'At Risk'", at_risk, delta="-1", delta_color="inverse")

st.markdown("###") # Spacer

# ---------------- CHARTS ROW ----------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Ingestion Velocity & Quality")
    
    # Aggregate data for chart
    df_chart = df_invoices.groupby("date")[["amount"]].count().reset_index()
    df_chart.columns = ["Date", "Count"]
    
    # Dual axis concept (Volume vs Confidence) - Simplified to stacked bar for demo
    fig_bar = px.bar(
        df_chart, x="Date", y="Count", 
        title="Daily Invoice Volume",
        template="plotly_white",
        color_discrete_sequence=["#007bff"]
    )
    fig_bar.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("🛡️ Supply Chain Risk")
    
    # Donut Chart for Supplier Tiers
    risk_counts = df_suppliers["risk"].value_counts().reset_index()
    risk_counts.columns = ["Risk Tier", "Count"]
    
    color_map = {
        "Preferred": "#28a745", 
        "Monitor": "#ffc107", 
        "Enablement Required": "#dc3545"
    }
    
    fig_donut = px.pie(
        risk_counts, values="Count", names="Risk Tier",
        color="Risk Tier", color_discrete_map=color_map,
        hole=0.5
    )
    fig_donut.update_layout(
        height=350, 
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ---------------- INTELLIGENCE & ALERTS ROW ----------------
st.divider()

c_alert, c_feed = st.columns([1, 1])

with c_alert:
    st.subheader("🚨 Priority Actions (Human-in-the-Loop)")
    
    # Filter for low confidence invoices
    low_conf = df_invoices[df_invoices["confidence"] < 75].sort_values("date", ascending=False).head(5)
    
    if not low_conf.empty:
        for _, row in low_conf.iterrows():
            with st.container():
                ac1, ac2, ac3 = st.columns([0.1, 0.7, 0.2])
                with ac1:
                    st.write("⚠️")
                with ac2:
                    st.markdown(f"**{row['supplier']}** - Low Confidence ({int(row['confidence'])}%)")
                    st.caption(f"Invoice Date: {row['date']} | Missing Fields: Fuel Type")
                with ac3:
                    st.button("Review", key=f"btn_{row['supplier']}_{random.randint(0,1000)}")
                st.markdown("---")
    else:
        st.success("🎉 No active alerts. System healthy.")

with c_feed:
    st.subheader("🧠 Supplier Intelligence Feed")
    
    # Mock Feed of Agent Actions
    activities = [
        {"icon": "🤖", "msg": "Agent 2 auto-enrolled **Viet Textile Co** in 'Basic Digital Training'", "time": "2 mins ago"},
        {"icon": "✅", "msg": "Agent 1 verified **Maersk Line** Q3 data packet (100% match)", "time": "15 mins ago"},
        {"icon": "📥", "msg": "Ingested 12 new invoices from **Foxconn Tech** via API", "time": "1 hour ago"},
        {"icon": "📉", "msg": "Detected -15% emission drop for **DHL Supply Chain** (Year-over-Year)", "time": "3 hours ago"},
    ]
    
    for act in activities:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px; padding: 10px; background: white; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
            <div style="font-size: 20px; margin-right: 15px;">{act['icon']}</div>
            <div>
                <div style="font-size: 14px;">{act['msg']}</div>
                <div style="font-size: 12px; color: #888;">{act['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- SUPPLIER TABLE ----------------
st.subheader("📦 Network Performance Summary")

# Create a joined view (Supplier + Aggregated Invoice Stats)
# Calculate avg confidence per supplier
stats = df_invoices.groupby("supplier")[["confidence", "amount"]].mean().reset_index()
stats.columns = ["name", "avg_conf", "avg_amt"]

# Merge with supplier profile
full_view = pd.merge(df_suppliers, stats, on="name", how="left").fillna(0)

# Display styled table
def highlight_risk(val):
    if val == "Preferred": return "background-color: #d4edda; color: #155724; font-weight: bold"
    if val == "Monitor": return "background-color: #fff3cd; color: #856404; font-weight: bold"
    return "background-color: #f8d7da; color: #721c24; font-weight: bold"

st.dataframe(
    full_view.style.map(highlight_risk, subset=["risk"]),
    column_config={
        "name": "Supplier Name",
        "country": "Region",
        "risk": "Risk Tier",
        "maturity": "Tech Maturity",
        "avg_conf": st.column_config.ProgressColumn("Avg Data Quality", min_value=0, max_value=100, format="%d%%"),
        "avg_amt": st.column_config.NumberColumn("Avg Invoice Value", format="$%.2f")
    },
    use_container_width=True,
    hide_index=True
)
