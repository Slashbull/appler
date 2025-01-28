import plotly.express as px
import pandas as pd

def plot_state_contributions(data):
    """
    Plot state contributions as a bar chart.
    
    Args:
        data (pd.DataFrame): The data containing 'State' and 'Quantity'.
    
    Returns:
        fig (plotly.graph_objs.Figure): A Plotly figure object.
    """
    # Aggregate data by state and sum the quantities
    state_data = data.groupby('State')['Quantity'].sum().reset_index()
    
    # Create a bar chart
    fig = px.bar(state_data, x='State', y='Quantity', 
                 title="State Contributions to Imports",
                 labels={'Quantity': 'Total Quantity (Kgs)', 'State': 'State'},
                 color='Quantity', color_continuous_scale='Viridis')
    
    fig.update_layout(height=400, xaxis_title="State", yaxis_title="Total Quantity (Kgs)")
    
    return fig


def plot_state_heatmap(data):
    """
    Plot a heatmap of state contributions over time (Month).
    
    Args:
        data (pd.DataFrame): The data containing 'State', 'Month', and 'Quantity'.
    
    Returns:
        fig (plotly.graph_objs.Figure): A Plotly figure object.
    """
    # Aggregate data by state and month
    state_month_data = data.groupby(['State', 'Month'])['Quantity'].sum().reset_index()
    
    # Pivot data for heatmap format
    heatmap_data = state_month_data.pivot(index='State', columns='Month', values='Quantity')
    
    # Create a heatmap
    fig = px.imshow(heatmap_data, title="State Contributions Heatmap",
                    labels={'x': 'Month', 'y': 'State', 'color': 'Total Quantity (Kgs)'},
                    color_continuous_scale='Viridis')
    
    fig.update_layout(height=600)
    
    return fig
