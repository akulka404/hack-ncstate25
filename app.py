import streamlit as st
from auth import login_page, signup_page
from pages.logistics import logistics_page
from pages.historical_data import historical_data_page
from pages.transactional_ai import transactional_ai_page

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

# Sidebar Navigation
if not st.session_state["authenticated"]:
    st.sidebar.title("🔑 Authentication")
    page = st.sidebar.radio("Navigation", ["Login", "Sign Up"])

    if page == "Login":
        login_page()
    elif page == "Sign Up":
        signup_page()

else:
    st.sidebar.title(f"👋 Welcome, {st.session_state['username']}!")
    page = st.sidebar.radio("Navigation", ["Logistics", "Enter Historical Data", "Transactional AI", "Logout"])

    if page == "Logistics":
        logistics_page()
    elif page == "Enter Historical Data":
        historical_data_page()
    elif page == "Transactional AI":
        transactional_ai_page()
    elif page == "Logout":
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()
