from fbprophet import Prophet
import pandas as pd

def forecast_energy(df, forecast_days=30):
    """
    Forecast future energy usage using Facebook Prophet.
    Args:
        df (DataFrame): Historical energy data (with 'Date' and 'EnergyUsed' columns)
        forecast_days (int): Number of days to predict into the future.
    Returns:
        DataFrame: Forecasted energy usage.
    """
    df = df.rename(columns={"Date": "ds", "EnergyUsed": "y"})

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)

    # Rename columns
    forecast = forecast[["ds", "yhat"]].rename(columns={"ds": "Date", "yhat": "EnergyForecast"})
    return forecast
