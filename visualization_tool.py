from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
ATLAS_URI = os.getenv("MONGO_URI")  # Replace with your MongoDB URI
DB_NAME = "energy_trade_db"
COLLECTION_NAME = "optimized_trades"


def fetch_from_mongo():
    """Fetches data from the specified MongoDB collection."""
    try:
        # Connect to MongoDB
        client = MongoClient(ATLAS_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Fetch all documents from the collection
        data = list(collection.find())

        # Convert to DataFrame for better manipulation
        df = pd.DataFrame(data)

        # Drop the '_id' field to avoid issues
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)

        return df

    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error
