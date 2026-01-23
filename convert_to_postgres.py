"""
MySQL Backup to PostgreSQL Converter (Fixed)
Properly handles newlines and single quotes in data values.
"""
import re
import os

def convert_mysql_to_postgres(input_file='backup.sql', output_file='backup_postgres.sql'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run dump_db.py first.")
        return False
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace line breaks within string values (multi-line strings break PostgreSQL)
    # This regex finds text between single quotes and removes newlines inside
    def fix_string_values(match):
        value = match.group(1)
        # Remove newlines, carriage returns, and excess whitespace
        value = value.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        # Escape single quotes properly for PostgreSQL ('' instead of \')
        value = value.replace("''", "<<ESCAPED_QUOTE>>")  # Preserve already escaped
        value = value.replace("\\'", "''")  # MySQL escape to PostgreSQL escape
        value = value.replace("'", "''")  # Raw quotes to escaped
        value = value.replace("<<ESCAPED_QUOTE>>", "''")  # Restore preserved
        return f"'{value}'"
    
    # First, join all lines (remove line breaks that break INSERT statements)
    # Then split properly
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Process line by line, but handle multi-line INSERT statements
    lines = content.split('\n')
    processed_lines = []
    buffer = ""
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        buffer += " " + line if buffer else line
        
        # Check if this is a complete statement (ends with ;)
        if buffer.endswith(';'):
            # Process complete INSERT statement
            if buffer.upper().startswith('INSERT'):
                # Fix backticks to double quotes
                buffer = buffer.replace('`', '"')
                
                # Fix escaped single quotes from MySQL (\') to PostgreSQL ('')
                buffer = buffer.replace("\\'", "''")
                
                # Fix backslash escapes for paths
                buffer = buffer.replace('\\\\', '/')  # Windows paths to Unix
                
                processed_lines.append(buffer)
            buffer = ""
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- PostgreSQL Data Import (converted from MySQL)\n")
        f.write("-- Run this in Supabase SQL Editor after creating schema with schema_postgres.sql\n\n")
        for line in processed_lines:
            f.write(line + '\n')
    
    print(f"Converted! Output saved to {output_file}")
    print(f"Total INSERT statements: {len(processed_lines)}")
    return True

if __name__ == "__main__":
    convert_mysql_to_postgres()
