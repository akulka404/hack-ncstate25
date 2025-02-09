# src/data_processor.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataProcessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.is_fitted = False
    
    def load_household_data(self, file_path):
        """Load and preprocess household energy data"""
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Fit the scaler when loading data
        features = ['EnergyUsed', 'EnergyGeneratedFromRenewableSources', 
                   'EnergyBought', 'EnergySold', 'TotalExpenditure']
        self.scaler.fit(df[features])
        self.is_fitted = True
        return df
    
    def calculate_delta(self, generated, used):
        """Calculate energy surplus/deficit"""
        return generated - used
    
    def prepare_training_data(self, df, sequence_length=4):
        """Prepare time series data for model training"""
        features = ['EnergyUsed', 'EnergyGeneratedFromRenewableSources', 
                    'EnergyBought', 'EnergySold', 'TotalExpenditure']
        
        # First fit the scaler if not already fitted
        if not self.is_fitted:
            self.scaler.fit(df[features])
            self.is_fitted = True
        
        # Scale the features
        scaled_data = self.scaler.transform(df[features])
        
        X, y = [], []
        
        # Create sequences for each household separately
        for household in df['HouseholdID'].unique():
            household_data = scaled_data[df['HouseholdID'] == household]
            
            for i in range(len(household_data) - sequence_length):
                # Input sequence
                X.append(household_data[i:(i + sequence_length)])
                # Target value (TotalExpenditure)
                y.append(household_data[i + sequence_length, -1])
        
        return np.array(X), np.array(y)

    
    def prepare_prediction_data(self, recent_data):
        """Prepare recent data for prediction"""
        features = ['EnergyUsed', 'EnergyGeneratedFromRenewableSources', 
                   'EnergyBought', 'EnergySold', 'TotalExpenditure']
        
        if not self.is_fitted:
            self.scaler.fit(recent_data[features])
            self.is_fitted = True
            
        scaled_data = self.scaler.transform(recent_data[features])
        X_pred = scaled_data.reshape(1, scaled_data.shape[0], scaled_data.shape[1])
        return X_pred
