def get_smart_alerts(data):
    """
    Generate smart alerts based on import data.
    Includes alerts for low imports, abnormal growth, and declining trends.
    
    Args:
        data (pd.DataFrame): Preprocessed import data.
    
    Returns:
        list: A list of alert messages.
    """
    alerts = []
    
    try:
        # Ensure required columns are present
        required_columns = ['Quantity', 'YoY Growth']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns for alerts: {', '.join(missing_columns)}")
        
        # Alert 1: Low import quantities
        low_imports_threshold = 1000  # Threshold for low imports
        low_imports = data[data['Quantity'] < low_imports_threshold]
        if not low_imports.empty:
            alerts.append(f"⚠️ Low import quantities detected for {len(low_imports)} entries. Check products or suppliers.")

        # Alert 2: High Year-over-Year (YoY) Growth
        yoy_growth_threshold = 30  # YoY growth threshold
        high_growth_alerts = data[data['YoY Growth'] > yoy_growth_threshold]
        if not high_growth_alerts.empty:
            alerts.append(f"🚀 High YoY growth detected for {len(high_growth_alerts)} entries. Review market demand.")

        # Alert 3: Declining imports (negative YoY Growth)
        declining_growth_alerts = data[data['YoY Growth'] < -20]  # Decline threshold: -20%
        if not declining_growth_alerts.empty:
            alerts.append(f"🔻 Declining imports detected for {len(declining_growth_alerts)} entries. Investigate reasons.")

        # Alert 4: Sudden drops in monthly imports
        monthly_totals = data.groupby(['Year', 'Month'])['Quantity'].sum().reset_index()
        if len(monthly_totals) > 1:
            monthly_totals['Change'] = monthly_totals['Quantity'].diff()
            sudden_drops = monthly_totals[monthly_totals['Change'] < -10000]  # Example threshold: -10,000
            if not sudden_drops.empty:
                alerts.append(f"📉 Sudden drops in monthly imports detected in {len(sudden_drops)} months. Review data.")

        # Return all generated alerts
        return alerts if alerts else ["✅ No critical alerts detected."]
    
    except Exception as e:
        return [f"❌ Error generating alerts: {str(e)}"]
