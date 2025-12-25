
import pandas as pd
import mysql.connector
from werkzeug.security import generate_password_hash
import random

def populate_doctors():
    try:
        # Load CSV
        df = pd.read_csv("doctor_specialization_clean.csv")
        # Get unique specializations (handling slashed ones like "Allergist/Immunologist")
        specs = set()
        for s in df['Doctor'].unique():
            if '/' in s:
                parts = s.split('/')
                for p in parts:
                    specs.add(p.strip())
            else:
                specs.add(s.strip())
        
        print(f"Found {len(specs)} unique specializations: {specs}")

        # Connect to DB
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="medimind"
        )
        cursor = conn.cursor()

        # Check existing
        cursor.execute("SELECT specialization FROM doctors")
        existing_specs = set([row[0] for row in cursor.fetchall()])
        print(f"Existing in DB: {existing_specs}")

        new_specs = specs - existing_specs
        
        # Insert missing
        for spec in new_specs:
            name = f"Dr. {spec.split()[0]} Specialist"
            email = f"{spec.lower().replace(' ', '')}@medimind.com"
            password = generate_password_hash("doctor123")
            city = random.choice(["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"])
            address = f"Clinic {random.randint(1, 100)}, {city}"
            
            # Using basic columns + upgrades if they exist
            # We'll try to insert with basic + address/city. If fails, we might need to handle schema diffs.
            # Assuming schema_upgrade.sql was run or main.py works.
            
            try:
                cursor.execute("""
                    INSERT INTO doctors 
                    (name, email, password, specialization, experience_years, fees, city, address, phone, available_start_time, available_end_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    name, email, password, spec, 
                    random.randint(5, 20), 
                    random.choice([500, 800, 1000, 1500]), 
                    city, address, "9876543210", 
                    "10:00", "18:00"
                ))
                print(f"Inserted: {name} ({spec})")
            except mysql.connector.Error as err:
                 # If column missing error, fallback to basic
                 print(f"Insertion failed for {spec}: {err}. Trying basic insert.")
                 cursor.execute("""
                    INSERT INTO doctors 
                    (name, email, password, specialization, experience_years, fees, available_start_time, available_end_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    name, email, password, spec, 
                    random.randint(5, 20), 
                    random.choice([500, 800, 1000, 1500]), 
                    "10:00", "18:00"
                ))

        conn.commit()
        print("Population complete.")
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    populate_doctors()
