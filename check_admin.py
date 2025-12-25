
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins LIMIT 1")
    admin = cursor.fetchone()
    if admin:
        print(f"Admin found: {admin['email']}")
    else:
        print("No admin found. Creating one...")
        from werkzeug.security import generate_password_hash
        hashed = generate_password_hash("admin123")
        cursor.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", ("Admin", "admin@medimind.com", hashed))
        conn.commit()
        print("Admin created: admin@medimind.com / admin123")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
