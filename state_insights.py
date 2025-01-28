import streamlit as st
import plotly.express as px

def run(data):
    """
    State-Wise Insights Submodule: Displays state-wise contributions and maps.
    """
    st.subheader("📍 State-Wise Insights")

    # Map State Abbreviations
    STATE_ABBREVIATIONS = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UK": "Uttarakhand",
    "WB": "West Bengal",
    "JK": "Jammu & Kashmir",
    "LD": "Lakshadweep",
    "PY": "Puducherry",
    "CH": "Chandigarh",
    "AN": "Andaman & Nicobar Islands",
    "DN": "Dadra & Nagar Haveli",
    "DL": "Delhi",
    "INDIA": "India"  # Special handling for cases where state is set as "India"
    }
    data['State'] = data['State'].map(STATE_ABBREVIATIONS).fillna(data['State'])

    # State-Wise Data
    state_data = data.groupby('State')['Quantity'].sum().reset_index()
    state_data = state_data[state_data['State'] != "India"]

    # Plot Bar Chart
    state_fig = px.bar(
        state_data,
        x='State',
        y='Quantity',
        title="State-Wise Import Contributions",
        labels={'Quantity': 'Total Quantity (Kgs)', 'State': 'State'},
        template="plotly_white"
    )
    st.plotly_chart(state_fig, use_container_width=True)
