from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def read_linter_output(file_path):
    # Read the Super Linter output from the file
    with open(file_path, 'r') as file:
        linter_output = file.read()
    return linter_output

def extract_data(linter_output):
    # Parse the Super Linter output and extract relevant data
    errors = []
    lines = linter_output.split('\n')
    for line in lines:
        if '[ERROR]' in line or '[FATAL]' in line:
            if '[ERROR]' in line:
                error_message = line.split('[ERROR]')[1].strip()
            elif '[FATAL]' in line:
                error_message = line.split('[FATAL]')[1].strip()
            errors.append(error_message)
    return errors

def generate_pdf_report(data):
    # Generate a PDF report using the extracted data
    doc = SimpleDocTemplate("code_analysis_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    report_content = []

    # Add title
    report_content.append(Paragraph("Code Analysis Report", styles['Title']))

    # Add data table
    data_table = Table([["Files with Errors"]] + [[file] for file in data])
    data_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    report_content.append(data_table)

    # Build the PDF report
    doc.build(report_content)

if __name__ == "__main__":
    # Read Super Linter output from file
    linter_output = read_linter_output("linter_output.txt")

    # Extract relevant data
    data = extract_data(linter_output)

    # Generate PDF report with extracted data
    generate_pdf_report(data)
