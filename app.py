import streamlit as st
from auth import login_page, signup_page
from pages.logistics import logistics_page
from pages.historical_data import historical_data_page
from pages.transactional_ai import transactional_ai_page
from pages.forecasting_energy import forecasting_energy_page  # ✅ NEW: Import Forecasting Page

# Set page title, icon, layout
st.set_page_config(
    page_title="Grid AI",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar starts collapsed
)

# Ensure session state for tracking authentication and navigation
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Enter Historical Data"  # Default landing page after login

# 🛑 **Hide Sidebar for Login/Signup Page**
if not st.session_state["authenticated"]:
    hide_sidebar_style = """
        <style>
        [data-testid="stSidebarNav"], header {display: none;}  /* Hide sidebar + Streamlit header */
        </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    # Show Login/Signup Page
    st.title("Welcome to Grid AI ⚡")
    page = st.radio("Navigation", ["Login", "Sign Up"], horizontal=True)

    if page == "Login":
        login_page()
    elif page == "Sign Up":
        signup_page()

else:
    # 🎯 **Show Sidebar After Login**
    st.sidebar.title(f"👋 Welcome, {st.session_state['username']}!")

    # Sidebar navigation that doesn't reset
    page = st.sidebar.radio(
        "Navigation",
        ["Enter Historical Data", "Logistics", "Transactional AI", "Forecasting Energy", "Logout"],  # ✅ NEW: Forecasting Energy
        index=["Enter Historical Data", "Logistics", "Transactional AI", "Forecasting Energy", "Logout"].index(st.session_state["current_page"])
    )

    # Preserve the selected page
    st.session_state["current_page"] = page

    # Render the selected page
    if page == "Enter Historical Data":
        historical_data_page()
    elif page == "Logistics":
        logistics_page()
    elif page == "Transactional AI":
        transactional_ai_page()
    elif page == "Forecasting Energy":  # ✅ NEW: Handle Forecasting Page
        forecasting_energy_page()
    elif page == "Logout":
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["current_page"] = "Enter Historical Data"  # Reset default page after logout
        st.rerun()

# Hide Streamlit default sidebar elements
hide_sidebar_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}  /* Hide sidebar navigation (top-left) */
    header {display: none;}  /* Hide Streamlit default header */
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)
