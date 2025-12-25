"""
Database migration script for appointment flow enhancements.
Run this script once to add required columns.
"""
import mysql.connector

def run_migrations():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medimind"
    )
    cursor = conn.cursor()
    
    migrations = [
        # Add payment_mode to appointments
        """ALTER TABLE appointments ADD COLUMN payment_mode 
           ENUM('online', 'at_clinic') DEFAULT 'at_clinic'""",
        
        # Add meeting_link to appointments
        """ALTER TABLE appointments ADD COLUMN meeting_link 
           VARCHAR(500) DEFAULT NULL""",
        
        # Add default_meeting_link to doctors
        """ALTER TABLE doctors ADD COLUMN default_meeting_link 
           VARCHAR(500) DEFAULT NULL"""
    ]
    
    for sql in migrations:
        try:
            cursor.execute(sql)
            print(f"✓ Executed: {sql[:50]}...")
        except mysql.connector.errors.ProgrammingError as e:
            if "Duplicate column name" in str(e):
                print(f"⊘ Column already exists, skipping...")
            else:
                print(f"✗ Error: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("\nMigration complete!")

if __name__ == "__main__":
    run_migrations()
