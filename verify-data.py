from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
uri = "mongodb+srv://aniruddhak1911:CmACAFpIdTx2RsMy@cluster0.o8hkt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client["gridwise"]
collection = db["energy_data"]

# Fetch Last 10 Entries
latest_data = list(collection.find().sort("_id", -1).limit(10))

# Convert to DataFrame for Visualization
df = pd.DataFrame(latest_data)
print(df)

import matplotlib.pyplot as plt

# Extract time & values
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df.set_index("timestamp", inplace=True)

plt.figure(figsize=(10, 5))
plt.plot(df["solar_output"], label="Solar Output (kWh)", color="orange")
plt.plot(df["energy_used"], label="Energy Used (kWh)", color="blue")
plt.xlabel("Time")
plt.ylabel("Energy (kWh)")
plt.title("Energy Consumption vs. Solar Generation")
plt.legend()
plt.show()

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Select relevant data columns
data = df[["solar_output", "energy_used", "grid_voltage"]].values

# Normalize Data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Prepare Data for LSTM (Past 10 Time Steps → Predict Next Step)
X, y = [], []
for i in range(10, len(data_scaled)):
    X.append(data_scaled[i-10:i])
    y.append(data_scaled[i, 1])  # Predict energy_used

X, y = np.array(X), np.array(y)

# Build LSTM Model
model = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    LSTM(50, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=20, batch_size=32)

# Save Model
model.save("energy_forecast_model.h5")
