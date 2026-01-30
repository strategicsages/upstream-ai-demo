import streamlit as st
import pandas as pd
import random

# Set page config for a wider layout
st.set_page_config(page_title="VeroFlow: Supplier Network", page_icon="🏭", layout="wide")

st.title("🏭 Supplier Network Scope 3 Data")
st.markdown("Real-time visibility into supplier invoice processing and data confidence.")

# --- 1. DATA GENERATION (Moved to top) ---
# List of 60 Real-world Suppliers (Logistics, Manufacturing, Raw Materials, Services)
suppliers_data = [
    # Logistics & Shipping (Cat 4/9)
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

    # Electronics & Components (Cat 1)
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

    # Chemicals & Raw Materials (Cat 1)
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

    # Steel & Metals (Cat 1)
    ("Tata Steel", "India", "Steel"),
    ("ArcelorMittal", "Luxembourg", "Steel"),
    ("Nippon Steel", "Japan", "Steel"),
    ("POSCO", "South Korea", "Steel"),
    ("Baowu Group", "China", "Steel"),

    # Packaging (Cat 1)
    ("Amcor", "Australia", "Packaging"),
    ("Ball Corporation", "USA", "Packaging"),
    ("Smurfit Kappa", "Ireland", "Packaging"),
    ("WestRock", "USA", "Packaging"),
    ("International Paper", "USA", "Packaging"),
    ("Avery Dennison", "USA", "Packaging"),

    # Textiles & Apparel (Cat 1)
    ("Li & Fung", "Hong Kong", "Textiles"),
    ("Shenzhou International", "China", "Textiles"),
    ("Arvind Ltd", "India", "Textiles"),
    ("Welspun India", "India", "Textiles"),
    ("Makalot Industrial", "Taiwan", "Textiles"),
    ("Pou Chen Corp", "Taiwan", "Footwear"),
    ("Gildan Activewear", "Canada", "Apparel"),

    # IT & Business Services (Cat 1 - Purchased Services)
    ("Infosys", "India", "IT Services"),
    ("TCS", "India", "IT Services"),
    ("Accenture", "Ireland", "Consulting"),
    ("Wipro", "India", "IT Services"),
    ("Cognizant", "USA", "IT Services"),
    ("Capgemini", "France", "Consulting")
]

# Generate realistic mock data for the table
table_rows = []

# Seed for reproducibility if needed, though random varies the demo nicely
# random.seed(42) 

for supplier, country, category in suppliers_data:
    # Randomize invoice counts based on category (Logistics usually has high volume)
    if category == "Logistics":
        invoices = random.randint(15, 120)
        confidence_base = 90 # Standardized forms usually
    elif category == "Textiles":
        invoices = random.randint(5, 40)
        confidence_base = 75 # Messier invoices
    else:
        invoices = random.randint(2, 25)
        confidence_base = 85

    # Simulate variations
    avg_confidence = min(99, max(60, confidence_base + random.randint(-10, 8)))
    reliability_score = random.randint(70, 99)
    
    # Formatting status
    if avg_confidence > 90:
        status = "✅ High"
    elif avg_confidence > 75:
        status = "⚠️ Medium"
    else:
        status = "❌ Review Needed"

    table_rows.append({
        "Supplier Name": supplier,
        "Category": category,
        "Country": country,
        "Invoices Processed": invoices,
        "Avg. AI Confidence": avg_confidence, # Keep as int for math
        "Data Reliability": reliability_score,
        "Status": status
    })

# Create DataFrame
df = pd.DataFrame(table_rows)

# --- 2. METRICS DISPLAY (Moved Up) ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Total Suppliers Tracked", len(df))
c2.metric("Total Invoices Processed", df["Invoices Processed"].sum())
c3.metric("Avg Network Reliability", f"{int(df['Data Reliability'].mean())}/100")
st.divider()

# --- 3. PAGINATION LOGIC ---
if "page_number" not in st.session_state:
    st.session_state.page_number = 0

rows_per_page = 12
last_page = (len(df) - 1) // rows_per_page

# Calculate start and end indices for the current page
start_idx = st.session_state.page_number * rows_per_page
end_idx = start_idx + rows_per_page

# Display Pagination Controls
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

# Slice the dataframe based on pagination
paginated_df = df.iloc[start_idx:end_idx]

# --- 4. TABLE DISPLAY ---
st.dataframe(
    paginated_df,
    column_config={
        "Avg. AI Confidence": st.column_config.ProgressColumn(
            "AI Confidence",
            help="Average confidence of AI extraction",
            format="%d%%", # Add % formatting here
            min_value=0,
            max_value=100,
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
