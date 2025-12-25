import mysql.connector
import os

def get_db_connection():
    """
    Returns a new MySQL connection to the MediMind database.
    Uses environment variables for production (Railway), falls back to local defaults.
    """
    return mysql.connector.connect(
        host=os.environ.get('MYSQLHOST', os.environ.get('DB_HOST', 'localhost')),
        user=os.environ.get('MYSQLUSER', os.environ.get('DB_USER', 'root')),
        password=os.environ.get('MYSQLPASSWORD', os.environ.get('DB_PASSWORD', 'root')),
        database=os.environ.get('MYSQLDATABASE', os.environ.get('DB_NAME', 'medimind')),
        port=int(os.environ.get('MYSQLPORT', os.environ.get('DB_PORT', 3306)))
    )

