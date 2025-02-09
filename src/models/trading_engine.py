# src/models/trading_engine.py
import numpy as np
import pandas as pd
class DynamicTradingEngine:
    def __init__(self, base_rate=0.14, max_fluctuation=0.20):
        self.base_rate = base_rate
        self.max_fluctuation = max_fluctuation
        
    def calculate_dynamic_price(self, total_supply, total_demand, time_of_day, season):
        if total_demand == 0:
            return self.base_rate
            
        # Increase supply-demand impact
        supply_demand_ratio = total_supply / total_demand
        price_adjustment = np.clip(1 - supply_demand_ratio, 
                                -self.max_fluctuation * 2,  # Double the max fluctuation
                                self.max_fluctuation * 2)
        
        # More dramatic time-of-day pricing
        if 9 <= time_of_day <= 11:  # Morning peak
            time_multiplier = 1.4
        elif 14 <= time_of_day <= 16:  # Afternoon peak
            time_multiplier = 1.6
        elif 19 <= time_of_day <= 21:  # Evening peak
            time_multiplier = 1.8
        else:
            time_multiplier = 0.7  # Off-peak discount
        
        # More pronounced seasonal factors
        season_multipliers = {
            'summer': 1.8,  # Higher cooling demand
            'winter': 1.6,  # Higher heating demand
            'spring': 0.9,
            'fall': 0.8
        }
        
        # Add random market volatility
        volatility = np.random.uniform(-0.1, 0.1)
        
        final_price = self.base_rate * (1 + price_adjustment) * time_multiplier * \
                    season_multipliers[season] * (1 + volatility)
        return round(final_price, 4)

    def match_orders(self, sellers_df, buyers_df, current_time, season):
        """Match orders with dynamic pricing"""
        matches = []
        sellers = sellers_df.sort_values('sellingRate')
        buyers = buyers_df.sort_values('buyingRate', ascending=False)
        
        total_supply = sellers['unitsToBeSold'].sum()
        total_demand = buyers['demand'].sum()
        
        for _, buyer in buyers.iterrows():
            remaining_demand = buyer['demand']
            max_buy_price = buyer['buyingRate']
            
            for _, seller in sellers.iterrows():
                if remaining_demand <= 0:
                    break
                
                # Calculate current market price
                current_price = self.calculate_dynamic_price(
                    total_supply, total_demand,
                    current_time, season
                )
                
                if current_price > max_buy_price:
                    continue
                    
                traded_amount = min(remaining_demand, seller['unitsToBeSold'])
                
                if traded_amount > 0:
                    matches.append({
                        'buyer_id': buyer['householdID'],
                        'seller_id': seller['householdID'],
                        'amount': traded_amount,
                        'price_per_unit': current_price,
                        'total_cost': round(traded_amount * current_price, 2),
                        'timestamp': current_time
                    })
                    
                    remaining_demand -= traded_amount
                    seller['unitsToBeSold'] -= traded_amount
                    total_supply -= traded_amount
                    total_demand -= traded_amount
        
        return pd.DataFrame(matches)
