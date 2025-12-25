import pandas as pd
import traceback

files = ['symptoms_df_clean.csv', 'precautions_clean.csv', 'workout_clean.csv', 
         'description.csv', 'medications_clean.csv', 'diet_clean.csv', 
         'doctor_specialization_clean.csv']

for f in files:
    try:
        df = pd.read_csv(f)
        print(f'{f}: OK ({len(df)} rows)')
    except Exception as e:
        print(f'{f}: ERROR')
        traceback.print_exc()
