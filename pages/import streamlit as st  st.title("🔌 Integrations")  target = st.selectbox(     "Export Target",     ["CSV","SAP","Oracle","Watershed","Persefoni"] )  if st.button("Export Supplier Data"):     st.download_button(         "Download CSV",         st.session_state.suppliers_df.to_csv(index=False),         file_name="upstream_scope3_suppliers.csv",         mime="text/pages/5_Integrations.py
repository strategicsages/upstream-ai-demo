import streamlit as st

st.title("🔌 Integrations")

target = st.selectbox(
    "Export Target",
    ["CSV","SAP","Oracle","Watershed","Persefoni"]
)

if st.button("Export Supplier Data"):
    st.download_button(
        "Download CSV",
        st.session_state.suppliers_df.to_csv(index=False),
        file_name="upstream_scope3_suppliers.csv",
        mime="text/csv"
    )

st.info("Upstream AI acts as a Scope 3 data provider, not a reporting tool.")
