import streamlit as st
import pandas as pd
from database import insert_historical_data, fetch_historical_data
from csv_to_list import csv_to_list  # Import conversion function

def historical_data_page():
    """Allows users to upload and store CSV data into MongoDB."""
    st.subheader("📊 Enter Historical Data")
    st.write("Upload a CSV file with columns: Energy Used, Energy Generated, Total Exp, Sold, Bought.")

    # File Upload UI
    uploaded_file = st.file_uploader("Upload CSV File", type="csv")

    if uploaded_file is not None:
        # Convert CSV file to list of dictionaries
        data_dict = csv_to_list(uploaded_file)

        if data_dict:
            # Show a preview
            df = pd.DataFrame(data_dict)
            st.write("📄 Preview of Uploaded Data:")
            st.dataframe(df.head())

            # Submit Data to MongoDB
            if st.button("Submit Data to Database"):
                if insert_historical_data(data_dict):
                    st.success("✅ Data successfully stored in MongoDB Atlas!")
                else:
                    st.error("❌ Error inserting data. Please check the file format.")

    # Dummy Data Submission
    if st.button("Submit Dummy Data"):
        dummy_record = [
            {
                "Energy Used": 500,
                "Energy Generated": 450,
                "Total Exp": 50,
                "Sold": 100,
                "Bought": 50
            }
        ]

        if insert_historical_data(dummy_record):
            st.success("✅ Dummy data successfully inserted into MongoDB!")
        else:
            st.error("❌ Error inserting dummy data.")

    # Fetch and display historical data from MongoDB
    if st.button("Show Stored Data"):
        data = fetch_historical_data()
        if data:
            df_stored = pd.DataFrame(data)
            st.write("📄 Data stored in MongoDB:")
            st.dataframe(df_stored)
        else:
            st.warning("⚠ No data found in MongoDB.")
