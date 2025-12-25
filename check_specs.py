
import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT specialization FROM doctors ORDER BY specialization ASC")
    specs = [row[0] for row in cursor.fetchall()]
    print(f"Total Specializations: {len(specs)}")
    print("List:")
    for s in specs:
        print(f"- {s}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
