"""
Database connection to Supabase PostgreSQL.
This module handles the connection to Supabase database.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL not found in environment variables. "
        "Please create a .env file with your Supabase connection string."
    )


def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
        psycopg2.connection: Database connection object
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def get_db_cursor(conn=None):
    """
    Get a database cursor with RealDictCursor (returns dict-like rows).
    
    Args:
        conn: Optional connection. If None, creates a new one.
    
    Returns:
        tuple: (connection, cursor)
    """
    if conn is None:
        conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cursor

