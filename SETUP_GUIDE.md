# 📋 Project Summary & Complete Supabase Setup Guide

## 📖 Basic Instructions from README

### Project Overview
Build a **Medical Records Sharing Web App** where:
- **Doctors** can create medical records
- **Patients** can view their records (read-only)
- Data is shared across multiple devices via Supabase database
- Built with **Python (FastAPI)** backend and **HTML/CSS** frontend

### Key Requirements
1. **Two user roles**: `doctor` and `patient`
2. **Authentication**: Custom email + password (hashed in Python)
3. **Database**: Supabase PostgreSQL (used ONLY as database, no Supabase auth)
4. **Architecture**: Browser → Python FastAPI → Supabase Database
5. **MVP Goal**: Doctor creates record on one laptop, patient sees it on another laptop

### Project Structure (Must Follow)
```
app/
├── main.py              # FastAPI entry point
├── database.py          # Supabase DB connection
├── models.py            # Data models / queries
├── auth.py              # Auth helpers (hashing, sessions)
├── routes/
│   ├── auth.py          # Register / login routes
│   ├── doctor.py        # Doctor dashboard + actions
│   ├── patient.py       # Patient dashboard
│   └── records.py       # Create / view records
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── doctor_dashboard.html
│   ├── patient_dashboard.html
│   └── create_record.html
└── static/
    └── style.css
```

### Database Schema
**Table: `users`**
- `id` (SERIAL PRIMARY KEY)
- `email` (TEXT UNIQUE)
- `password_hash` (TEXT)
- `role` (TEXT: "doctor" | "patient")
- `created_at` (TIMESTAMP)

**Table: `medical_records`**
- `id` (SERIAL PRIMARY KEY)
- `doctor_id` (INTEGER REFERENCES users(id))
- `patient_id` (INTEGER REFERENCES users(id))
- `title` (TEXT)
- `notes` (TEXT)
- `created_at` (TIMESTAMP)

### Application Routes
- `/` - Landing page (Login/Register)
- `/register` - User registration
- `/login` - User login
- `/doctor/dashboard` - Doctor dashboard
- `/patient/dashboard` - Patient dashboard
- `/records/create` - Create medical record (doctors only)

---

## 🚀 Complete Supabase Setup Guide (For Beginners)

### Step 1: Create a Supabase Account

1. **Go to Supabase website**
   - Visit: https://supabase.com
   - Click **"Start your project"** or **"Sign up"**

2. **Sign up**
   - You can sign up with:
     - GitHub account (easiest)
     - Email address
     - Google account
   - Complete the sign-up process

3. **Verify your email** (if using email sign-up)
   - Check your inbox for verification email
   - Click the verification link

### Step 2: Create a New Project

1. **After logging in**, you'll see the Supabase dashboard
2. Click **"New Project"** button (usually top right or center)
3. **Fill in project details**:
   - **Name**: `aarogya-saathi` (or any name you prefer)
   - **Database Password**: 
     - Create a STRONG password (save it securely!)
     - You'll need this to connect from Python
     - Example: `MySecurePass123!@#`
   - **Region**: Choose closest to you (e.g., "Southeast Asia (Singapore)" or "US East")
   - **Pricing Plan**: Select **"Free"** (perfect for hackathon/demo)
4. Click **"Create new project"**
5. **Wait 2-3 minutes** for Supabase to set up your project

### Step 3: Get Your Database Connection Details

Once your project is ready:

1. **Go to Project Settings**
   - Click the **gear icon** (⚙️) in the left sidebar
   - Or click **"Settings"** → **"API"**

2. **Find your connection details**:
   - Scroll down to **"Connection string"** section
   - You'll see something like:
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
     ```
   - **Copy this connection string** (you'll need it for Python)

3. **Alternative: Get individual details**
   - **Database URL**: `db.xxxxx.supabase.co`
   - **Port**: `5432`
   - **Database name**: `postgres`
   - **User**: `postgres`
   - **Password**: (the one you created in Step 2)

### Step 4: Create Database Tables

1. **Open SQL Editor**
   - Click **"SQL Editor"** in the left sidebar (icon looks like `</>`)

2. **Create the `users` table**
   - Click **"New query"**
   - Copy and paste this SQL:

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('doctor', 'patient')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

3. **Click "Run"** (or press Ctrl+Enter)
   - You should see: "Success. No rows returned"

4. **Create the `medical_records` table**
   - Click **"New query"** again
   - Copy and paste this SQL:

```sql
-- Create medical_records table
CREATE TABLE IF NOT EXISTS medical_records (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    patient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_medical_records_doctor_id ON medical_records(doctor_id);
CREATE INDEX IF NOT EXISTS idx_medical_records_patient_id ON medical_records(patient_id);
```

5. **Click "Run"** again
   - You should see: "Success. No rows returned"

### Step 5: Verify Tables Were Created

1. **Go to Table Editor**
   - Click **"Table Editor"** in the left sidebar (database icon)
   - You should see two tables:
     - `users`
     - `medical_records`

2. **Check table structure**
   - Click on `users` table
   - Verify columns: `id`, `email`, `password_hash`, `role`, `created_at`
   - Click on `medical_records` table
   - Verify columns: `id`, `doctor_id`, `patient_id`, `title`, `notes`, `created_at`

### Step 6: Set Up Python Connection (Next Steps)

You'll need to install the Supabase Python client:

```bash
pip install supabase psycopg2-binary
```

Or if using connection string directly:
```bash
pip install psycopg2-binary sqlalchemy
```

### Step 7: Save Your Credentials Securely

Create a `.env` file in your project root (NEVER commit this to git):

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

**Where to find these:**
- **SUPABASE_URL**: Settings → API → Project URL
- **SUPABASE_KEY**: Settings → API → `anon` `public` key
- **DATABASE_URL**: Settings → Database → Connection string (use the one with password)

### Step 8: Test Your Connection (Optional)

You can test the connection using Python:

```python
import psycopg2
from os import getenv

# Replace with your actual connection string
conn = psycopg2.connect(
    "postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres"
)
cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

---

## ✅ Checklist

- [ ] Created Supabase account
- [ ] Created new project
- [ ] Saved database password securely
- [ ] Created `users` table
- [ ] Created `medical_records` table
- [ ] Verified tables in Table Editor
- [ ] Copied connection details to `.env` file
- [ ] Ready to connect from Python!

---

## 🔒 Security Notes

1. **Never commit `.env` file** to git
2. **Never share your database password** publicly
3. **Use environment variables** for all sensitive data
4. **The free tier is fine** for hackathon/demo purposes

---

## 🆘 Troubleshooting

**Problem**: "Connection refused"
- **Solution**: Check if your IP is blocked. Go to Settings → Database → Connection Pooling and check restrictions.

**Problem**: "Table doesn't exist"
- **Solution**: Make sure you ran the SQL queries in the correct database (should be `postgres`)

**Problem**: "Password authentication failed"
- **Solution**: Double-check your password. You can reset it in Settings → Database.

**Problem**: "Can't find SQL Editor"
- **Solution**: Make sure you're in the correct project. SQL Editor is in the left sidebar.

---

## 📚 Additional Resources

- Supabase Docs: https://supabase.com/docs
- PostgreSQL Tutorial: https://www.postgresql.org/docs/
- FastAPI Docs: https://fastapi.tiangolo.com/

---

**You're all set!** Now you can start building your Python FastAPI application to connect to this Supabase database.

