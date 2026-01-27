
import requests
from math import radians, cos, sin, asin, sqrt
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import database

# --- Geocoding (OpenStreetMap / Nominatim) ---
def geocode_address(address, city, pincode):
    """
    Geocodes an address using OpenStreetMap's Nominatim API.
    Returns (lat, lng) as floats, or (None, None) if not found.
    Tries multiple query formats to maximize hit rate.
    """
    queries = [
        f"{address}, {city}, {pincode}",
        f"{city}, {pincode}",
        f"{city}"
    ]
    
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        'User-Agent': 'MediMindAI/1.0 (educational_project; contact_admin@wellsure.app)',
        'Accept-Language': 'en'
    }

    for q in queries:
        try:
            params = {
                'q': q,
                'format': 'json',
                'limit': 1
            }
            # Add timeout to prevent hanging
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    return lat, lon
        except Exception as e:
            # Log as warning but don't crash. Network unreachable is common in free tiers.
            print(f"Geocoding Warning: Could not fetch coordinates for '{q}' ({e})")
            
    return None, None

# --- Distance Calculation (Haversine) ---
def distance_km(lat1, lon1, lat2, lon2):
    """
    Calculates the Great Circle distance between two points in kilometers.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 9999.0 # Fallback for sorting

    try:
        # Check if values are valid numbers (strings or floats)
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
        
        # Convert degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return round(c * r, 1)
    except Exception as e:
        print(f"Distance Calc Error: {e}")
        return 9999.0

# --- Activity Logger ---
def log_activity(user_id, role, action, details=""):
    """
    Log user activity to the database.
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO activity_logs (user_id, role, action, details) VALUES (%s, %s, %s, %s)",
            (user_id, role, action, details)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Logging Error: {e}")

# --- PDF Report Generator ---
def generate_pdf_report(filepath, patient_name, disease, symptoms, description, medications, precautions, diets, workouts, age=None, gender=None):
    """
    Generate a professional PDF report for the medical prediction.
    Updated for WellSure branding with optional age/gender context.
    """
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, spaceAfter=20, textColor=colors.darkblue)
    story.append(Paragraph("WellSure - Medical Report", title_style))
    story.append(Spacer(1, 12))

    # Patient Details
    story.append(Paragraph(f"<b>Patient Name:</b> {patient_name}", styles['Normal']))
    
    # Age and Gender (if provided)
    if age or gender:
        age_gender_parts = []
        if age:
            age_gender_parts.append(f"Age: {age}")
        if gender:
            age_gender_parts.append(f"Gender: {gender.capitalize()}")
        story.append(Paragraph(f"<b>{' | '.join(age_gender_parts)}</b>", styles['Normal']))
    
    story.append(Paragraph(f"<b>Date:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 20))

    # Diagnosis Section
    story.append(Paragraph("Diagnosis Results", styles['Heading2']))
    story.append(Paragraph(f"<b>Predicted Disease:</b> {disease}", styles['Normal']))
    story.append(Paragraph(f"<b>Symptoms Reported:</b> {symptoms}", styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Description:</b> {description}", styles['BodyText']))
    story.append(Spacer(1, 20))

    # Treatment Plan
    story.append(Paragraph("Recommended Treatment Plan", styles['Heading2']))
    
    # Medications
    story.append(Paragraph("<b>Medications:</b>", styles['Heading3']))
    if isinstance(medications, list):
        meds_text = ", ".join(medications)
    else:
        meds_text = str(medications)
    story.append(Paragraph(meds_text, styles['Normal']))
    story.append(Spacer(1, 10))

    # Precautions
    story.append(Paragraph("<b>Precautions:</b>", styles['Heading3']))
    if isinstance(precautions, list):
        pre_text = "\n".join([f"• {p}" for p in precautions])
    else:
        pre_text = str(precautions)
    story.append(Paragraph(pre_text, styles['Normal']))
    story.append(Spacer(1, 10))

    # Diet & Workout - formatting as Paragraphs to allow wrapping
    diet_text = ", ".join(eval(diets)) if isinstance(diets, str) else ", ".join(diets)
    workout_text = ", ".join(eval(workouts)) if isinstance(workouts, str) else ", ".join(workouts)
    
    data = [
        [Paragraph("Dietary Advice", styles['Heading3']), Paragraph("Workout Recommendations", styles['Heading3'])],
        [Paragraph(diet_text, styles['BodyText']), Paragraph(workout_text, styles['BodyText'])]
    ]
    t = Table(data, colWidths=[250, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 30))

    # Disclaimer
    story.append(Paragraph("<b>Disclaimer:</b> This report is generated by AI and should not replace professional medical advice. Please consult a doctor.", styles['Italic']))

    doc.build(story)
    return True


def process_doctors_data(doctors_list, patient_lat, patient_lng):
    """
    Calculates distances for doctors and ensures JSON serializability.
    Modifies the list in-place or returns processed list.
    """
    from datetime import timedelta
    
    for d in doctors_list:
        # Distance
        if patient_lat and patient_lng and d.get('lat') and d.get('lng'):
             d['distance'] = distance_km(patient_lat, patient_lng, d['lat'], d['lng'])
        else:
             d['distance'] = 99999.0
             
        # JSON Serialization (timedelta)
        for k, v in list(d.items()):
            if isinstance(v, timedelta):
                d[k] = str(v)
                
    # Sort
    doctors_list.sort(key=lambda x: x.get('distance', 99999.0))
    return doctors_list
