import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load local environment secrets safely (ignored by Git)
load_dotenv()

from src.db.database import init_db, save_verified_report, get_longitudinal_trends, get_all_reports, get_connection
from src.parser.rule_extractor import extract_report_deterministic

# Ensure directories exist
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Initialize SQLite database on startup
init_db()

app = FastAPI(
    title="HealthTrack AI API",
    description="Local-first, privacy-focused longitudinal health tracking API for Indian diagnostic lab formats",
    version="1.0.0"
)

# Enable CORS for local client-side interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BiomarkerPayload(BaseModel):
    raw_name: str
    canonical_name: str
    raw_value: str
    numeric_value: Optional[float] = None
    raw_unit: str
    standard_value: Optional[float] = None
    standard_unit: str
    ref_min: Optional[float] = None
    ref_max: Optional[float] = None
    ref_text: Optional[str] = None
    method: Optional[str] = None
    comparable_flag: bool = True
    source_line_text: Optional[str] = None
    page_number: int = 1

class SaveReportRequest(BaseModel):
    patient_name: str
    report_id: str
    lab_name: str
    collection_date: str
    report_date: str
    pdf_filename: Optional[str] = None
    biomarkers: List[BiomarkerPayload]

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Accepts an Indian blood-test lab PDF, runs deterministic pdfplumber extraction,
    and returns structured biomarkers paired with raw source line text for verification.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF report files are supported.")

    temp_path = UPLOAD_DIR / file.filename
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted = extract_report_deterministic(temp_path)

        # Structure response for UI verification studio
        biomarker_records = []
        for b in extracted.biomarkers:
            biomarker_records.append({
                "raw_name": b.raw_name,
                "canonical_name": b.canonical_name,
                "raw_value": b.raw_value,
                "numeric_value": b.numeric_value,
                "raw_unit": b.raw_unit,
                "standard_value": b.standard_value,
                "standard_unit": b.standard_unit,
                "ref_min": b.reference_range.min_val if b.reference_range else None,
                "ref_max": b.reference_range.max_val if b.reference_range else None,
                "ref_text": b.reference_range.raw_text if b.reference_range else "",
                "method": b.method or "Standard",
                "comparable_flag": b.comparable_flag,
                "source_line_text": b.source_line_text or "",
                "page_number": b.page_number
            })

        return {
            "status": "success",
            "report_id": extracted.report_id,
            "lab_name": extracted.lab_name,
            "collection_date": extracted.collection_date,
            "report_date": extracted.report_date,
            "patient_age": extracted.patient_age,
            "patient_sex": extracted.patient_sex,
            "pdf_filename": file.filename,
            "biomarkers": biomarker_records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")

@app.post("/api/save")
async def save_report(payload: SaveReportRequest):
    """
    Commits verified lab report and biomarkers to local SQLite database.
    """
    report_dict = {
        "report_id": payload.report_id,
        "lab_name": payload.lab_name,
        "collection_date": payload.collection_date,
        "report_date": payload.report_date,
        "pdf_filename": payload.pdf_filename
    }
    biomarkers_dict = [b.dict() for b in payload.biomarkers]

    db_id = save_verified_report(payload.patient_name, report_dict, biomarkers_dict)
    return {"status": "success", "report_db_id": db_id}

@app.get("/api/trends")
async def get_trends(patient_name: str = "Ramesh Natani", canonical_name: str = "HbA1c"):
    """
    Retrieves longitudinal trend points from SQLite database for the selected biomarker.
    """
    records = get_longitudinal_trends(patient_name, canonical_name)
    return {"patient_name": patient_name, "canonical_name": canonical_name, "points": records}

@app.get("/api/reports")
async def list_reports(patient_name: Optional[str] = None):
    """
    Lists all saved lab reports from SQLite database.
    """
    reports = get_all_reports(patient_name)
    return {"reports": reports}

@app.get("/api/patients")
async def list_patients():
    """
    Retrieves registered family caregiver profiles.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY id ASC")
    patients = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"patients": patients}

# Serve root website files directly
@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/styles.css")
async def serve_styles():
    return FileResponse("styles.css")

@app.get("/app.js")
async def serve_script():
    return FileResponse("app.js")
