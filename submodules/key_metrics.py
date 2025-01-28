import pandas as pd

def calculate_kpis(data):
    """
    Calculate Key Performance Indicators (KPIs) from the given dataset.
    """
    try:
        # Check required columns
        required_columns = ['Quantity', 'Year', 'Consignee Name', 'Exporter Name', 'State']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Calculate KPIs
        total_imports = data['Quantity'].sum()
        total_shipments = len(data)
        unique_importers = data['Consignee Name'].nunique()
        unique_exporters = data['Exporter Name'].nunique()
        unique_states = data['State'].nunique()

        # Calculate YoY growth
        yoy_growth = calculate_yoy_growth(data)

        # Calculate MoM growth
        mom_growth = calculate_mom_growth(data)

        # Top contributors
        top_importer = data.groupby('Consignee Name')['Quantity'].sum().idxmax() if not data.empty else "N/A"
        top_exporter = data.groupby('Exporter Name')['Quantity'].sum().idxmax() if not data.empty else "N/A"
        top_state = data.groupby('State')['Quantity'].sum().idxmax() if not data.empty else "N/A"

        return {
            'Total Imports': total_imports,
            'Total Shipments': total_shipments,
            'Unique Importers': unique_importers,
            'Unique Exporters': unique_exporters,
            'Unique States': unique_states,
            'YoY Growth': yoy_growth,
            'MoM Growth': mom_growth,
            'Top Importer': top_importer,
            'Top Exporter': top_exporter,
            'Top State': top_state,
        }

    except Exception as e:
        logging.error(f"Error in KPI calculation: {e}")
        raise ValueError(f"Error calculating KPIs: {e}")
        
def calculate_yoy_growth(data):
    """
    Calculate Year-over-Year (YoY) Growth based on the data.

    Args:
        data (pd.DataFrame): The input data containing yearly import records.

    Returns:
        float: Year-over-Year growth percentage.
    """
    try:
        # Group by year and calculate total imports
        yearly_totals = data.groupby('Year')['Quantity'].sum()

        # Ensure at least two years are present
        if len(yearly_totals) < 2:
            return 0.0

        # Calculate YoY growth
        last_year = yearly_totals.index[-1]
        previous_year = yearly_totals.index[-2]
        yoy_growth = ((yearly_totals[last_year] - yearly_totals[previous_year]) /
                      yearly_totals[previous_year]) * 100

        return round(yoy_growth, 2)
    except Exception as e:
        return 0.0


def calculate_mom_growth(data):
    """
    Calculate Month-over-Month (MoM) Growth based on the data.

    Args:
        data (pd.DataFrame): The input data containing monthly import records.

    Returns:
        float: Month-over-Month growth percentage.
    """
    try:
        # Group by year and month to calculate monthly totals
        monthly_data = data.groupby(['Year', 'Month'])['Quantity'].sum().reset_index()

        # Ensure at least two months are present
        if len(monthly_data) < 2:
            return 0.0

        # Calculate MoM growth
        last_month_quantity = monthly_data.iloc[-1]['Quantity']
        previous_month_quantity = monthly_data.iloc[-2]['Quantity']
        mom_growth = ((last_month_quantity - previous_month_quantity) / previous_month_quantity) * 100

        return round(mom_growth, 2)
    except Exception as e:
        return 0.0
