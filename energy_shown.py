from web3 import Web3
import json
import time
from datetime import datetime
import pandas as pd
import requests
from pymongo import MongoClient

# Load CSV Data
file_path = "future_trading_forecast.csv"
df = pd.read_csv(file_path)

# MongoDB Connection
uri = "mongodb+srv://firasat:zd7RQlTbaz7qf6AT@gridcluster.3ft8i.mongodb.net/?retryWrites=true&w=majority&appName=GridCluster"
client = MongoClient(uri)
db = client["transactions"]
collection = db["sellnbuy_data"]

def fetch_market_prices():
    latest_data = list(collection.find().sort("_id", -1).limit(1))
    if latest_data:
        return latest_data[0]  # Expected format: {"H1": [sell_price, buy_price], ...}
    else:
        raise Exception("No market prices found in MongoDB")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected(), "Connection failed"
print(f"Connected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def create_market(week_data, grid_price):
    market_prices = fetch_market_prices()
    market = {}
    
    for _, row in week_data.iterrows():
        house = row["HouseholdID"]
        generation = row["PredictedGeneration"]
        usage = row["PredictedUsage"]
        sell_price, buy_price = market_prices.get(house, [grid_price, grid_price])
        
        market[house] = {
            "excess": max(round(generation - usage, 2), 0),
            "deficit": max(round(usage - generation, 2), 0),
            "sell_price": sell_price,
            "buy_price": buy_price,
            "original_sell": sell_price,
            "original_buy": buy_price
        }
    
    return market

def execute_transaction(seller, buyer, amount, price, market):
    print(f"⚡ {seller} → {buyer}: {amount}kWh @ ${price}/kWh")
    market[seller]["excess"] -= amount
    market[buyer]["deficit"] -= amount

def resolve_deficits(market, grid_price):
    buyers = [h for h in market if market[h]["deficit"] > 0]
    
    for buyer in buyers:
        while market[buyer]["deficit"] > 0:
            sellers = [h for h in market if h != buyer and market[h]["excess"] > 0 and market[h]["sell_price"] <= market[buyer]["buy_price"]]
            
            if not sellers:
                grid_cost = market[buyer]["deficit"] * grid_price
                print(f"🏭 {buyer} bought {market[buyer]['deficit']}kWh from grid @ ${grid_price}/kWh")
                market[buyer]["deficit"] = 0
                break
            
            best_seller = min(sellers, key=lambda x: market[x]["sell_price"])
            max_amount = min(market[best_seller]["excess"], market[buyer]["deficit"])
            execute_transaction(best_seller, buyer, max_amount, market[best_seller]["sell_price"], market)

# Process all available weeks in dataset
unique_dates = df["Date"].unique()
for current_date in unique_dates:
    print(f"\n==================== Week: {current_date} ====================")
    week_data = df[df["Date"] == current_date]
    grid_price = week_data["DynamicPrice"].iloc[0]  # Update grid price per week
    market = create_market(week_data, grid_price)
    
    print("\n🔋 Initial Market State:")
    for house, data in market.items():
        status = "SELLER" if data["excess"] > 0 else "BUYER"
        print(f"{house} [{status}]")
        print(f"  Sell: ${data['sell_price']}/kWh | Buy: ${data['buy_price']}/kWh")
        print(f"  Excess: {data['excess']}kWh | Deficit: {data['deficit']}kWh")
    
    resolve_deficits(market, grid_price)
    
    print("\n🏁 Final Market State:")
    for house, data in market.items():
        status = "SELLER" if data["excess"] > 0 else "BUYER"
        print(f"{house} [{status}]")
        print(f"  Remaining Excess: {data['excess']}kWh")
        print(f"  Remaining Deficit: {data['deficit']}kWh")
        print(f"  Final Sell Price: ${data['sell_price']}/kWh")
    print(f"===========================================================\n")
