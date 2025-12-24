"""
Test script to verify Supabase database connection.
Run this before starting the main application.
"""
import os
from dotenv import load_dotenv
from app.database import get_db_connection

# Load environment variables
load_dotenv()
 
try:
    print("Testing database connection...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"[SUCCESS] Connection successful!")
    print(f"PostgreSQL version: {version[0]}")
    
    # Test if tables exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    print(f"\n[INFO] Found {len(tables)} tables:")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Verify required tables exist
    table_names = [t[0] for t in tables]
    required_tables = ['users', 'medical_records']
    missing_tables = [t for t in required_tables if t not in table_names]
    
    if missing_tables:
        print(f"\n[WARNING] Missing required tables: {', '.join(missing_tables)}")
        print("   Please run the SQL queries from SETUP_GUIDE.md Step 4")
    else:
        print("\n[SUCCESS] All required tables exist!")
    
    cursor.close()
    conn.close()
    print("\n[SUCCESS] Everything is working! You can now run the app with:")
    print("   uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check your .env file exists and has DATABASE_URL")
    print("2. Verify your password in the connection string")
    print("3. Make sure your Supabase project is active (not paused)")
    print("4. Check your internet connection")
    print("5. Verify the hostname in your connection string is correct")
    print("6. Try accessing your Supabase dashboard to ensure project is running")

