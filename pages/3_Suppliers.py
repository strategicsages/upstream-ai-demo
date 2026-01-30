import streamlit as st
import pandas as pd
import random

# Set page config for a wider layout
st.set_page_config(page_title="Upstream AI", page_icon="🌍", layout="wide")

st.title("🏭 Supplier Network Scope 3 Data")
st.markdown("Real-time visibility into supplier invoice processing and data confidence.")

# --- 1. DATA INITIALIZATION (SESSION STATE) ---
# We use a function to generate data only once, so we can add to it later
def initialize_data():
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
        # Electronics
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
        # Chemicals
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
        # Steel
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
        # Textiles
        ("Li & Fung", "Hong Kong", "Textiles"),
        ("Shenzhou International", "China", "Textiles"),
        ("Arvind Ltd", "India", "Textiles"),
        ("Welspun India", "India", "Textiles"),
        ("Makalot Industrial", "Taiwan", "Textiles"),
        ("Pou Chen Corp", "Taiwan", "Footwear"),
        ("Gildan Activewear", "Canada", "Apparel"),
        # IT
        ("Infosys", "India", "IT Services"),
        ("TCS", "India", "IT Services"),
        ("Accenture", "Ireland", "Consulting"),
        ("Wipro", "India", "IT Services"),
        ("Cognizant", "USA", "IT Services"),
        ("Capgemini", "France", "Consulting")
    ]

    rows = []
    for supplier, country, category in suppliers_data:
        row = generate_single_supplier_data(supplier, country, category)
        rows.append(row)
    return rows

def generate_single_supplier_data(name, country, category):
    """Helper to generate random metrics for a single supplier"""
    if category == "Logistics":
        invoices = random.randint(15, 120)
        confidence_base = 90 
    elif category == "Textiles":
        invoices = random.randint(5, 40)
        confidence_base = 65 
    else:
        invoices = random.randint(2, 25)
        confidence_base = 85

    variation = random.randint(-30, 10)
    avg_confidence = min(99, max(5, confidence_base + variation))
    reliability_score = random.randint(70, 99)
    
    if avg_confidence > 90: status = "✅ Verified"
    elif avg_confidence > 80: status = "⚠️ Check"
    elif avg_confidence > 10: status = "⚠️ Review"
    else: status = "❌ Failed"

    return {
        "Supplier Name": name,
        "Category": category,
        "Country": country,
        "Invoices Processed": invoices,
        "Avg. AI Confidence": avg_confidence,
        "Data Reliability": reliability_score,
        "Status": status
    }

# Initialize Session State
if "supplier_data" not in st.session_state:
    st.session_state.supplier_data = initialize_data()

# --- 2. SIDEBAR CONTROLS (Add, Search, Filter) ---
with st.sidebar:
    st.title("🛠️ Controls")
    
    # A. Add Supplier Form
    with st.expander("➕ Add New Supplier", expanded=False):
        with st.form("add_supplier_form"):
            new_name = st.text_input("Supplier Name")
            new_country = st.text_input("Country")
            new_category = st.selectbox("Category", [
                "Logistics", "Textiles", "Electronics", "Chemicals", 
                "Steel", "Packaging", "IT Services", "Other"
            ])
            submit_btn = st.form_submit_button("Add Supplier")
            
            if submit_btn and new_name and new_country:
                new_row = generate_single_supplier_data(new_name, new_country, new_category)
                st.session_state.supplier_data.insert(0, new_row) # Add to top
                st.success(f"Added {new_name}!")
                st.rerun()

    st.divider()
    
    # B. Filters
    st.subheader("🔍 Search & Filter")
    
    # Convert state to DF for filtering options
    base_df = pd.DataFrame(st.session_state.supplier_data)
    
    # Search
    search_query = st.text_input("Search by Name", placeholder="e.g. Maersk")
    
    # Filter Categories
    all_countries = sorted(base_df['Country'].unique())
    all_categories = sorted(base_df['Category'].unique())
    
    selected_countries = st.multiselect("Filter Country", all_countries)
    selected_categories = st.multiselect("Filter Category", all_categories)
    
    # Filter Score
    min_score = st.slider("Min AI Confidence %", 0, 100, 0)

# --- 3. FILTERING LOGIC ---
df = pd.DataFrame(st.session_state.supplier_data)

# Apply Search
if search_query:
    df = df[df["Supplier Name"].str.contains(search_query, case=False)]

# Apply Filters
if selected_countries:
    df = df[df["Country"].isin(selected_countries)]

if selected_categories:
    df = df[df["Category"].isin(selected_categories)]

df = df[df["Avg. AI Confidence"] >= min_score]

# --- 4. METRICS (Based on Filtered Data) ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Visible Suppliers", len(df))
c2.metric("Invoices (Visible)", df["Invoices Processed"].sum() if not df.empty else 0)
avg_rel = int(df['Data Reliability'].mean()) if not df.empty else 0
c3.metric("Avg Reliability", f"{avg_rel}/100")
st.divider()

# --- 5. PAGINATION ---
if "page_number" not in st.session_state:
    st.session_state.page_number = 0

rows_per_page = 12
if len(df) > 0:
    last_page = max(0, (len(df) - 1) // rows_per_page)
else:
    last_page = 0

# Reset page if out of bounds (e.g. after filtering)
if st.session_state.page_number > last_page:
    st.session_state.page_number = 0

start_idx = st.session_state.page_number * rows_per_page
end_idx = start_idx + rows_per_page

# Pagination Controls
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

# --- 6. DISPLAY WITH CONDITIONAL FORMATTING ---
def color_confidence(val):
    if val > 90:
        return 'background-color: #d1e7dd; color: #0f5132' # Green
    elif val > 80:
        return 'background-color: #fff3cd; color: #664d03' # Yellow
    elif val > 10:
        return 'background-color: white; color: black'     # Neutral
    else:
        return 'background-color: #f8d7da; color: #842029' # Red

if not paginated_df.empty:
    styled_df = paginated_df.style.map(color_confidence, subset=["Avg. AI Confidence"])

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
else:
    st.info("No suppliers found matching your filters.")
