import streamlit as st
import pandas as pd
from forecasting_model import predict_future_weeks
from trade_optimizer import extract_weekly_trade_data, run_trade_optimization
from database import insert_data  # ✅ Store forecasts & trades in MongoDB

def forecasting_energy_page():
    """UI for Forecasting Energy Data for Next 10 Weeks and Optimizing Trade Plans."""
    st.title("🔮 Forecasting Energy Usage & Trading Optimization")

    # Generate Forecasted Data
    if st.button("📊 Generate Next 10 Weeks of Data"):
        with st.spinner("⏳ Generating Forecasts..."):
            try:
                # 🚀 Load household models & generate forecast
                # household_models = load_household_models()
                # df = pd.read_csv("../data/sample_household_data.csv")  # Load historical data
                future_df = predict_future_weeks()  # Generate predictions

                # Display Forecast Data
                st.subheader("📄 Forecast Data Preview")
                st.dataframe(future_df)

                # Store Forecast Data in MongoDB
                db_name = "energy_forecast_db"
                collection_name = "weekly_forecasts"
                insert_data(db_name, collection_name, future_df.to_dict(orient="records"))

                st.success("✅ Forecast stored successfully in MongoDB!")

                # Store future_df in session state for next step
                st.session_state["future_df"] = future_df
                
            except Exception as e:
                st.error(f"❌ Error generating forecast: {e}")

    # Optimize Trade Plan
    if "future_df" in st.session_state and st.button("⚡ Optimize Trading Plan"):
        with st.spinner("🔄 Running Trade Optimization..."):
            try:
                # Extract sample week data
                buyers, sellers = extract_weekly_trade_data(st.session_state["future_df"])

                # Display Sample Week Buyers & Sellers Data
                st.subheader("📊 Sample Week Data (Buyers & Sellers)")
                st.write("**Buyers:**")
                st.dataframe(buyers)
                st.write("**Sellers:**")
                st.dataframe(sellers)

                # Run trade optimization
                optimal_trade_df = run_trade_optimization(st.session_state["future_df"])

                # Display Optimized Trade Plan
                st.subheader("🔄 Optimized Trade Plan")
                st.dataframe(optimal_trade_df)

                # Store Trade Plan in MongoDB
                trade_db = "energy_trade_db"
                trade_collection = "optimized_trades"
                insert_data(trade_db, trade_collection, optimal_trade_df.to_dict(orient="records"))

                st.success("✅ Trade Plan stored successfully in MongoDB!")

            except Exception as e:
                st.error(f"❌ Error optimizing trade plan: {e}")
