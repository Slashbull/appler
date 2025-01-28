import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

def forecast_imports(data):
    """
    Forecast future imports using a simple machine learning model (e.g., Linear Regression).
    """

    # Example: Forecast imports using 'Month' and 'Year' as features
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    data['Year'] = pd.to_datetime(data['Date']).dt.year

    # Prepare features and target variable
    X = data[['Month', 'Year']]
    y = data['Quantity']  # Assuming 'Quantity' is the target variable

    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future imports (for example, forecasting for the next 12 months)
    future_months = pd.DataFrame({
        'Month': [i for i in range(1, 13)],  # Example for 12 months
        'Year': [2025] * 12  # Example forecasting for the year 2025
    })
    forecast = model.predict(future_months)

    # Create a forecast plot
    forecast_plot = go.Figure()
    forecast_plot.add_trace(go.Scatter(x=future_months['Month'], y=forecast, mode='lines', name='Forecasted Imports'))
    forecast_plot.update_layout(title="Forecasted Imports for 2025", xaxis_title="Month", yaxis_title="Imports (Kgs)")
    
    return forecast_plot
