import streamlit as st

# -------------------------------------------------
# Page Config (MUST be first Streamlit call)
# -------------------------------------------------
st.set_page_config(
    page_title="Upstream AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Sidebar: Branding (TOP)
# -------------------------------------------------
st.sidebar.markdown(
    """
    <div style="padding-bottom: 12px;">
        <h2 style="margin-bottom: 0;">🌍 Upstream AI</h2>
        <small style="color: #666;">
            Agentic Scope 3 Intelligence Platform
        </small>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# -------------------------------------------------
# Main Page Content (Welcome Shell)
# -------------------------------------------------
st.title("Welcome to Upstream AI")

st.markdown(
    """
    **Upstream AI transforms messy supplier documents into trusted, audit-ready  
    Scope 3 emissions intelligence.**
    """
)

st.info(
    "Use the sidebar to navigate through the platform. "
    "Start with the **Dashboard** to see live supplier intelligence."
)

# -------------------------------------------------
# Context Section (Exec-friendly framing)
# -------------------------------------------------
st.markdown("### Why this matters")

st.markdown(
    """
    - **Scope 3 emissions account for up to 90% of a company’s carbon footprint**
    - Data lives outside the enterprise — across suppliers, invoices, emails, PDFs, and photos
    - Manual collection is slow, unreliable, and non-compliant with emerging regulations  
      (e.g. **SB 253, CSRD**)
    """
)

st.markdown(
    """
    **Upstream AI sits upstream of ESG platforms and ERPs —  
    turning chaotic supplier data into clean, structured intelligence.**
    """
)

st.markdown("---")

# -------------------------------------------------
# Sidebar: Utilities (BOTTOM – simulated footer)
# -------------------------------------------------
st.sidebar.markdown(
    """
    <hr style="margin-top: 40px;">
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("### ⚙️ Utilities")

    # These are intentionally disabled for demo honesty
    st.button("👤 Profile", disabled=True, help="User profile & access controls")
    st.button("🛠 Settings", disabled=True, help="Integrations, thresholds, preferences")
    st.button("📜 Audit Logs", disabled=True, help="Full traceability for compliance")

