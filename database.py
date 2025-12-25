import mysql.connector

def get_db_connection():
    """
    Returns a new MySQL connection to the MediMind database.
    Make sure to replace YOUR_MYSQL_PASSWORD with your actual MySQL root password.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",                  # MySQL username
        password="root",  # <-- CHANGE THIS
        database="medimind"           # Database we created in Workbench
    )
