"""
Helper script to verify your Supabase connection string format.
"""
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("[ERROR] DATABASE_URL not found in .env file")
    exit(1)

print("Connection string format check:")
print("=" * 60)

# Hide password for security
if "@" in database_url:
    parts = database_url.split("@")
    if len(parts) == 2:
        # Show format without password
        safe_url = parts[0].split(":")[0] + "://postgres:***@" + parts[1]
        print(f"Format: {safe_url}")
    else:
        print(f"Format: {database_url[:50]}...")
else:
    print(f"Format: {database_url[:50]}...")

print("\nExpected format:")
print("postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres")
print("\nYour connection string components:")

try:
    # Parse the connection string
    if database_url.startswith("postgresql://"):
        url_part = database_url.replace("postgresql://", "")
        if "@" in url_part:
            auth_part, host_part = url_part.split("@", 1)
            if ":" in auth_part:
                user, password = auth_part.split(":", 1)
                print(f"  User: {user}")
                print(f"  Password: {'*' * len(password)} ({len(password)} characters)")
            
            if ":" in host_part:
                host, port_db = host_part.split(":", 1)
                if "/" in port_db:
                    port, database = port_db.split("/", 1)
                    print(f"  Host: {host}")
                    print(f"  Port: {port}")
                    print(f"  Database: {database}")
            
            # Check hostname format
            if host.startswith("db.") and host.endswith(".supabase.co"):
                print(f"\n[OK] Hostname format looks correct")
            else:
                print(f"\n[WARNING] Hostname format might be incorrect")
                print(f"  Expected: db.xxxxx.supabase.co")
                print(f"  Got: {host}")
            
            # Check if it's a valid Supabase hostname
            if "supabase.co" in host:
                print(f"[OK] Hostname contains 'supabase.co'")
            else:
                print(f"[WARNING] Hostname doesn't contain 'supabase.co'")
                
except Exception as e:
    print(f"[ERROR] Could not parse connection string: {e}")

print("\n" + "=" * 60)
print("\nNext steps:")
print("1. Go to Supabase Dashboard: https://supabase.com/dashboard")
print("2. Select your project")
print("3. Go to Settings -> Database")
print("4. Verify the connection string matches what you have in .env")
print("5. Make sure your project is NOT paused")
print("6. If paused, click 'Restore' to activate it")
print("\n[IMPORTANT] The DNS error suggests your Supabase project might be:")
print("  - Paused (most common on free tier after inactivity)")
print("  - Deleted")
print("  - Or there's a network/DNS issue")
print("\nCheck your Supabase dashboard to see the project status!")

