import pandas as pd
from fpdf import FPDF

def download_csv(data):
    """
    Return CSV data for download.
    """
    return data.to_csv(index=False)

def generate_pdf_report(data, metrics):
    """
    Generate a PDF report with key metrics and insights.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add Metrics
    pdf.cell(200, 10, txt="Market Overview Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Total Imports: {metrics['total_imports']:,.0f} Kgs", ln=True)
    pdf.cell(200, 10, txt=f"Total Shipments: {metrics['total_shipments']}", ln=True)
    pdf.cell(200, 10, txt=f"Year-over-Year Growth: {metrics['yoy_growth']:.2f}%", ln=True)

    # Save and return the report
    file_path = "Market_Overview_Report.pdf"
    pdf.output(file_path)
    return file_path
