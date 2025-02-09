import pandas as pd
import streamlit as st
from database import fetch_data
from graph_generator import generate_household_plots

def logistics_page():
    st.subheader("📦 Logistics Dashboard")

    db_name = "energy_db"
    collection_name = "historical_data"

    # Fetch data from MongoDB
    st.write("Fetching data from the database...")
    data = fetch_data(db_name, collection_name)

    if data:
        df = pd.DataFrame(data)
        st.write("📄 Data from the Database:")
        st.dataframe(df)

        # Select a household ID
        household_id = st.selectbox(
            "Select Household ID for Analysis:",
            df['HouseholdID'].unique()
        )

        # Generate plots for the selected household
        if st.button("Generate Household Plots"):
            generate_household_plots(df, household_id)
    else:
        st.warning("⚠ No data found in the database.")
