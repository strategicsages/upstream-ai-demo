import streamlit as st
import pandas as pd
import random
if "suppliers_df" not in st.session_state:
    st.session_state.suppliers_df = df.copy()
# Set page config for a wider layout
st.set_page_config(page_title="Upstream AI", page_icon="🌍", layout="wide")

st.title("🏭 Supplier Network Scope 3 Data")
st.markdown("Real-time visibility into supplier invoice processing and data confidence.")

# --- 1. DATA GENERATION ---
# List of 60 Real-world Suppliers
suppliers_data = [
    # Logistics & Shipping
    ("Maersk Line", "Denmark", "Logistics"),
    ("DHL Supply Chain", "Germany", "Logistics"),
    ("FedEx Logistics", "USA", "Logistics"),
    ("Nippon Express", "Japan", "Logistics"),
    ("DB Schenker", "Germany", "Logistics"),
    ("Kuehne + Nagel", "Switzerland", "Logistics"),
    ("C.H. Robinson", "USA", "Logistics"),
    ("XPO Logistics", "USA", "Logistics"),
    ("DSV Panalpina", "Denmark", "Logistics"),
    ("Sinotrans", "China", "Logistics"),
    ("Hapag-Lloyd", "Germany", "Logistics"),
    ("MSC Mediterranean Shipping", "Switzerland", "Logistics"),
    ("CMA CGM", "France", "Logistics"),
    ("COSCO Shipping", "China", "Logistics"),
    ("Evergreen Marine", "Taiwan", "Logistics"),

    # Electronics & Components
    ("Foxconn Technology Group", "Taiwan", "Electronics"),
    ("Flex Ltd", "Singapore", "Electronics"),
    ("Jabil Inc", "USA", "Electronics"),
    ("TSMC", "Taiwan", "Semiconductors"),
    ("Samsung Electronics", "South Korea", "Components"),
    ("LG Chem", "South Korea", "Batteries"),
    ("CATL", "China", "Batteries"),
    ("SK Hynix", "South Korea", "Semiconductors"),
    ("Micron Technology", "USA", "Semiconductors"),
    ("Intel Corp", "USA", "Semiconductors"),

    # Chemicals & Raw Materials
    ("BASF SE", "Germany", "Chemicals"),
    ("Dow Chemical", "USA", "Chemicals"),
    ("Sinopec", "China", "Chemicals"),
    ("SABIC", "Saudi Arabia", "Chemicals"),
    ("LyondellBasell", "Netherlands", "Chemicals"),
    ("Rio Tinto", "UK/Australia", "Mining"),
    ("BHP", "Australia", "Mining"),
    ("Vale", "Brazil", "Mining"),
    ("Glencore", "Switzerland", "Commodities"),
    ("Cargill", "USA", "Agriculture"),

    # Steel & Metals
    ("Tata Steel", "India", "Steel"),
    ("ArcelorMittal", "Luxembourg", "Steel"),
    ("Nippon Steel", "Japan", "Steel"),
    ("POSCO", "South Korea", "Steel"),
    ("Baowu Group", "China", "Steel"),

    # Packaging
    ("Amcor", "Australia", "Packaging"),
    ("Ball Corporation", "USA", "Packaging"),
    ("Smurfit Kappa", "Ireland", "Packaging"),
    ("WestRock", "USA", "Packaging"),
    ("International Paper", "USA", "Packaging"),
    ("Avery Dennison", "USA", "Packaging"),

    # Textiles & Apparel
    ("Li & Fung", "Hong Kong", "Textiles"),
    ("Shenzhou International", "China", "Textiles"),
    ("Arvind Ltd", "India", "Textiles"),
    ("Welspun India", "India", "Textiles"),
    ("Makalot Industrial", "Taiwan", "Textiles"),
    ("Pou Chen Corp", "Taiwan", "Footwear"),
    ("Gildan Activewear", "Canada", "Apparel"),

    # IT & Business Services
    ("Infosys", "India", "IT Services"),
    ("TCS", "India", "IT Services"),
    ("Accenture", "Ireland", "Consulting"),
    ("Wipro", "India", "IT Services"),
    ("Cognizant", "USA", "IT Services"),
    ("Capgemini", "France", "Consulting")
]

