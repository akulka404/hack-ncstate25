# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'energy_trading')
    MAX_PRICE_FLUCTUATION = 0.20  # 20% max price fluctuation
    PREDICTION_WINDOW = 7  # 7 days prediction window
