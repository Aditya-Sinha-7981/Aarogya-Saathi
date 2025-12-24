# 🔌 How to Connect Your App to Supabase

This guide will walk you through connecting your Python FastAPI application to Supabase step by step.

## 📋 Prerequisites

1. ✅ You have completed the Supabase setup (created account, project, and tables)
2. ✅ You have your Supabase database connection string
3. ✅ Python 3.8+ installed on your computer

---

## Step 1: Install Python Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `fastapi` - Web framework
- `uvicorn` - ASGI server to run FastAPI
- `python-dotenv` - Load environment variables from `.env` file
- `psycopg2-binary` - PostgreSQL database adapter (to connect to Supabase)
- `jinja2` - Template engine for HTML
- `python-multipart` - Handle form data

---

## Step 2: Get Your Supabase Connection String

1. **Go to your Supabase Dashboard**
   - Visit: https://supabase.com/dashboard
   - Select your project

2. **Navigate to Settings**
   - Click the **gear icon** (⚙️) in the left sidebar
   - Click **"Database"** in the settings menu

3. **Find Connection String**
   - Scroll down to **"Connection string"** section
   - You'll see something like:
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
     ```
   - **IMPORTANT**: Replace `[YOUR-PASSWORD]` with the actual password you created when setting up the project
   - Example:
     ```
     postgresql://postgres:MySecurePass123@db.abcdefgh.supabase.co:5432/postgres
     ```

4. **Copy the complete connection string** (with your password)

---

## Step 3: Create `.env` File

1. **In your project root directory**, create a file named `.env`
   - This file stores your database credentials securely
   - **NEVER commit this file to git** (it's already in `.gitignore`)

2. **Add your connection string** to the `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

**Replace:**
- `YOUR_ACTUAL_PASSWORD` with your Supabase database password
- `xxxxx` with your actual Supabase project ID

**Example:**
```env
DATABASE_URL=postgresql://postgres:MySecurePass123!@#@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## Step 4: Verify Your Tables Exist

Before running the app, make sure your Supabase tables are created:

1. **Go to Supabase Dashboard** → **Table Editor**
2. **Verify you have two tables:**
   - ✅ `users` (with columns: id, email, password_hash, role, created_at)
   - ✅ `medical_records` (with columns: id, doctor_id, patient_id, title, notes, created_at)

If tables don't exist, go to **SQL Editor** and run the SQL from `SETUP_GUIDE.md` Step 4.

---

## Step 5: Test the Connection

Create a simple test script to verify the connection works:

**Create file: `test_connection.py`** in your project root:

```python
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
    print(f"✅ Connection successful!")
    print(f"PostgreSQL version: {version[0]}")
    
    # Test if tables exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print(f"\n✅ Found {len(tables)} tables:")
    for table in tables:
        print(f"   - {table[0]}")
    
    cursor.close()
    conn.close()
    print("\n🎉 Everything is working! You can now run the app.")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check your .env file exists and has DATABASE_URL")
    print("2. Verify your password in the connection string")
    print("3. Make sure your Supabase project is active")
```

**Run the test:**
```bash
python test_connection.py
```

If you see "✅ Connection successful!", you're good to go!

---

## Step 6: Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload when you make code changes.

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 7: Access the Application

Open your web browser and go to:

**http://localhost:8000**

You should see the landing page with "Login" and "Register" buttons!

---

## 🎯 Quick Test Flow

1. **Register a Doctor:**
   - Click "Register"
   - Email: `doctor@test.com`
   - Password: `test123`
   - Role: `Doctor`
   - Click "Register"

2. **Register a Patient:**
   - Click "Register" again
   - Email: `patient@test.com`
   - Password: `test123`
   - Role: `Patient`
   - Click "Register"

3. **Login as Doctor:**
   - Login with `doctor@test.com` / `test123`
   - You'll see the Doctor Dashboard

4. **Create a Medical Record:**
   - Click "➕ Create Medical Record"
   - Patient Email: `patient@test.com`
   - Title: `Annual Checkup`
   - Notes: `Patient is healthy, all vitals normal`
   - Click "Create Record"

5. **Login as Patient:**
   - Logout, then login with `patient@test.com` / `test123`
   - You should see the record created by the doctor!

---

## 🔧 Troubleshooting

### Error: "DATABASE_URL not found"
- **Solution**: Make sure you created a `.env` file in the project root
- Check that the file is named exactly `.env` (not `.env.txt`)

### Error: "Connection refused" or "Connection timeout"
- **Solution**: 
  - Check your internet connection
  - Verify your Supabase project is active (not paused)
  - Double-check the connection string in `.env`

### Error: "Password authentication failed"
- **Solution**: 
  - Verify your password in the connection string
  - Make sure you replaced `[YOUR-PASSWORD]` with the actual password
  - Password is case-sensitive

### Error: "Table 'users' does not exist"
- **Solution**: Run the SQL queries from `SETUP_GUIDE.md` Step 4 to create the tables

### Error: "Module not found"
- **Solution**: Run `pip install -r requirements.txt` again

---

## 📝 Important Notes

1. **Never share your `.env` file** - it contains your database password
2. **The `.env` file is already in `.gitignore`** - it won't be committed to git
3. **For production**, use environment variables or a secrets manager
4. **Free Supabase tier** is perfect for hackathons and demos

---

## 🚀 Next Steps

Once everything is working:

1. ✅ Test creating records on one device
2. ✅ Test viewing records on another device (same Supabase database)
3. ✅ Customize the UI in `app/static/style.css`
4. ✅ Add more features as needed

---

## 📚 Need Help?

- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

**You're all set! Happy coding! 🎉**

