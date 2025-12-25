
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
    
    email = "test@test.com"
    password = "test"
    hashed = generate_password_hash(password)
    
    # Check if exists
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        print("User exists, updating password...")
        cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed, email))
    else:
        print("Creating new user...")
        # Need mandatory fields: name, email, password, city, address, pincode, medical_history, lat, lng
        cursor.execute("""
            INSERT INTO users (name, email, password, city, address, pincode, medical_history, lat, lng)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ("Test User", email, hashed, "Test City", "Test Address", "123456", "None", 0.0, 0.0))
    
    conn.commit()
    print("User setup complete: test@test.com / test")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
