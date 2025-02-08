# src/models/expenditure_predictor.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class ExpenditurePredictor:
    def __init__(self, sequence_length=4, n_features=5):
        self.model = self._build_model(sequence_length, n_features)
        
    def _build_model(self, sequence_length, n_features):
        """Build LSTM model for expenditure prediction"""
        model = Sequential([
            LSTM(64, input_shape=(sequence_length, n_features), return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dense(16, activation='relu'),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def train(self, X_train, y_train, epochs=100, batch_size=32):
        """Train the model"""
        return self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2
        )
    
    def predict(self, X):
        """Predict expenditure"""
        return self.model.predict(X)
