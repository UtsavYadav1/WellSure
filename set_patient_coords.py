
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor()
    # Mumbai coordinates
    lat = 19.0760
    lng = 72.8777
    cursor.execute("UPDATE users SET lat=%s, lng=%s WHERE email='test@test.com'", (lat, lng))
    conn.commit()
    print(f"Updated test@test.com with coords: {lat}, {lng}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
