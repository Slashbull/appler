def calculate_growth_metrics(data):
    """
    Function to calculate growth metrics such as Year-over-Year (YoY) growth and
    Month-over-Month (MoM) growth based on the imported data.
    """
    # Assuming 'data' has columns 'Year', 'Month', and 'Total Imports'
    yoy_growth = (data['Total Imports'].pct_change(periods=12).mean()) * 100  # Example YoY growth calculation
    mom_growth = (data['Total Imports'].pct_change(periods=1).mean()) * 100  # Example MoM growth calculation
    
    # You can modify this logic depending on your dataset and how you want to calculate the growth metrics
    return {
        'yoy_growth': yoy_growth,
        'mom_growth': mom_growth
    }
