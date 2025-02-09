import pandas as pd

def extract_weekly_trade_data(future_df, week_index=7):
    """
    Extracts a sample week of forecasted data and prepares buyers & sellers.

    Args:
        future_df (pd.DataFrame): Forecasted energy data.
        week_index (int): Index of the week to extract from forecast.

    Returns:
        tuple: (buyers, sellers) DataFrames with updated Remaining Demand/Supply.
    """
    sample_dates = future_df["Date"].unique()
    sample_week = future_df[future_df["Date"] == sample_dates[week_index]].copy()

    # Add Selling Price (SP) & Buying Price (BP) values (example fixed values)
    sample_week["SP"] = [0.20, 0.40, 0.10, 0.30, 0.05]  # Seller Price per kWh
    sample_week["BP"] = [0.15, 0.30, 0.05, 0.25, 0.10]  # Buyer Price per kWh

    # Split Buyers & Sellers
    buyers = sample_week[sample_week["TradingPosition"] == "Buyer"].copy()
    sellers = sample_week[sample_week["TradingPosition"] == "Seller"].copy()

    # Calculate Remaining Demand/Supply
    buyers["RemainingDemand"] = buyers["PredictedUsage"] - buyers["PredictedGeneration"]
    sellers["RemainingSupply"] = sellers["PredictedGeneration"] - sellers["PredictedUsage"]

    # Drop Unnecessary Columns
    buyers.drop(columns=["PredictedUsage", "PredictedGeneration", "TradingPosition"], inplace=True)
    sellers.drop(columns=["PredictedUsage", "PredictedGeneration", "TradingPosition"], inplace=True)

    return buyers, sellers

def optimal_trade_plan(buyers, sellers, trade_plan=None):
    """
    Recursively finds the optimal trade plan where buyers and sellers match based on pricing and demand.

    Args:
        buyers (pd.DataFrame): Buyers with their demand & buying price.
        sellers (pd.DataFrame): Sellers with their supply & selling price.
        trade_plan (list): List of previous trades (used for recursion).

    Returns:
        tuple: (optimal_plan, total_cost)
    """
    if trade_plan is None:
        trade_plan = []
    
    # If all buyers' demands are met or all sellers' supplies are exhausted, return the trade plan
    if buyers["RemainingDemand"].sum() == 0 or sellers["RemainingSupply"].sum() == 0:
        return trade_plan, sum(t["Total Cost ($)"] for t in trade_plan)

    optimal_plan = None
    optimal_cost = float("inf")

    # Iterate over all possible buyer-seller pairs
    for buyer_idx, buyer in buyers[buyers["RemainingDemand"] > 0].iterrows():
        for seller_idx, seller in sellers[sellers["RemainingSupply"] > 0].iterrows():
            if buyer["BP"] >= seller["SP"]:  # Check if a deal is possible
                trade_volume = min(buyer["RemainingDemand"], seller["RemainingSupply"])
                trade_price = (buyer["BP"] + seller["SP"]) / 2  # Midpoint price
                
                # Create a new trade plan by adding this transaction
                new_trade = {
                    "Buyer": buyer["HouseholdID"],
                    "Seller": seller["HouseholdID"],
                    "Volume (kWh)": trade_volume,
                    "Price ($/kWh)": trade_price,
                    "Total Cost ($)": trade_volume * trade_price
                }
                
                # Update buyers and sellers
                new_buyers = buyers.copy()
                new_sellers = sellers.copy()
                new_buyers.at[buyer_idx, "RemainingDemand"] -= trade_volume
                new_sellers.at[seller_idx, "RemainingSupply"] -= trade_volume

                # Recursively find the optimal plan for the remaining buyers and sellers
                current_plan, current_cost = optimal_trade_plan(new_buyers, new_sellers, trade_plan + [new_trade])

                # Update the optimal plan if the current plan is better
                if current_cost < optimal_cost:
                    optimal_plan = current_plan
                    optimal_cost = current_cost
                print(new_buyers)
                print(new_sellers)

    return optimal_plan, optimal_cost


def run_trade_optimization(future_df, week_index=7):
    """
    Runs the full buyer-seller trade optimization for a selected week.

    Args:
        future_df (pd.DataFrame): Forecasted energy data.
        week_index (int): Index of the forecasted week to optimize.

    Returns:
        pd.DataFrame: Optimal trade plan.
    """
    buyers, sellers = extract_weekly_trade_data(future_df, week_index)

    # Run optimization function
    optimal_plan, total_cost = optimal_trade_plan(buyers, sellers)

    # Convert to DataFrame for easy viewing
    optimal_plan_df = pd.DataFrame(optimal_plan)

    print("\n🔥 Optimal Trade Plan 🔥")
    print(optimal_plan_df)

    print("\n💰 Total Cost for Buyers:")
    print(total_cost)

    return optimal_plan_df
