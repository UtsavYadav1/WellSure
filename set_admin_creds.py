
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
    
    email = "admin@medimind.ai"
    password = "Admin@123"
    hashed = generate_password_hash(password)
    
    # Check if exists
    cursor.execute("SELECT id FROM admins WHERE email=%s", (email,))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("UPDATE admins SET password=%s WHERE id=%s", (hashed, row[0]))
        print(f"Updated password for {email}")
    else:
        cursor.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", ("Admin", email, hashed))
        print(f"Created admin {email}")
        
    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
