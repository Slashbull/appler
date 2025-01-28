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

def generate_unique_ids(data):
    """
    Generate unique IDs for importers and exporters based on their names.
    Ensures consistent tracking and easy future use for AI/ML applications.
    """
    data['Importer ID'] = data['Consignee Name'].apply(lambda x: (x[:6].upper() + str(abs(hash(x)) % 1000000)))
    data['Exporter ID'] = data['Exporter Name'].apply(lambda x: (x[:6].upper() + str(abs(hash(x)) % 1000000)))
    return data

def load_state_mapping():
    """
    Load state abbreviations from a JSON file for better scalability.
    """
    try:
        if os.path.exists("states.json"):
            with open("states.json", "r") as file:
                return json.load(file)
        else:
            return {
                "MH": "Maharashtra",
                "JK": "Jammu & Kashmir",
                "TG": "Telangana",
                "UP": "Uttar Pradesh",
                "MP": "Madhya Pradesh"
            }
    except Exception as e:
        logging.error(f"Error loading state mapping: {e}")
        return {}

def preprocess_data(data):
    """
    Preprocess the data by standardizing columns, handling missing values, and generating derived fields.
    """
    try:
        # Rename columns to standard names
        column_mapping = {
            'Quantity': 'Quantity',
            'Year': 'Year',
            'Month': 'Month',
            'Consignee Name': 'Consignee Name',
            'Exporter Name': 'Exporter Name',
            'State': 'State',
        }
        data.rename(columns=column_mapping, inplace=True)

        # Validate required columns
        required_columns = list(column_mapping.values())
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Process 'Date' column
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data = data.dropna(subset=['Date'])

        # Clean 'Quantity' column
        if data['Quantity'].dtype == 'object':
            data['Quantity'] = data['Quantity'].str.extract(r'(\d+)').astype(float)

        # Drop rows with missing critical values
        data = data.dropna(subset=['Quantity', 'Consignee Name', 'Exporter Name', 'State'])

        # Add derived columns
        data['Year'] = data['Date'].dt.year
        data['Month'] = data['Date'].dt.month_name()

        # Generate unique IDs
        data = generate_unique_ids(data)

        return data

    except Exception as e:
        logging.error(f"Error in preprocessing: {e}")
        raise ValueError(f"Preprocessing error: {e}")

def load_google_sheet(sheet_url):
    """
    Load data from a Google Sheets URL. The sheet must be published in CSV format.
    """
    try:
        if "docs.google.com/spreadsheets" not in sheet_url:
            raise ValueError("Invalid Google Sheets URL. Please provide a valid link.")
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        data = pd.read_csv(export_url)
        return preprocess_data(data)
    except Exception as e:
        logging.error(f"Error loading Google Sheet: {e}")
        raise ValueError(f"Error loading Google Sheet: {e}")

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

def get_filtered_data(data, state=None, month=None, year=None, importer=None, exporter=None):
    """
    Apply filters to the data based on state, month, year, importer, or exporter.
    """
    try:
        if state and state != "All":
            data = data[data['State'] == state]
        if month and month != "All":
            data = data[data['Month'] == month]
        if year and year != "All":
            data = data[data['Year'] == year]
        if importer and importer != "All":
            data = data[data['Consignee Name'] == importer]
        if exporter and exporter != "All":
            data = data[data['Exporter Name'] == exporter]

        return data
    except Exception as e:
        logging.error(f"Error in filtering data: {e}")
        raise ValueError(f"Filtering error: {e}")

def generate_pdf_report(filtered_data, metrics):
    """
    Example placeholder function for generating PDF reports.
    """
    # Implement PDF report generation logic
    pass

def download_csv(filtered_data):
    """
    Generate a CSV file from the filtered data for download.
    """
    return filtered_data.to_csv(index=False)
