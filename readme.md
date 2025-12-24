# 🏥 Medical Records Sharing Web App (Hackathon MVP)

A **Python-first web application** that allows **doctors and patients to share medical records** in one centralized place.

This project is built for a **hackathon demo**, with an emphasis on:
- stability
- clarity
- multi-device usage
- ease of extension later

The goal is not to overengineer, but to ship a **working, understandable system** that can grow safely.

---

## 🎯 Core Idea

- Users register as **Doctor** or **Patient**
- Users log in with **email + password**
- Doctors create medical records
- Patients can view those records
- Data is shared across **multiple laptops/devices**
- All logic lives in **Python**
- UI is built using **HTML + CSS**

---

## 🧱 Final Architecture (Locked)

Browser (HTML + CSS)
|
v
Python Server (FastAPI)
|
v
Supabase (PostgreSQL database only)


### Important Notes
- Supabase is used **only as a database**
- No Supabase auth
- No Supabase policies
- No frontend calling Supabase directly
- **Python is the single source of truth**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|------------|
| Frontend | HTML + CSS + minimal JS |
| Backend | Python (FastAPI) |
| Database | Supabase (PostgreSQL) |
| Auth | Custom email + password (hashed in Python) |

---

## 🌐 Why Supabase Is Used

Supabase is used to:
- host a **shared PostgreSQL database**
- allow multiple laptops to see the same data
- avoid local networking complexity during demos

Supabase is treated as:
> “Remote PostgreSQL with a nice dashboard”

All business logic stays in Python.

---

## 👤 User Roles

There are **two roles**:
- `doctor`
- `patient`

Both are stored in the same table and differentiated using a `role` field.

---

## 📄 Medical Records

- Created **only by doctors**
- Each record belongs to:
  - one doctor
  - one patient
- Records contain:
  - title
  - notes (plain text)
- Patients have **read-only access**

---

## 🗄️ Database Schema (Stable Core)

### `users`
```sql
id              SERIAL PRIMARY KEY
email           TEXT UNIQUE
password_hash   TEXT
role            TEXT        -- "doctor" | "patient"
created_at      TIMESTAMP

medical_records
id              SERIAL PRIMARY KEY
doctor_id       INTEGER REFERENCES users(id)
patient_id      INTEGER REFERENCES users(id)
title           TEXT
notes           TEXT
created_at      TIMESTAMP


This schema is intentionally minimal and stable.
New features should add tables, not rewrite these.

📁 Project Structure (Must Be Preserved)
app/
├── main.py              # FastAPI entry point
├── database.py          # Supabase DB connection
├── models.py            # Data models / queries
├── auth.py              # Auth helpers (hashing, sessions)
│
├── routes/
│   ├── auth.py          # Register / login routes
│   ├── doctor.py        # Doctor dashboard + actions
│   ├── patient.py       # Patient dashboard
│   └── records.py       # Create / view records
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── doctor_dashboard.html
│   ├── patient_dashboard.html
│   └── create_record.html
│
├── static/
│   └── style.css
│
└── README.md


AI tools and contributors must extend, not restructure, this layout.

🔁 Application Flow
1️⃣ Landing Page

Route: /

Login

Register

2️⃣ Registration

Route: /register

Fields

Email

Password

Role (Doctor / Patient)

Backend Logic

Ensure email is unique

Hash password in Python

Store user in database

Redirect to login

3️⃣ Login

Route: /login

Backend Logic

Verify password hash

Create session (cookie-based)

Redirect based on role:

Doctor → /doctor/dashboard

Patient → /patient/dashboard

🩺 Doctor Dashboard

Route: /doctor/dashboard

Features:

View doctor info

Create a medical record

View records created by the doctor

➕ Create Medical Record

Route: /records/create

Fields

Patient email or ID

Title

Notes

On Submit

Verify logged-in user is a doctor

Insert record into database

Redirect to dashboard

👨‍⚕️ Patient Dashboard

Route: /patient/dashboard

Features:

View patient info

View all records linked to the patient

Read-only access

🌍 Multi-Device Usage

Each laptop runs the Python server locally

All servers connect to the same Supabase database

Data changes are visible across devices instantly

Example:

Laptop A: doctor creates record

Laptop B: patient refreshes dashboard and sees it

✅ MVP Success Criteria

The MVP is considered successful if:

A doctor can create a record on one laptop and a patient can see it on another laptop.

Everything else is secondary.

🚫 Explicitly Out of Scope (For Now)

QR code linking

File uploads (PDFs, images)

Realtime WebSockets

Notifications

Audit logs

OCR

ML models

OAuth / social login

These will be added after the MVP works.

🧠 Design Philosophy

Stability over cleverness

Python owns all logic

Supabase is infrastructure, not brain

HTML/CSS stays simple and durable

Easy for humans and AI tools to continue

📌 Source of Truth

This README defines:

architecture

scope

constraints

Any changes to architecture must be discussed before implementation.

🧪 First Task for Contributors / AI Tools

Implement only:

Database connection to Supabase

User registration

User login

Create one medical record

View that record as another user

No refactors. No redesigns. No extras.


---

That’s your **final README**.  
It’s boring. It’s strict. It’s stable. And it won’t betray you when you add features or switch AI tools.

Next step is obvious:  
spin up Supabase tables and start wiring Python to them, one route at a time.