import pandas as pd
import os

# Check precautions line count and structure
filepath = 'precautions_clean.csv'
print(f'File size: {os.path.getsize(filepath)} bytes')

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')
print(f'\nHeader: {lines[0].strip()}')
print(f'Header columns: {len(lines[0].strip().split(","))}')

print('\nChecking problematic lines around 72:')
for i in range(70, min(78, len(lines))):
    line = lines[i].strip()
    cols = len(line.split(','))
    print(f'Line {i+1}: {cols} cols - {line[:60]}...')

print('\nAttempting to load with pandas...')
try:
    df = pd.read_csv(filepath)
    print(f'SUCCESS: {len(df)} rows loaded')
except Exception as e:
    print(f'ERROR: {e}')
