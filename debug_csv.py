import traceback
import sys

try:
    import pandas as pd
    print("pandas imported OK")
    
    print("Loading symptoms_df_clean.csv...")
    sym_des = pd.read_csv("symptoms_df_clean.csv")
    print(f"  OK: {len(sym_des)} rows")
    
    print("Loading precautions_clean.csv...")
    precautions = pd.read_csv("precautions_clean.csv")
    print(f"  OK: {len(precautions)} rows")
    
    print("Loading workout_clean.csv...")
    workout = pd.read_csv("workout_clean.csv")
    print(f"  OK: {len(workout)} rows")
    
    print("Loading description.csv...")
    description = pd.read_csv("description.csv")
    print(f"  OK: {len(description)} rows")
    
    print("Loading medications_clean.csv...")
    medications = pd.read_csv("medications_clean.csv")
    print(f"  OK: {len(medications)} rows")
    
    print("Loading diet_clean.csv...")
    diets = pd.read_csv("diet_clean.csv")
    print(f"  OK: {len(diets)} rows")
    
    print("Loading doctor_specialization_clean.csv...")
    doctors = pd.read_csv("doctor_specialization_clean.csv")
    print(f"  OK: {len(doctors)} rows")
    
    print("\nALL CSVs loaded successfully!")
    
    # Now try importing main
    print("\nTrying to import main modules...")
    import database
    print("  database OK")
    
    import utils
    print("  utils OK")
    
    from rules_engine import RulesEngine
    print("  rules_engine OK")
    
    print("\nAll imports successful!")
    
except Exception as e:
    print(f"\n\nERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
