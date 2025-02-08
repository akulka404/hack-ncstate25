# src/data_processor.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataProcessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def load_household_data(self, file_path):
        """Load and preprocess household energy data"""
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Calculate rate per unit for analysis
        df['RatePerUnit'] = df['TotalExpenditure'] / df['EnergyBought'].replace(0, 1)
        return df
    
    def calculate_delta(self, generated, used):
        """Calculate energy surplus/deficit"""
        return generated - used
    
    def prepare_training_data(self, df, sequence_length=4):
        """Prepare time series data for model training"""
        features = ['EnergyUsed', 'EnergyGeneratedFromRenewableSources', 
                   'EnergyBought', 'EnergySold', 'RatePerUnit', 'TotalExpenditure']
        
        scaled_data = self.scaler.fit_transform(df[features])
        X, y = [], []
        
        for i in range(len(scaled_data) - sequence_length):
            X.append(scaled_data[i:(i + sequence_length), :-1])  # All features except TotalExpenditure
            y.append(scaled_data[i + sequence_length, -1])  # TotalExpenditure
            
        return np.array(X), np.array(y)
