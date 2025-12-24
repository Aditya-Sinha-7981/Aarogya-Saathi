"""
Authentication helpers: password hashing and session management.
"""
import hashlib
import secrets
from fastapi import Request, Response
from datetime import datetime, timedelta


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with salt.
    For production, consider using bcrypt or argon2.
    
    Args:
        password: Plain text password
    
    Returns:
        str: Hashed password
    """
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        password: Plain text password
        password_hash: Stored password hash (format: "salt:hash")
    
    Returns:
        bool: True if password matches
    """
    try:
        salt, stored_hash = password_hash.split(":")
        computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return computed_hash == stored_hash
    except ValueError:
        return False


# Simple in-memory session store (for demo purposes)
# In production, use Redis or database-backed sessions
sessions = {}


def create_session(user_id: int, role: str) -> str:
    """
    Create a new session for a user.
    
    Args:
        user_id: User ID
        role: User role
    
    Returns:
        str: Session token
    """
    session_token = secrets.token_urlsafe(32)
    sessions[session_token] = {
        "user_id": user_id,
        "role": role,
        "created_at": datetime.now()
    }
    return session_token


def get_session(session_token: str):
    """
    Get session data by token.
    
    Args:
        session_token: Session token
    
    Returns:
        dict: Session data or None if invalid
    """
    if session_token in sessions:
        session = sessions[session_token]
        # Check if session is expired (24 hours)
        if datetime.now() - session["created_at"] < timedelta(hours=24):
            return session
        else:
            # Session expired, remove it
            del sessions[session_token]
    return None


def delete_session(session_token: str):
    """
    Delete a session.
    
    Args:
        session_token: Session token
    """
    if session_token in sessions:
        del sessions[session_token]


def get_current_user(request: Request):
    """
    Get current user from session cookie.
    
    Args:
        request: FastAPI request object
    
    Returns:
        dict: User data with 'user_id' and 'role', or None if not logged in
    """
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    
    session = get_session(session_token)
    if not session:
        return None
    
    return {
        "user_id": session["user_id"],
        "role": session["role"]
    }

