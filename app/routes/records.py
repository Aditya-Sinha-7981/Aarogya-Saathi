"""
Medical records routes: create and view records.
"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from pathlib import Path
from app.auth import get_current_user
from app.models import get_user_by_email, create_medical_record, get_user_by_id

router = APIRouter()
TEMPLATES_DIR = Path("app/templates")

def render_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 template."""
    template_path = TEMPLATES_DIR / template_name
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**context)


@router.get("/records/create", response_class=HTMLResponse)
async def create_record_page(request: Request):
    """Page to create a new medical record (doctors only)."""
    # Check authentication
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create records.")
    
    # Get patient_id from query params if provided
    patient_id = request.query_params.get("patient_id")
    patient_email = None
    if patient_id:
        try:
            patient = get_user_by_id(int(patient_id))
            if patient and patient["role"] == "patient":
                patient_email = patient["email"]
        except (ValueError, TypeError):
            pass
    
    html = render_template("create_record.html", {
        "request": request,
        "patient_email": patient_email
    })
    return HTMLResponse(content=html)


@router.post("/records/create")
async def create_record(
    request: Request,
    patient_email: str = Form(...),
    title: str = Form(...),
    notes: str = Form(...)
):
    """
    Handle medical record creation.
    
    Only doctors can create records.
    """
    # Check authentication
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create records.")
    
    # Validate inputs
    if not title.strip():
        html = render_template("create_record.html", {"request": request, "error": "Title is required."})
        return HTMLResponse(content=html, status_code=400)
    
    # Find patient by email
    patient = get_user_by_email(patient_email)
    if not patient:
        html = render_template("create_record.html", {"request": request, "error": f"Patient with email '{patient_email}' not found."})
        return HTMLResponse(content=html, status_code=404)
    
    if patient["role"] != "patient":
        html = render_template("create_record.html", {"request": request, "error": f"User '{patient_email}' is not a patient."})
        return HTMLResponse(content=html, status_code=400)
    
    # Create record
    try:
        create_medical_record(
            doctor_id=user["user_id"],
            patient_id=patient["id"],
            title=title.strip(),
            notes=notes.strip() if notes else ""
        )
        return RedirectResponse(url="/doctor/dashboard?created=1", status_code=303)
    except Exception as e:
        html = render_template("create_record.html", {"request": request, "error": f"Error creating record: {str(e)}"})
        return HTMLResponse(content=html, status_code=500)

