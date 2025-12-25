
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email, password FROM users LIMIT 1")
    user = cursor.fetchone()
    if user:
        print(f"User found: {user['email']}")
    else:
        print("No users found.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
