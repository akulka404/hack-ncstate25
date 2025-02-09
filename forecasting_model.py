import sys
import os
from pathlib import Path

# Add parent directory to Python path
notebook_dir = Path(os.getcwd())
project_dir = notebook_dir.parent
sys.path.append(str(project_dir))



# notebooks/03_trading_simulation.ipynb

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from src.models.trading_engine import DynamicTradingEngine
from src.data_processor import DataProcessor
from src.models.expenditure_predictor import ExpenditurePredictor
import tensorflow as tf
from tensorflow.keras.models import Sequential



# Load data
processor = DataProcessor()
df = processor.load_household_data('data/sample_household_data.csv')

def load_household_models(df=df):
    """Load trained models for each household"""
    household_models = {}
    for household in df['HouseholdID'].unique():
        model_path = f'src/models/saved/model_{household}.keras'
        household_models[household] = tf.keras.models.load_model(model_path)
        
household_models = {}
for household in df['HouseholdID'].unique():
    model_path = f'src/models/saved/model_{household}.keras'
    household_models[household] = tf.keras.models.load_model(model_path)

def predict_future_weeks(df=df, household_models=household_models, num_weeks=10):
    """Predict energy patterns and trading positions for next n weeks"""
    last_date = pd.to_datetime(df['Date'].max())
    future_dates = [last_date + pd.Timedelta(weeks=i+1) for i in range(num_weeks)]
    
    # First, calculate weekly market prices
    weekly_prices = {}
    for future_date in future_dates:
        season = get_season(future_date)
        
        # Calculate total supply and demand for the week
        total_supply = df.groupby('Date')['EnergyGeneratedFromRenewableSources'].mean().mean()
        total_demand = df.groupby('Date')['EnergyUsed'].mean().mean()
        
        # Apply seasonal adjustments
        season_mult = {
            'summer': 1.4,
            'winter': 0.6,
            'spring': 1.0,
            'fall': 0.8
        }[season]
        
        # Calculate centralized market price for the week
        market_price = engine.calculate_dynamic_price(
            total_supply=total_supply * season_mult,
            total_demand=total_demand,
            time_of_day=14,  # Using peak hour for base price
            season=season
        )
        weekly_prices[future_date] = market_price
    
    future_predictions = []
    for household in df['HouseholdID'].unique():
        # Get last 4 weeks of data for prediction
        recent_data = df[df['HouseholdID'] == household]
        
        # Use recent averages for baseline predictions
        base_usage = recent_data['EnergyUsed'].mean()
        base_generation = recent_data['EnergyGeneratedFromRenewableSources'].mean()
        
        for future_date in future_dates:
            season = get_season(future_date)
            season_mult = {
                'summer': 1.4,
                'winter': 0.6,
                'spring': 1.0,
                'fall': 0.8
            }[season]
            
            predicted_generation = base_generation * season_mult
            predicted_usage = base_usage
            
            # Calculate if household will be buyer or seller
            delta = predicted_generation - predicted_usage
            trading_position = 'Seller' if delta > 0 else 'Buyer'
            
            future_predictions.append({
                'Date': future_date,
                'HouseholdID': household,
                'PredictedUsage': round(predicted_usage, 2),
                'PredictedGeneration': round(predicted_generation, 2),
                'TradingPosition': trading_position,
                'DynamicPrice': round(weekly_prices[future_date], 4)
            })
    
    return pd.DataFrame(future_predictions)

# Initialize trading engine
engine = DynamicTradingEngine()
def get_season(date):
    month = pd.to_datetime(date).month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'
# Generate predictions for next 10 weeks
future_df = predict_future_weeks(df, household_models)

# Display predictions grouped by date
print("\nTrading Forecast for Next 10 Weeks:")
print(future_df['TradingPosition'].value_counts())
future_df
