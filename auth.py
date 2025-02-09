import streamlit as st
from database import register_user, authenticate_user

def login_page():
    """Displays the login form and handles authentication."""
    st.subheader("🔑 Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials! Please try again.")

def signup_page():
    """Displays the signup form and handles user registration."""
    st.subheader("📝 Create a new account")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password == confirm_password:
            if register_user(new_username, new_password):
                st.success("✅ Account created successfully! You can now log in.")
            else:
                st.error("⚠ Username already exists. Try a different one.")
        else:
            st.error("⚠ Passwords do not match!")
