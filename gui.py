import streamlit as st
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(layout="wide", page_title="Energy Trading Dashboard")

# Custom CSS for dark theme
st.markdown("""
<style>
    .reportview-container {
        background: #1E1E1E;
        color: #FFFFFF;
    }
    .main {
        background: #1E1E1E;
    }
    .stApp {
        background: #1E1E1E;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stSelectbox > div > div {
        background-color: #2C2C2C;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
    }
    .metric-card {
        background-color: #2C2C2C;
        border: 1px solid #3C3C3C;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card h3 {
        color: #E0E0E0;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        color: #BDBDBD;
        font-size: 0.9rem;
    }
    .scrollable-div {
        height: 300px;
        overflow-y: auto;
        background-color: #2C2C2C;
        border: 1px solid #3C3C3C;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .scrollable-div h3 {
        color: #E0E0E0;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .scrollable-div p {
        color: #BDBDBD;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .stPlotlyChart {
        background-color: #2C2C2C;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for graph navigation
if 'graph_index' not in st.session_state:
    st.session_state.graph_index = 0

# Define options
houses = [f"House {i}" for i in range(1, 6)]
dates = [f"{(datetime.date.today() - datetime.timedelta(days=7*n)).strftime('%Y-%m-%d')} (Week {n})" for n in range(1, 11)]

# Streamlit UI
st.title("Energy Trading Dashboard")

col1, col2 = st.columns(2)
with col1:
    selected_house = st.selectbox("Select House", houses)
with col2:
    selected_date = st.selectbox("Select Date", dates)

# Function to generate random dummy graphs
def generate_dummy_graph():
    graph_types = ['line', 'bar', 'scatter', 'pie']
    graph_type = graph_types[st.session_state.graph_index % 4]
    
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#2C2C2C')
    x = np.arange(10)
    y = np.random.randn(10)
    
    if graph_type == 'line':
        ax.plot(x, y, marker='o', color='#4CAF50')
        ax.set_title('Energy Consumption Trend', fontsize=14, color='#E0E0E0')
    elif graph_type == 'bar':
        ax.bar(x, y, color='#2196F3')
        ax.set_title('Daily Energy Production', fontsize=14, color='#E0E0E0')
    elif graph_type == 'scatter':
        ax.scatter(x, y, c='#FFC107', s=100)
        ax.set_title('Price vs Demand', fontsize=14, color='#E0E0E0')
    elif graph_type == 'pie':
        ax.pie(np.abs(y), labels=[f"Source {i+1}" for i in range(10)], autopct='%1.1f%%', colors=plt.cm.Pastel1_r.colors)
        ax.set_title('Energy Source Distribution', fontsize=14, color='#E0E0E0')
    
    ax.set_facecolor('#2C2C2C')
    ax.tick_params(colors='#BDBDBD')
    ax.spines['bottom'].set_color('#BDBDBD')
    ax.spines['top'].set_color('#BDBDBD') 
    ax.spines['right'].set_color('#BDBDBD')
    ax.spines['left'].set_color('#BDBDBD')
    plt.tight_layout()
    return fig

# First row of boxes
st.markdown("### Key Metrics")
box_row = st.columns(4)
for i, box in enumerate(box_row):
    with box:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Metric {i+1}</h3>
            <p>Value: {random.randint(50, 500)}</p>
        </div>
        """, unsafe_allow_html=True)

# Second row of boxes
st.markdown("### Detailed Analysis")
box_bottom = st.columns(2)
for i, box in enumerate(box_bottom):
    with box:
        if i == 0:  # First detailed box with graphs
            # Navigation buttons
            cols = st.columns([1, 4, 1])
            with cols[0]:
                if st.button('←', key='prev'):
                    st.session_state.graph_index -= 1
            with cols[2]:
                if st.button('→', key='next'):
                    st.session_state.graph_index += 1
            
            # Display current graph
            st.pyplot(generate_dummy_graph())
        else:  # Second detailed box with scrollable text
            st.markdown("""
            <div class="scrollable-div">
                <h3>Energy Market Insights</h3>
                <p>The energy market has shown significant volatility in recent weeks, with prices fluctuating due to various factors including weather patterns, geopolitical events, and changes in supply and demand dynamics.</p>
                <p>Renewable energy sources continue to gain market share, with solar and wind power installations increasing across multiple regions. This shift is driven by both environmental concerns and improving cost-effectiveness of renewable technologies.</p>
                <p>Grid stability remains a key focus area, with utilities and regulators working on implementing smart grid solutions to better manage the integration of intermittent renewable energy sources.</p>
                <p>Energy storage technologies, particularly battery systems, are seeing rapid advancements and declining costs. This trend is expected to play a crucial role in balancing supply and demand, especially as the share of renewable energy grows.</p>
                <p>The concept of prosumers - consumers who also produce energy - is gaining traction, facilitated by the increasing adoption of rooftop solar panels and the development of local energy trading platforms.</p>
                <p>Policy changes and regulatory frameworks continue to evolve, with many jurisdictions introducing or updating incentives for clean energy adoption and setting more ambitious targets for carbon emission reductions.</p>
            </div>
            """, unsafe_allow_html=True)
