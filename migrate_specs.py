
import mysql.connector
import pandas as pd

def migrate_specializations():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="medimind"
        )
        cursor = conn.cursor()

        # 1. Cleanup Dummy Doctors
        # We identified them by the email pattern @medimind.com (from populate_doctors.py)
        # Be careful not to delete real doctors if they used that domain, but for this context it's safe as it was just added.
        print("Cleaning up dummy doctors...")
        cursor.execute("DELETE FROM doctors WHERE email LIKE '%@medimind.com'")
        deleted_count = cursor.rowcount
        print(f"Removed {deleted_count} dummy doctor records.")

        # 2. Create Specializations Table
        print("Creating specializations table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS specializations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            )
        """)

        # 3. Populate Specializations from CSV
        print("Populating specializations...")
        df = pd.read_csv("doctor_specialization_clean.csv")
        specs = set()
        for s in df['Doctor'].unique():
            if '/' in s:
                parts = s.split('/')
                for p in parts:
                    specs.add(p.strip())
            else:
                specs.add(s.strip())
        
        inserted_count = 0
        for spec in specs:
            try:
                cursor.execute("INSERT IGNORE INTO specializations (name) VALUES (%s)", (spec,))
                inserted_count += cursor.rowcount
            except Exception as e:
                print(f"Error inserting {spec}: {e}")
        
        print(f"Inserted/Verified {inserted_count} specializations.")

        conn.commit()
        conn.close()
        print("Migration successful.")

    except Exception as e:
        print(f"Migration Error: {e}")

if __name__ == "__main__":
    migrate_specializations()
