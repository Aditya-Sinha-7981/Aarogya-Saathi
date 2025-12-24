"""
Doctor dashboard and routes.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from pathlib import Path
from app.auth import get_current_user
from app.models import get_user_by_id, get_records_by_doctor

router = APIRouter()
TEMPLATES_DIR = Path("app/templates")

def render_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 template."""
    template_path = TEMPLATES_DIR / template_name
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**context)


@router.get("/doctor/dashboard", response_class=HTMLResponse)
async def doctor_dashboard(request: Request):
    """Doctor dashboard showing doctor info and their records."""
    # Check authentication
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Access denied. Doctor role required.")
    
    # Get doctor info
    doctor = get_user_by_id(user["user_id"])
    
    # Get doctor's records
    records = get_records_by_doctor(user["user_id"])
    
    # Get query params for success message
    created = request.query_params.get("created")
    
    html = render_template(
        "doctor_dashboard.html",
        {
            "request": request,
            "doctor": doctor,
            "records": records,
            "created": created
        }
    )
    return HTMLResponse(content=html)

