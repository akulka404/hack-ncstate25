import streamlit as st
import pandas as pd
import plotly.express as px
from utils.forecasting_model import forecast_energy

def forecasting_energy_page():
    """Page for forecasting future energy usage based on historical data."""
    st.title("🔮 Forecasting Energy Usage")

    # File Upload UI
    uploaded_file = st.file_uploader("📂 Upload Historical Energy Data (CSV)", type="csv")

    if uploaded_file is not None:
        # Load CSV data
        df = pd.read_csv(uploaded_file, parse_dates=["Date"])

        # Show a preview of the uploaded data
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

        # Ensure the dataset has the correct columns
        required_columns = {"Date", "EnergyUsed", "EnergyGeneratedFromRenewableSources"}
        if not required_columns.issubset(df.columns):
            st.error(f"❌ Missing required columns: {required_columns - set(df.columns)}")
            return

        # User selects forecast duration
        forecast_days = st.slider("📅 Select Forecast Horizon (Days)", min_value=7, max_value=365, value=30)

        # Run Forecasting Model
        if st.button("🔍 Forecast Energy Usage"):
            with st.spinner("🔄 Running forecast..."):
                forecast_df = forecast_energy(df, forecast_days)

                # Plot Results
                fig = px.line(forecast_df, x="Date", y="EnergyForecast", title="📈 Forecasted Energy Usage")
                fig.add_scatter(x=df["Date"], y=df["EnergyUsed"], mode="lines", name="Historical Energy Used")
                st.plotly_chart(fig)

                st.success("✅ Forecast Completed!")
