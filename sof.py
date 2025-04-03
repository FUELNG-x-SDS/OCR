import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer

# Updated list of activities in order (matching sample)
activities = [
    "EOSP",
    "All equipment rigged and ready",
    "NOR tendered by LBV",
    "NOR tendered by RV",
    "Mooring",
    "Gangway landed",
    "Hose(s) or arm connection",
    "Hose(s) or arm pressure tested",
    "Hose(s) or arm purged with N2",
    "Pre-operations meeting",
    "WarmESD",
    "Opening CTS",
    "Hose(s) or arm and lines cool-dow",
    "Cold ESD tests",
    "Open BOG valve to shore",
    "Ramp-up bunker transfer",
    "Bulk transfer",
    "Ramp-down until loading / discharge complete",
    "Draining of hose(s) or arm",
    "Close BOG valve to shore",
    "Hose(s) or arm purged",
    "Closing CTS",
    "Post operation meeting",
    "Hose(s) or arm disconnected",
    "Documentation completed",
    "IAPH checklist part E",
    "Pilot on board",
    "Unmooring",
    "FAOP"
]

# Activities that must have the "Started" field as dashes.
special_activities = [
    "EOSP",
    "All equipment rigged and ready",
    "NOR tendered by LBV",
    "NOR tendered by RV",
    "WarmESD",
    "Hose(s) or arm and lines cool-dow",
    "Ramp-up bunker transfer",
    "IAPH checklist part E",
    "Hose(s) or arm disconnected",
    "Pilot on board"
]

def generate_times(start_time, activities):
    """
    Generate realistic 'Started' and 'Completed' times for each activity.
    For activities in special_activities, the "Started" field is set to "—".
    Otherwise, times are generated normally.
    Times are formatted as 'YYYY-MM-DD HH:MM LT'.
    """
    rows = []
    current_time = start_time

    for activity in activities:
        # Determine if the "Started" field should be blank (dash)
        if activity in special_activities:
            started_str = "—"
        else:
            started_str = current_time.strftime("%Y-%m-%d %H:%M LT")
        
        # Random duration for the activity (in minutes)
        duration = random.randint(5, 15)
        # Always compute completed time
        current_time += timedelta(minutes=duration)
        completed_str = current_time.strftime("%Y-%m-%d %H:%M LT")
        
        rows.append((activity, started_str, completed_str))
        
        # Add a small random gap (1-4 minutes) between activities
        gap = random.randint(1, 4)
        current_time += timedelta(minutes=gap)
    
    return rows

def create_sof_pdf(filename, sof_data):
    """
    Create a single SOF PDF document with the given data.
    sof_data: list of (activity, started, completed) tuples.
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    header_style = styles["Heading2"]
    
    # Header information (adjust as necessary)
    header_text = f"""
    <b>LNG Loading Time Sheet - Statement of Facts</b><br/><br/>
    <b>LNG Bunker Vessel:</b> FUELNG VENOSA<br/>
    <b>Terminal:</b> SLNG Terminal<br/>
    <b>Berth:</b> —<br/>
    <b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}<br/>
    <b>Port:</b> Singapore, Singapore<br/><br/>
    """
    elements.append(Paragraph(header_text, header_style))
    elements.append(Spacer(1, 12))
    
    # Build table data
    table_data = [["Activity", "Started", "Completed"]]
    for row in sof_data:
        table_data.append(list(row))
    
    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    table = Table(table_data, colWidths=[220, 120, 120])
    table.setStyle(table_style)
    elements.append(table)
    
    doc.build(elements)

def main():
    output_folder = "FueLNG_SOF_PDFs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Generate 15 separate SOF PDFs
    for i in range(1, 16):
        # Random start time between 07:00 and 08:00 on 24 March 2025
        start_hour = random.randint(7, 8)
        start_minute = random.randint(0, 59)
        start_time = datetime(2025, 3, 24, start_hour, start_minute)
        
        sof_data = generate_times(start_time, activities)
        filename = os.path.join(output_folder, f"SOF_Document_{i}.pdf")
        create_sof_pdf(filename, sof_data)
        print(f"Generated: {filename}")

if __name__ == "__main__":
    main()
