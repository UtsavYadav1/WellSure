
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
    
    # 1. Ensure Admin
    hashed_admin = generate_password_hash("admin123")
    cursor.execute("SELECT id FROM admins WHERE email='admin@medimind.com'")
    if cursor.fetchone():
        cursor.execute("UPDATE admins SET password=%s WHERE email='admin@medimind.com'", (hashed_admin,))
        print("Admin password reset to 'admin123'.")
    else:
        cursor.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", ("Admin", "admin@medimind.com", hashed_admin))
        print("Admin created: admin@medimind.com / admin123")

    # 2. Ensure Doctor
    hashed_doc = generate_password_hash("doctor123")
    cursor.execute("SELECT id FROM doctors WHERE email='dr_test@medimind.com'")
    if cursor.fetchone():
        cursor.execute("UPDATE doctors SET password=%s WHERE email='dr_test@medimind.com'", (hashed_doc,))
        print("Doctor password reset to 'doctor123'.")
    else:
        # Need a valid spec - use 'General Physician' which we know is in CSV
        cursor.execute("""
            INSERT INTO doctors (name, email, password, specialization, city, address, fees) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ("Dr. Test", "dr_test@medimind.com", hashed_doc, "General Physician", "Mumbai", "123 Test St", 500))
        print("Doctor created: dr_test@medimind.com / doctor123")
        
    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