# Generate realistic mock data
table_rows = []

for supplier, country, category in suppliers_data:
    if category == "Logistics":
        invoices = random.randint(15, 120)
        confidence_base = 90 
    elif category == "Textiles":
        invoices = random.randint(5, 40)
        confidence_base = 65 # Lower base to trigger red/yellow more often
    else:
        invoices = random.randint(2, 25)
        confidence_base = 85

    # Simulate wider variations to show off the color logic (0-100 range)
    # Using a wider random spread
    variation = random.randint(-30, 10)
    avg_confidence = min(99, max(5, confidence_base + variation))
    
    reliability_score = random.randint(70, 99)
    
    # Status Logic
    if avg_confidence > 90:
        status = "✅ Verified"
    elif avg_confidence > 80:
        status = "⚠️ Check"
    elif avg_confidence > 10:
        status = "⚠️ Review"
    else:
        status = "❌ Failed"

    table_rows.append({
        "Supplier Name": supplier,
        "Category": category,
        "Country": country,
        "Invoices Processed": invoices,
        "Avg. AI Confidence": avg_confidence,
        "Data Reliability": reliability_score,
        "Status": status
    })

df = pd.DataFrame(table_rows)

# --- 2. METRICS ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Total Suppliers Tracked", len(df))
c2.metric("Total Invoices Processed", df["Invoices Processed"].sum())
c3.metric("Avg Network Reliability", f"{int(df['Data Reliability'].mean())}/100")
st.divider()

# --- 3. PAGINATION ---
if "page_number" not in st.session_state:
    st.session_state.page_number = 0

rows_per_page = 12
last_page = (len(df) - 1) // rows_per_page

start_idx = st.session_state.page_number * rows_per_page
end_idx = start_idx + rows_per_page

col_prev, col_info, col_next = st.columns([1, 2, 1])

def next_page():
    if st.session_state.page_number < last_page:
        st.session_state.page_number += 1

def prev_page():
    if st.session_state.page_number > 0:
        st.session_state.page_number -= 1

with col_prev:
    st.button("Previous", on_click=prev_page, disabled=(st.session_state.page_number == 0))

with col_next:
    st.button("Next", on_click=next_page, disabled=(st.session_state.page_number == last_page))

with col_info:
    st.markdown(f"**Page {st.session_state.page_number + 1} of {last_page + 1}**")

# Get current page data
paginated_df = df.iloc[start_idx:end_idx]

# --- 4. CONDITIONAL FORMATTING FUNCTION ---
def color_confidence(val):
    """
    Green > 90
    Light Green 80-90
    Light/White 10-80
    Red Hues < 10
    """
    if val > 90:
        return 'background-color: #d1e7dd; color: #0f5132' # Bootstrap Success Green
    elif val > 80:
        return 'background-color: #fff3cd; color: #664d03' # Using Yellowish/Light Green tone
    elif val > 10:
        return 'background-color: white; color: black'     # Neutral
    else:
        return 'background-color: #f8d7da; color: #842029' # Bootstrap Danger Red

# Apply styling to the specific column
styled_df = paginated_df.style.map(color_confidence, subset=["Avg. AI Confidence"])

# --- 5. TABLE DISPLAY ---
st.dataframe(
    styled_df,
    column_config={
        "Avg. AI Confidence": st.column_config.NumberColumn(
            "AI Confidence (%)",
            format="%d%%"
        ),
        "Data Reliability": st.column_config.NumberColumn(
            "Reliability Score",
            help="Supplier responsiveness score (0-100)",
            format="%d"
        ),
    },
    hide_index=True,
    use_container_width=True
)
