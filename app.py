import streamlit as st
from core import load_uploaded_file, dynamic_column_mapping_ui

# Sidebar Navigation
st.sidebar.title("Importer Dashboard")
st.sidebar.markdown("📂 Upload your data file to explore insights.")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

def main():
    st.title("📊 Importer Dashboard")
    if uploaded_file:
        try:
            # Load the uploaded file into a DataFrame
            if uploaded_file.name.endswith(".csv"):
                raw_data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                raw_data = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                st.stop()

            # Get dynamic column mapping
            mapping = dynamic_column_mapping_ui(raw_data)

            # Preprocess data with mapping
            data = load_uploaded_file(uploaded_file, mapping)
            st.success("Data loaded and processed successfully!")
            st.dataframe(data.head())  # Display the first few rows

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
            st.stop()
    else:
        st.warning("📄 Please upload a data file to proceed.")

if __name__ == "__main__":
    main()
