import pandas as pd
from cryptography.fernet import Fernet
import os
import logging
import json

# Setup Logging
logging.basicConfig(
    filename="dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Encryption Key File
KEY_FILE = "encryption_key.key"

def load_key():
    """
    Load or generate an encryption key for securing sensitive data.
    """
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as file:
            file.write(Fernet.generate_key())
    with open(KEY_FILE, "rb") as file:
        return file.read()

cipher = Fernet(load_key())

EXPECTED_COLUMNS = {
    "Quantity": "Quantity",
    "Year": "Year",
    "Month": "Month",
    "Consignee Name": "Consignee",
    "Exporter Name": "Exporter",
    "State": "Consignee State"
}

def dynamic_column_mapping(data):
    """
    Allow user to map columns dynamically if mismatched.
    """
    st.info("Mapping dataset columns. Please map your dataset columns to the expected format.")
    mapping = {}
    for expected, display_name in EXPECTED_COLUMNS.items():
        st.text(f"Expected: {expected}")
        user_column = st.selectbox(f"Select column for '{expected}'", options=["None"] + list(data.columns))
        if user_column != "None":
            mapping[user_column] = display_name
    return mapping

def preprocess_data(data):
    """
    Preprocess the data by standardizing columns, handling missing values, and generating derived fields.
    """
    try:
        # Map columns dynamically
        st.info("Detecting column names...")
        mapping = dynamic_column_mapping(data)
        if not mapping:
            raise ValueError("Column mapping failed. Please ensure all required columns are mapped.")
        
        data.rename(columns=mapping, inplace=True)

        # Validate required columns
        missing_columns = [col for col in EXPECTED_COLUMNS.values() if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns after mapping: {', '.join(missing_columns)}")

        # Process 'Quantity' column
        if 'Quantity' in data.columns:
            data['Quantity'] = data['Quantity'].str.extract(r'(\d+)').astype(float)

        # Add derived columns
        if 'Date' in data.columns:
            data['Year'] = pd.to_datetime(data['Date']).dt.year
            data['Month'] = pd.to_datetime(data['Date']).dt.month_name()

        return data

    except Exception as e:
        logging.error(f"Error in preprocessing: {e}")
        raise ValueError(f"Preprocessing error: {e}")

def load_uploaded_file(file):
    """
    Load and preprocess data from an uploaded file (CSV or Excel).
    """
    try:
        if file.name.endswith(".csv"):
            data = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            data = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        return preprocess_data(data)
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        raise ValueError(f"Error loading file: {e}")
