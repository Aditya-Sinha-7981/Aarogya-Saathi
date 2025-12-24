"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, doctor, patient, records

# Create FastAPI app
app = FastAPI(title="Aarogya Saathi - Medical Records Sharing")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(records.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

