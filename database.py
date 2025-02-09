import os
import sqlite3
import pymongo
import bcrypt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🔹 SQLite Setup (for user authentication)
sqlite_conn = sqlite3.connect("users.db", check_same_thread=False)
sqlite_cursor = sqlite_conn.cursor()

# Ensure users table exists with hashed passwords
sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT)''')
sqlite_conn.commit()


# 🔹 Function to hash passwords before storing
def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# 🔹 Function to check passwords
def check_password(password, hashed):
    """Checks if a plaintext password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

# 🔹 Register User in SQLite
def register_user(username, password):
    """Registers a new user with hashed password in SQLite."""
    try:
        hashed_password = hash_password(password)  # Hash password before storing
        sqlite_cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        sqlite_conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

# 🔹 Authenticate User in SQLite
def authenticate_user(username, password):
    """Authenticates user by checking the hashed password in SQLite."""
    sqlite_cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    user = sqlite_cursor.fetchone()
    
    if user and check_password(password, user[0]):  # Verify hashed password
        return True
    return False

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Atlas URI from .env file
ATLAS_URI = os.getenv("MONGO_URI")  # Ensure this is set in .env
DB_NAME = "energy_db"
COLLECTION_NAME = "historical_data"

class AtlasClient:
    """MongoDB Atlas Client to manage database connections and operations."""

    def __init__(self, atlas_uri, dbname):
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]

    def ping(self):
        """Test MongoDB connection."""
        try:
            self.mongodb_client.admin.command("ping")
            print("✅ Connected to MongoDB Atlas!")
        except Exception as e:
            print(f"❌ MongoDB Ping Error: {e}")

    def get_collection(self, collection_name):
        """Retrieve a collection from the database."""
        return self.database[collection_name]

    def insert_data(self, collection_name, data):
        """Insert one document into a collection."""
        collection = self.database[collection_name]
        return collection.insert_one(data)

    def find_data(self, collection_name, filter={}, limit=0):
        """Retrieve data from a collection."""
        collection = self.database[collection_name]
        return list(collection.find(filter=filter, limit=limit))


# Initialize MongoDB connection
atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
atlas_client.ping()

# Function to insert historical data
def insert_historical_data(data):
    """Inserts multiple records into MongoDB."""
    try:
        collection = atlas_client.get_collection(COLLECTION_NAME)
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
        return True
    except Exception as e:
        print(f"❌ MongoDB Insert Error: {e}")
        return False

# Function to fetch historical data
def fetch_historical_data():
    """Fetches all records from MongoDB."""
    try:
        return atlas_client.find_data(COLLECTION_NAME)
    except Exception as e:
        print(f"❌ MongoDB Fetch Error: {e}")
        return []
