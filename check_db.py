
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    print("DB Connection Successful")
    conn.close()
except Exception as e:
    print(f"DB Connection Failed: {e}")
