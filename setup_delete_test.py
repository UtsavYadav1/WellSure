
import mysql.connector
from datetime import datetime, timedelta

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor(dictionary=True)
    
    # 1. Get a patient ID (any user)
    cursor.execute("SELECT id FROM users LIMIT 1")
    user = cursor.fetchone()
    if not user:
        print("No users found. Creating dummy user.")
        cursor.execute("INSERT INTO users (name, email, password) VALUES ('Dummy Patient', 'dummy@test.com', 'pass')")
        user_id = cursor.lastrowid
    else:
        user_id = user['id']

    # 2. Create Test Doctor
    doc_email = "delete_me@test.com"
    cursor.execute("SELECT id FROM doctors WHERE email=%s", (doc_email,))
    existing = cursor.fetchone()
    if existing:
        doc_id = existing['id']
        print(f"Test doctor exists: ID {doc_id}")
    else:
        cursor.execute("""
            INSERT INTO doctors (name, email, password, specialization, city, address, fees) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ("Dr. Delete Me", doc_email, "pass", "General Physician", "City", "Addr", 100))
        doc_id = cursor.lastrowid
        print(f"Created test doctor: ID {doc_id}")
    
    # 3. Create Appointment
    cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status) VALUES (%s, %s, CURDATE(), '10:00', 'Pending')", (user_id, doc_id))
    print(f"Created appointment for doctor {doc_id}")
    
    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
