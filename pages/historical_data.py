import streamlit as st
import pandas as pd
from database import insert_data, fetch_data, delete_all_data
from csv_to_list import csv_to_list  # Import conversion function

def historical_data_page():
    """Allows users to upload and store CSV data into MongoDB."""
    st.subheader("📊 Enter Historical Data")
    st.write("Upload a CSV file with columns: Energy Used, Energy Generated, Total Exp, Sold, Bought.")

    # Database and collection for historical data
    db_name = "energy_db"
    collection_name = "historical_data"

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
                if insert_data(db_name, collection_name, data_dict):
                    st.success("✅ Data successfully stored in MongoDB Atlas!")
                else:
                    st.error("❌ Error inserting data. Please check the file format.")

    # Delete Old Data
    if st.button("Delete Old Data"):
        deleted_count = delete_all_data(db_name, collection_name)
        if deleted_count > 0:
            st.success(f"✅ Deleted {deleted_count} old records from MongoDB!")
        else:
            st.warning("⚠ No data found to delete or an error occurred.")

    # Fetch and display historical data from MongoDB
    if st.button("Show Stored Data"):
        data = fetch_data(db_name, collection_name)
        if data:
            df_stored = pd.DataFrame(data)
            st.write("📄 Data stored in MongoDB:")
            st.dataframe(df_stored)
        else:
            st.warning("⚠ No data found in MongoDB.")
