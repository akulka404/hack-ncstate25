import streamlit as st
import pandas as pd
from database import insert_data, fetch_data, delete_all_data

def transactional_ai_page():
    """Allows users to set and store transactional AI preferences in MongoDB."""
    st.subheader("🤖 Transactional AI Settings")
    st.write("Set the lowest selling price and highest buying price for transactions.")

    # Database and collection for transactional AI
    db_name = "transactions"
    collection_name = "sellnbuy_data"

    # Input Fields
    lowest_selling_price = st.number_input(
        "Set the lowest selling price you are ready to go for:",
        min_value=0.0,
        value=10.0,
        step=0.1,
    )

    highest_buying_price = st.number_input(
        "Set the highest buying price you are ready to go for:",
        min_value=0.0,
        value=50.0,
        step=0.1,
    )

    # Submit Data to MongoDB
    if st.button("Submit Data to Database"):
        if lowest_selling_price >= highest_buying_price:
            st.error("❌ The lowest selling price cannot be greater than or equal to the highest buying price.")
        else:
            data_dict = [{
                "lowest_selling_price": lowest_selling_price,
                "highest_buying_price": highest_buying_price,
            }]

            if insert_data(db_name, collection_name, data_dict):
                st.success("✅ Data successfully stored in MongoDB Atlas!")
            else:
                st.error("❌ Error inserting data. Please check the input format.")

    # Delete Old Data
    if st.button("Delete Old Data"):
        deleted_count = delete_all_data(db_name, collection_name)
        if deleted_count > 0:
            st.success(f"✅ Deleted {deleted_count} old records from MongoDB!")
        else:
            st.warning("⚠ No data found to delete or an error occurred.")

    # Fetch and display stored transactional AI data from MongoDB
    if st.button("Show Stored Data"):
        data = fetch_data(db_name, collection_name)
        if data:
            df_stored = pd.DataFrame(data)
            st.write("📄 Data stored in MongoDB:")
            st.dataframe(df_stored)
        else:
            st.warning("⚠ No data found in MongoDB.")
