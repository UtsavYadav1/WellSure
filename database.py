import psycopg2
import psycopg2.extras
import os

def get_db_connection():
    """
    Returns a new PostgreSQL connection to the Supabase database.
    Uses DATABASE_URL (standard for Render/Supabase) or individual env vars.
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Supabase/Render provides a full connection URL
        return psycopg2.connect(database_url)
    else:
        # Fallback to individual environment variables
        return psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'postgres'),
            database=os.environ.get('DB_NAME', 'wellsure'),
            port=int(os.environ.get('DB_PORT', 5432))
        )

def get_dict_cursor(conn):
    """Returns a cursor that returns rows as dictionaries."""
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
