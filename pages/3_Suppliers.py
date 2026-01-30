import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🏭 Supplier Network")
st.caption("Operational view of Scope 3 supplier data quality")

df = st.session_state.suppliers_df

# --- Metrics ---
c1, c2, c3 = st.columns(3)
c1.metric("Suppliers", len(df))
c2.metric("Invoices Processed", df["Invoices Processed"].sum())
c3.metric("Avg Reliability", f"{int(df['Data Reliability'].mean())}/100")

st.divider()

# --- Pagination ---
rows_per_page = 12
page = st.session_state.get("supplier_page", 0)
max_page = (len(df) - 1) // rows_per_page

start = page * rows_per_page
end = start + rows_per_page
page_df = df.iloc[start:end]

# --- Styling ---
def color_conf(val):
    if val > 90:
        return "background-color:#d1e7dd"
    elif val > 80:
        return "background-color:#fff3cd"
    else:
        return "background-color:#f8d7da"

styled = page_df.style.map(color_conf, subset=["Avg. AI Confidence"])

st.dataframe(styled, use_container_width=True, hide_index=True)

col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.button("⬅ Prev", disabled=page == 0, on_click=lambda: st.session_state.update({"supplier_page": page-1}))
with col3:
    st.button("Next ➡", disabled=page == max_page, on_click=lambda: st.session_state.update({"supplier_page": page+1}))

# --- Add Supplier ---
with st.expander("➕ Add Supplier"):
    name = st.text_input("Supplier Name")
    cat = st.selectbox("Category", df["Category"].unique())
    country = st.text_input("Country")

    if st.button("Add Supplier"):
        st.session_state.suppliers_df = pd.concat([
            df,
            pd.DataFrame([{
                "Supplier Name": name,
                "Category": cat,
                "Country": country,
                "Invoices Processed": 0,
                "Avg. AI Confidence": 0,
                "Data Reliability": 0,
                "Status": "⚠️ New"
            }])
        ], ignore_index=True)
        st.success("Supplier onboarded")
