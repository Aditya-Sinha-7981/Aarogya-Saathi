"""
Doctor dashboard and routes.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from pathlib import Path
from app.auth import get_current_user
from app.models import (
    get_user_by_id, 
    get_records_by_doctor, 
    search_patients, 
    get_all_patients,
    get_patient_record_count
)

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
    
    # Get query params
    created = request.query_params.get("created")
    view = request.query_params.get("view", "overview")  # overview, patients, records, search
    
    # Get search query if in search view
    search_query = request.query_params.get("q", "")
    search_results = []
    if view == "search" and search_query:
        search_results = search_patients(search_query)
    elif view == "patients":
        search_results = get_all_patients()
    
    # Calculate stats
    total_records = len(records)
    unique_patients = len(set(record["patient_id"] for record in records))
    
    html = render_template(
        "doctor_dashboard.html",
        {
            "request": request,
            "doctor": doctor,
            "records": records,
            "created": created,
            "view": view,
            "search_query": search_query,
            "search_results": search_results,
            "total_records": total_records,
            "unique_patients": unique_patients,
            "doctor_id": user["user_id"]
        }
    )
    return HTMLResponse(content=html)

