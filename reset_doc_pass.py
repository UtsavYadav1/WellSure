
import mysql.connector
from werkzeug.security import generate_password_hash

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor()
    
    email = "dr_test@medimind.com"
    password = "doctor123"
    hashed = generate_password_hash(password)
    
    # Check if exists
    cursor.execute("SELECT id FROM doctors WHERE email=%s", (email,))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("UPDATE doctors SET password=%s WHERE id=%s", (hashed, row[0]))
        print(f"Updated password for {email} to {password}")
    else:
        # Create if missing
        cursor.execute("""
            INSERT INTO doctors (name, email, password, specialization, city, address, fees) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ("Dr. Test", email, hashed, "General Physician", "Mumbai", "123 Test St", 500))
        print(f"Created doctor {email}")
        
    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
