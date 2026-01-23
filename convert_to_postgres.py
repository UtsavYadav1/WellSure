"""
MySQL Backup to PostgreSQL Converter
Run this script to convert backup.sql (MySQL) to backup_postgres.sql (PostgreSQL/Supabase)
"""
import re
import os

def convert_mysql_to_postgres(input_file='backup.sql', output_file='backup_postgres.sql'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run dump_db.py first.")
        return False
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Conversions:
    # 1. Remove MySQL-specific statements
    content = re.sub(r'SET FOREIGN_KEY_CHECKS\s*=\s*\d+;', '', content)
    content = re.sub(r'DROP TABLE IF EXISTS.*?;', '', content)
    content = re.sub(r'CREATE TABLE.*?;', '', content, flags=re.DOTALL)  # Schema created separately
    
    # 2. Fix AUTO_INCREMENT (not needed in inserts)
    # 3. Fix backticks to double quotes
    content = content.replace('`', '"')
    
    # 4. Fix escaped quotes (MySQL uses \' but PostgreSQL uses '')
    content = content.replace("\\'", "''")
    
    # 5. Fix hex binary data (0x... to E'\\x...'::bytea or just skip for now)
    # Most tables don't have binary data
    
    # 6. Remove empty lines
    lines = [line for line in content.split('\n') if line.strip() and not line.strip().startswith('--')]
    
    # Filter only INSERT statements
    insert_lines = [line for line in lines if line.strip().upper().startswith('INSERT')]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- PostgreSQL Data Import (converted from MySQL)\n")
        f.write("-- Run this in Supabase SQL Editor after creating schema with schema_postgres.sql\n\n")
        for line in insert_lines:
            f.write(line + '\n')
    
    print(f"Converted! Output saved to {output_file}")
    print(f"Total INSERT statements: {len(insert_lines)}")
    return True

if __name__ == "__main__":
    convert_mysql_to_postgres()
