"""
Patient dashboard and routes.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from pathlib import Path
from app.auth import get_current_user
from app.models import (
    get_user_by_id, 
    get_records_by_patient,
    search_doctors,
    get_doctors_visited_by_patient
)

router = APIRouter()
TEMPLATES_DIR = Path("app/templates")

def render_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 template."""
    template_path = TEMPLATES_DIR / template_name
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**context)


@router.get("/patient/dashboard", response_class=HTMLResponse)
async def patient_dashboard(request: Request):
    """Patient dashboard showing patient info and their records."""
    # Check authentication
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Access denied. Patient role required.")
    
    # Get patient info
    patient = get_user_by_id(user["user_id"])
    
    # Get patient's records
    records = get_records_by_patient(user["user_id"])
    
    # Get query params
    view = request.query_params.get("view", "overview")  # overview, doctors, records, search
    
    # Get search query if in search view
    search_query = request.query_params.get("q", "")
    search_results = []
    if view == "search" and search_query:
        search_results = search_doctors(search_query)
    elif view == "doctors":
        search_results = get_doctors_visited_by_patient(user["user_id"])
    
    # Calculate stats
    total_records = len(records)
    unique_doctors = len(set(record["doctor_id"] for record in records))
    
    html = render_template(
        "patient_dashboard.html",
        {
            "request": request,
            "patient": patient,
            "records": records,
            "view": view,
            "search_query": search_query,
            "search_results": search_results,
            "total_records": total_records,
            "unique_doctors": unique_doctors,
            "patient_id": user["user_id"]
        }
    )
    return HTMLResponse(content=html)

