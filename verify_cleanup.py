
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor()
    
    # 1. Verify Specializations Count
    cursor.execute("SELECT COUNT(*) FROM specializations")
    spec_count = cursor.fetchone()[0]
    print(f"Total Specializations: {spec_count}")

    # 2. Verify Doctors Count for a specific type (should be 0)
    target = "Gastroenterologist"
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE specialization=%s", (target,))
    doc_count = cursor.fetchone()[0]
    print(f"Doctors for {target}: {doc_count}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
