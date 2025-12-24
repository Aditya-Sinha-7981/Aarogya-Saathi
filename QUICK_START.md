# 🚀 Quick Start Guide

Get your Medical Records Sharing App running in 5 minutes!

## ✅ Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Supabase account created
- [ ] Supabase project created
- [ ] Database tables created (`users` and `medical_records`)
- [ ] Database connection string ready

---

## 📦 Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Step 2: Set Up Environment Variables

1. **Create `.env` file** in the project root
2. **Add your Supabase connection string:**

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

**How to get this:**
- Supabase Dashboard → Settings → Database → Connection string
- Replace `[YOUR-PASSWORD]` with your actual password

---

## 🧪 Step 3: Test Connection

```bash
python test_connection.py
```

You should see: `✅ Connection successful!`

---

## 🎬 Step 4: Run the App

```bash
uvicorn app.main:app --reload
```

Open your browser: **http://localhost:8000**

---

## 🎯 Test the App

1. **Register a Doctor:**
   - Email: `doctor@test.com`
   - Password: `test123`
   - Role: `Doctor`

2. **Register a Patient:**
   - Email: `patient@test.com`
   - Password: `test123`
   - Role: `Patient`

3. **Login as Doctor** → Create a medical record for the patient

4. **Login as Patient** → View the record!

---

## 📚 More Details

- **Full Supabase Setup**: See `SETUP_GUIDE.md`
- **Connection Details**: See `CONNECTION_GUIDE.md`
- **Project Overview**: See `readme.md`

---

## 🆘 Having Issues?

1. Check `.env` file exists and has correct `DATABASE_URL`
2. Verify Supabase tables are created
3. Run `python test_connection.py` to diagnose
4. See `CONNECTION_GUIDE.md` for troubleshooting

**That's it! You're ready to go! 🎉**

