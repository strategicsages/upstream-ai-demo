import streamlit as st

st.set_page_config(
    page_title="Upstream AI",
    page_icon="🌍",
    layout="wide"
)

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("### 🌍 Upstream AI")
    st.caption("Agentic Scope 3 Intelligence Platform")
    st.divider()

    # Spacer to push utilities to bottom
    st.markdown(
        """
        <div style="flex:1; height: 65vh;"></div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("### ⚙️ Utilities")

    st.button("👤 Profile", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)
    st.button("📜 Audit Logs", use_container_width=True)

# --- MAIN LANDING CONTENT ---
st.title("Welcome to Upstream AI")
st.caption(
    "Transform messy supplier documents into trusted, audit-ready Scope 3 intelligence."
)

st.info("Use the sidebar to navigate through the platform.")
