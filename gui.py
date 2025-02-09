import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

# Dummy user database
USER_DB = {'test_user': 'password123'}

# Function to check login credentials
def authenticate(username, password):
    return USER_DB.get(username) == password

# Function to generate random profit/loss data
def get_profit_loss():
    return round(random.uniform(-1000, 5000), 2)

# Function to generate dummy graphs
def generate_graphs():
    graphs = []
    for i in range(3):
        fig, ax = plt.subplots()
        x = list(range(10))
        y = [random.randint(1, 100) for _ in range(10)]
        ax.plot(x, y, marker='o')
        ax.set_title(f'Graph {i+1}')
        graphs.append(fig)
    return graphs

def main():
    st.set_page_config(page_title="Dashboard", layout="wide")
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("Welcome to the Dashboard")
        st.write("Login or Sign Up to continue")
        
        col1, col2 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password", key="password")
            
            login_btn = st.button("Login")
            signup_btn = st.button("Sign Up")
            
            if login_btn:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
                    
            if signup_btn:
                if username in USER_DB:
                    st.error("Username already exists")
                else:
                    USER_DB[username] = password
                    st.success("Signup successful! Please login.")
    else:
        # Dashboard Layout
        st.title("User Dashboard")
        profit_loss = get_profit_loss()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Profit/Loss")
            st.metric(label="Current Profit/Loss", value=f"${profit_loss}")
        
        # Graph Carousel
        graphs = generate_graphs()
        if "graph_index" not in st.session_state:
            st.session_state.graph_index = 0
        
        with col2:
            st.subheader("Analytics")
            st.pyplot(graphs[st.session_state.graph_index])
            
            col_left, col_right = st.columns([1, 1])
            with col_left:
                if st.button("⬅ Previous"):
                    st.session_state.graph_index = (st.session_state.graph_index - 1) % len(graphs)
                    st.experimental_rerun()
            with col_right:
                if st.button("Next ➡"):
                    st.session_state.graph_index = (st.session_state.graph_index + 1) % len(graphs)
                    st.experimental_rerun()
        
        # Second row (Placeholder for additional components)
        st.subheader("Additional Analytics")
        st.write("This section can be extended with more charts, statistics, or reports.")

if __name__ == "__main__":
    main()
