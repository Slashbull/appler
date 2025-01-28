import plotly.express as px

def plot_contributions(data, contributor_type):
    """
    Generate a bar chart for contributions by importer or exporter.
    """
    contributor_data = data.groupby(contributor_type)['Quantity'].sum().reset_index()
    chart = px.bar(
        contributor_data,
        x=contributor_type,
        y='Quantity',
        title=f"{contributor_type} Contributions",
        labels={"Quantity": "Total Quantity (Kgs)", contributor_type: contributor_type},
    )
    return chart
