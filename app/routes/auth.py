"""
Authentication routes: registration and login.
"""
from fastapi import APIRouter, Request, Response, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from jinja2 import Template
from pathlib import Path
from app.models import create_user, get_user_by_email
from app.auth import hash_password, verify_password, create_session

router = APIRouter()
TEMPLATES_DIR = Path("app/templates")


def render_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 template."""
    template_path = TEMPLATES_DIR / template_name
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**context)

@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Landing page with login/register options."""
    html = render_template("landing.html", {"request": request})
    return HTMLResponse(content=html)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page."""
    html = render_template("register.html", {"request": request})
    return HTMLResponse(content=html)


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    """
    Handle user registration.
    
    Validates input, hashes password, and creates user.
    """
    # Validate role
    if role not in ["doctor", "patient"]:
        html = render_template("register.html", {"request": request, "error": "Invalid role. Must be 'doctor' or 'patient'."})
        return HTMLResponse(content=html, status_code=400)
    
    # Validate email format (basic)
    if "@" not in email or "." not in email:
        html = render_template("register.html", {"request": request, "error": "Invalid email format."})
        return HTMLResponse(content=html, status_code=400)
    
    # Validate password length
    if len(password) < 6:
        html = render_template("register.html", {"request": request, "error": "Password must be at least 6 characters."})
        return HTMLResponse(content=html, status_code=400)
    
    # Hash password
    password_hash = hash_password(password)
    
    # Create user
    user = create_user(email, password_hash, role)
    
    if user is None:
        # Email already exists
        html = render_template("register.html", {"request": request, "error": "Email already registered. Please login instead."})
        return HTMLResponse(content=html, status_code=400)
    
    # Redirect to login
    return RedirectResponse(url="/login?registered=1", status_code=303)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: int = None):
    """Login page."""
    message = None
    if registered:
        message = "Registration successful! Please login."
    html = render_template("login.html", {"request": request, "message": message})
    return HTMLResponse(content=html)


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Handle user login.
    
    Verifies credentials and creates session.
    """
    # Get user by email
    user = get_user_by_email(email)
    
    if not user:
        html = render_template("login.html", {"request": request, "error": "Invalid email or password."})
        return HTMLResponse(content=html, status_code=401)
    
    # Verify password
    if not verify_password(password, user["password_hash"]):
        html = render_template("login.html", {"request": request, "error": "Invalid email or password."})
        return HTMLResponse(content=html, status_code=401)
    
    # Create session
    session_token = create_session(user["id"], user["role"])
    
    # Set session cookie
    response = RedirectResponse(url=f"/{user['role']}/dashboard", status_code=303)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax"
    )
    
    return response


@router.get("/logout")
async def logout(request: Request, response: Response):
    """Logout user by clearing session."""
    session_token = request.cookies.get("session_token")
    if session_token:
        from app.auth import delete_session
        delete_session(session_token)
    
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_token")
    return response

