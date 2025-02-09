import pandas as pd
import plotly.graph_objects as go

def generate_household_plots(df, household_id="H5"):
    """
    Generate comprehensive plots for a specific household's energy data using Plotly.
    
    Parameters:
    df (pandas.DataFrame): Complete household data.
    household_id (str): Household ID (e.g., 'H1', 'H2', etc.). Default is 'H5'.
    """
    # Filter data for the specific household
    household_df = df[df['HouseholdID'] == household_id].copy()
    household_df['Delta'] = household_df['EnergyGeneratedFromRenewableSources'] - household_df['EnergyUsed']
    
    # 1. Energy Usage vs Generation Plot
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=household_df['Date'],
        y=household_df['EnergyUsed'],
        name='Energy Used',
        line=dict(color='red')
    ))
    fig1.add_trace(go.Scatter(
        x=household_df['Date'],
        y=household_df['EnergyGeneratedFromRenewableSources'],
        name='Energy Generated',
        line=dict(color='green')
    ))
    fig1.update_layout(
        title=f'Energy Usage vs Generation - Household {household_id}',
        xaxis_title='Date',
        yaxis_title='Energy (kWh)',
        hovermode='x unified'
    )
    fig1.show()

    # 2. Energy Surplus/Deficit Analysis
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=household_df['Date'],
        y=household_df['Delta'],
        line=dict(color='blue')
    ))
    fig2.update_layout(
        title=f'Energy Surplus/Deficit Over Time - Household {household_id}',
        xaxis_title='Date',
        yaxis_title='Energy Delta (kWh)',
        hovermode='x'
    )
    fig2.add_hline(y=0, line_dash="dash", line_color="red")
    fig2.show()

    # 3. Trading Activity
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=household_df['Date'],
        y=household_df['EnergyBought'],
        name='Energy Bought',
        line=dict(color='red')
    ))
    fig3.add_trace(go.Scatter(
        x=household_df['Date'],
        y=household_df['EnergySold'],
        name='Energy Sold',
        line=dict(color='green')
    ))
    fig3.update_layout(
        title=f'Trading Activity - Household {household_id}',
        xaxis_title='Date',
        yaxis_title='Energy (kWh)',
        hovermode='x unified'
    )
    fig3.show()

    # 4. Financial Analysis
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=household_df['Date'],
        y=household_df['TotalExpenditure'],
        line=dict(color='purple')
    ))
    fig4.update_layout(
        title=f'Weekly Energy Expenditure - Household {household_id}',
        xaxis_title='Date',
        yaxis_title='Expenditure ($)',
        hovermode='x'
    )
    fig4.add_hline(y=0, line_dash="dash", line_color="gray")
    fig4.show()

    # Print summary statistics
    stats = {
        'Average Weekly Usage (kWh)': household_df['EnergyUsed'].mean(),
        'Average Weekly Generation (kWh)': household_df['EnergyGeneratedFromRenewableSources'].mean(),
        'Average Weekly Expenditure ($)': household_df['TotalExpenditure'].mean(),
        'Total Net Expenditure ($)': household_df['TotalExpenditure'].sum(),
        'Weeks as Seller': (household_df['Delta'] > 0).sum(),
        'Weeks as Buyer': (household_df['Delta'] < 0).sum()
    }
    
    print(f"\nSummary Statistics for Household {household_id}")
    print("-" * 50)
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")

