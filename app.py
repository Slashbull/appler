import streamlit as st
import pandas as pd
from core import preprocess_data
import market_overview

# Sidebar Navigation
st.sidebar.title("Importer Dashboard")
st.sidebar.markdown("📂 Upload your data file to explore insights.")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

# Main Dashboard Logic
def main():
    """
    Main entry point for the Importer Dashboard.
    Handles file uploads, preprocessing, and module execution.
    """
    st.title("📊 Importer Dashboard")
    st.markdown(
        """
        Welcome to the **Importer Dashboard**! Analyze your import data using:
        - Interactive visualizations
        - Key metrics
        - Trends over time
        - AI-driven insights
        """
    )
    
    # Check if a file is uploaded
    if uploaded_file:
        try:
            # Load the uploaded file into a DataFrame
            if uploaded_file.name.endswith(".csv"):
                raw_data = pd.read_csv(uploaded_file)  # Read CSV file
            elif uploaded_file.name.endswith(".xlsx"):
                raw_data = pd.read_excel(uploaded_file)  # Read Excel file
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                st.stop()

            # Preprocess the data
            data = preprocess_data(raw_data)

            # Run the Market Overview module
            market_overview.run(data)

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
            st.stop()
    else:
        st.warning("📄 Please upload a data file to proceed.")

# Entry point
if __name__ == "__main__":
    main()
