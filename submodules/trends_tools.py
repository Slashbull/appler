import pandas as pd
import plotly.express as px

def get_monthly_trends(data):
    """
    Generate a line chart for monthly trends of imports.
    Data should contain 'Date' and 'Quantity' columns.

    Args:
        data (pd.DataFrame): The data containing import records.
    
    Returns:
        fig (plotly.graph_objs.Figure): A Plotly figure object.
    """
    # Grouping data by Month and Year to get total imports per month
    monthly_data = data.groupby(['Year', 'Month'])['Quantity'].sum().reset_index()
    
    # Create the line chart
    fig = px.line(monthly_data, x='Month', y='Quantity', color='Year', 
                  title="Monthly Trends of Imports", 
                  labels={'Quantity': 'Total Quantity (Kgs)', 'Month': 'Month'},
                  markers=True)
    
    # Update layout for better visualization
    fig.update_layout(xaxis=dict(type='category'), height=400)
    
    return fig


def get_yearly_trends(data):
    """
    Generate a bar chart for yearly trends of imports.
    Data should contain 'Year' and 'Quantity' columns.

    Args:
        data (pd.DataFrame): The data containing import records.
    
    Returns:
        fig (plotly.graph_objs.Figure): A Plotly figure object.
    """
    # Grouping data by Year to get total imports per year
    yearly_data = data.groupby('Year')['Quantity'].sum().reset_index()
    
    # Create the bar chart
    fig = px.bar(yearly_data, x='Year', y='Quantity', 
                 title="Yearly Trends of Imports",
                 labels={'Quantity': 'Total Quantity (Kgs)', 'Year': 'Year'})
    
    # Update layout for better visualization
    fig.update_layout(height=400)
    
    return fig


def get_comparative_trends(data, comparison_column="Year"):
    """
    Generate a comparative line chart based on the provided comparison column.
    Can compare trends by Year, Month, or any other categorical column.
    
    Args:
        data (pd.DataFrame): The data containing import records.
        comparison_column (str): The column used for comparison (default: 'Year').
    
    Returns:
        fig (plotly.graph_objs.Figure): A Plotly figure object.
    """
    if comparison_column not in data.columns:
        raise ValueError(f"Column '{comparison_column}' not found in data.")
    
    # Grouping data by the comparison column and summing the imports
    comparative_data = data.groupby([comparison_column, 'Month'])['Quantity'].sum().reset_index()

    # Create the comparative line chart
    fig = px.line(comparative_data, x='Month', y='Quantity', color=comparison_column, 
                  title=f"Comparative Trends by {comparison_column}",
                  labels={'Quantity': 'Total Quantity (Kgs)', 'Month': 'Month'},
                  markers=True)
    
    # Update layout for better visualization
    fig.update_layout(xaxis=dict(type='category'), height=400)
    
    return fig
