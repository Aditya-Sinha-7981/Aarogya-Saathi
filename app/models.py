"""
Data models and database queries.
This module contains all database operations.
"""
from app.database import get_db_connection, get_db_cursor
from datetime import datetime


def create_user(email: str, password_hash: str, role: str):
    """
    Create a new user in the database.
    
    Args:
        email: User email (must be unique)
        password_hash: Hashed password
        role: "doctor" or "patient"
    
    Returns:
        dict: Created user data or None if email already exists
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, role, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, role, created_at
            """,
            (email, password_hash, role, datetime.now())
        )
        user = cursor.fetchone()
        conn.commit()
        return dict(user) if user else None
    except Exception as e:
        conn.rollback()
        # Check if it's a unique constraint violation
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            return None  # Email already exists
        raise
    finally:
        cursor.close()
        conn.close()


def get_user_by_email(email: str):
    """
    Get user by email.
    
    Args:
        email: User email
    
    Returns:
        dict: User data or None if not found
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            "SELECT id, email, password_hash, role, created_at FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id: int):
    """
    Get user by ID.
    
    Args:
        user_id: User ID
    
    Returns:
        dict: User data or None if not found
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            "SELECT id, email, role, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        return dict(user) if user else None
    finally:
        cursor.close()
        conn.close()


def create_medical_record(doctor_id: int, patient_id: int, title: str, notes: str):
    """
    Create a new medical record.
    
    Args:
        doctor_id: ID of the doctor creating the record
        patient_id: ID of the patient
        title: Record title
        notes: Record notes
    
    Returns:
        dict: Created record data
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            INSERT INTO medical_records (doctor_id, patient_id, title, notes, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, doctor_id, patient_id, title, notes, created_at
            """,
            (doctor_id, patient_id, title, notes, datetime.now())
        )
        record = cursor.fetchone()
        conn.commit()
        return dict(record) if record else None
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def get_records_by_doctor(doctor_id: int):
    """
    Get all medical records created by a doctor.
    
    Args:
        doctor_id: Doctor ID
    
    Returns:
        list: List of medical records with patient info
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT 
                mr.id, 
                mr.title, 
                mr.notes, 
                mr.created_at,
                mr.patient_id,
                u.email as patient_email
            FROM medical_records mr
            JOIN users u ON mr.patient_id = u.id
            WHERE mr.doctor_id = %s
            ORDER BY mr.created_at DESC
            """,
            (doctor_id,)
        )
        records = cursor.fetchall()
        return [dict(record) for record in records]
    finally:
        cursor.close()
        conn.close()


def get_records_by_patient(patient_id: int):
    """
    Get all medical records for a patient.
    
    Args:
        patient_id: Patient ID
    
    Returns:
        list: List of medical records with doctor info
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT 
                mr.id, 
                mr.title, 
                mr.notes, 
                mr.created_at,
                mr.doctor_id,
                u.email as doctor_email
            FROM medical_records mr
            JOIN users u ON mr.doctor_id = u.id
            WHERE mr.patient_id = %s
            ORDER BY mr.created_at DESC
            """,
            (patient_id,)
        )
        records = cursor.fetchall()
        return [dict(record) for record in records]
    finally:
        cursor.close()
        conn.close()


def search_patients(search_term: str, limit: int = 20):
    """
    Search for patients by email (partial match).
    
    Args:
        search_term: Search term to match against email
        limit: Maximum number of results to return
    
    Returns:
        list: List of patient users matching the search term
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT id, email, role, created_at
            FROM users
            WHERE role = 'patient' AND email ILIKE %s
            ORDER BY email
            LIMIT %s
            """,
            (f"%{search_term}%", limit)
        )
        patients = cursor.fetchall()
        return [dict(patient) for patient in patients]
    finally:
        cursor.close()
        conn.close()


def get_all_patients(limit: int = 100):
    """
    Get all patients.
    
    Args:
        limit: Maximum number of patients to return
    
    Returns:
        list: List of all patient users
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT id, email, role, created_at
            FROM users
            WHERE role = 'patient'
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,)
        )
        patients = cursor.fetchall()
        return [dict(patient) for patient in patients]
    finally:
        cursor.close()
        conn.close()


def get_patient_record_count(patient_id: int, doctor_id: int):
    """
    Get count of records for a specific patient by a specific doctor.
    
    Args:
        patient_id: Patient ID
        doctor_id: Doctor ID
    
    Returns:
        int: Number of records
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*) as count
            FROM medical_records
            WHERE patient_id = %s AND doctor_id = %s
            """,
            (patient_id, doctor_id)
        )
        result = cursor.fetchone()
        return result['count'] if result else 0
    finally:
        cursor.close()
        conn.close()


def search_doctors(search_term: str, limit: int = 20):
    """
    Search for doctors by email (partial match).
    
    Args:
        search_term: Search term to match against email
        limit: Maximum number of results to return
    
    Returns:
        list: List of doctor users matching the search term
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT id, email, role, created_at
            FROM users
            WHERE role = 'doctor' AND email ILIKE %s
            ORDER BY email
            LIMIT %s
            """,
            (f"%{search_term}%", limit)
        )
        doctors = cursor.fetchall()
        return [dict(doctor) for doctor in doctors]
    finally:
        cursor.close()
        conn.close()


def get_doctors_visited_by_patient(patient_id: int):
    """
    Get all unique doctors that a patient has visited (doctors who have created records for this patient).
    
    Args:
        patient_id: Patient ID
    
    Returns:
        list: List of unique doctor users that the patient has visited
    """
    conn, cursor = get_db_cursor()
    try:
        cursor.execute(
            """
            SELECT DISTINCT u.id, u.email, u.role, u.created_at
            FROM users u
            INNER JOIN medical_records mr ON u.id = mr.doctor_id
            WHERE mr.patient_id = %s AND u.role = 'doctor'
            ORDER BY u.email
            """,
            (patient_id,)
        )
        doctors = cursor.fetchall()
        return [dict(doctor) for doctor in doctors]
    finally:
        cursor.close()
        conn.close()