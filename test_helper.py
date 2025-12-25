import pandas as pd

# Load CSVs
description = pd.read_csv("description.csv")
precautions = pd.read_csv("precautions_clean.csv")
medications = pd.read_csv('medications_clean.csv')
diets = pd.read_csv("diet_clean.csv")
workout = pd.read_csv("workout_clean.csv")
doctors = pd.read_csv("doctor_specialization_clean.csv")

# Test diseases
test_diseases = ["Tuberculosis", "COVID-19", "Meningitis", "Anemia", "Conjunctivitis"]

for dis in test_diseases:
    print(f"\n--- Testing '{dis}' ---")
    
    # Check description
    desc = description[description['Disease'] == dis]
    print(f"Description found: {not desc.empty}")
    if not desc.empty:
        print(f"  Value: {desc['Description'].values[0][:50]}...")
    
    # Check precautions
    prec = precautions[precautions['Disease'] == dis]
    print(f"Precautions found: {not prec.empty}")
    
    # Check medications
    med = medications[medications['Disease'] == dis]
    print(f"Medications found: {not med.empty}")
    
    # Check workout (lowercase 'disease' column!)
    wrk = workout[workout['disease'] == dis]
    print(f"Workout found: {not wrk.empty}")
    
    # Check doctors
    doc = doctors[doctors['Disease'] == dis]
    print(f"Doctor found: {not doc.empty}")
