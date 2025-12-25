
import database

def check_columns():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("DESCRIBE doctors")
        columns = cursor.fetchall()
        for col in columns:
            print(f"DTO: {col['Field']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_columns()
