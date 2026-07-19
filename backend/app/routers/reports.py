from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime
import os
import uuid

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import analyze_medical_report, test_gemini
from app.utils.security import get_current_user
import app.database as db

router = APIRouter(prefix="/reports", tags=["Medical Reports"])

UPLOAD_FOLDER = "app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
):
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG files are allowed."
        )

    filename = f"{uuid.uuid4()}{extension}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save uploaded file
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text from PDF
    report_text = ""
    if extension == ".pdf":
        report_text = extract_text_from_pdf(filepath)

    # Analyze with Gemini
    analysis = None
    if report_text:
        analysis = await analyze_medical_report(report_text)

    # Save to MongoDB
    report = {
        "user_email": current_user,
        "file_name": file.filename,
        "stored_name": filename,
        "file_path": filepath,
        "file_type": extension,
        "uploaded_at": datetime.utcnow().isoformat(),
        "analysis": analysis,
    }

    result = await db.database.reports.insert_one(report)

    report["_id"] = str(result.inserted_id)

    return {
        "message": "Report uploaded successfully",
        "file": report
    }


@router.get("/test-ai")
async def test_ai():
    return {
        "response": await test_gemini()
    }

@router.get("/all")
async def get_all_reports(
    current_user: str = Depends(get_current_user)
):
    reports = await db.database.reports.find(
        {"user_email": current_user}
    ).to_list(None)

    for report in reports:
        report["_id"] = str(report["_id"])

    return reports


@router.get("/dashboard")
async def get_dashboard(
    current_user: str = Depends(get_current_user)
):
    reports = await db.database.reports.find(
        {"user_email": current_user}
    ).to_list(None)

    total_reports = len(reports)

    reports_requiring_doctor = 0
    latest_upload = None
    latest_summary = ""
    overall_health_status = "Healthy"

    if reports:
        # Sort latest first
        reports.sort(
            key=lambda x: x["uploaded_at"],
            reverse=True
        )

        latest_report = reports[0]

        latest_upload = latest_report["uploaded_at"]
        analysis = latest_report.get("analysis", {})

        if isinstance(analysis, dict):
            latest_summary = analysis.get("summary", "")
        else:
            latest_summary = analysis

        for report in reports:
            analysis = report.get("analysis", {})

            # Skip old reports where analysis is a string
            if not isinstance(analysis, dict):
                continue

            doctor = (
                analysis.get("doctor_consultation", {})
                .get("required", False)
            )

            if doctor:
                reports_requiring_doctor += 1

        if reports_requiring_doctor > 0:
            overall_health_status = "Needs Attention"

    return {
        "total_reports": total_reports,
        "reports_requiring_doctor": reports_requiring_doctor,
        "latest_upload": latest_upload,
        "latest_summary": latest_summary,
        "overall_health_status": overall_health_status
    }


@router.get("/health-score")
async def get_health_score(
    current_user: str = Depends(get_current_user)
):
    reports = await db.database.reports.find(
        {"user_email": current_user}
    ).to_list(None)

    if not reports:
        return {
            "health_score": 100,
            "risk_level": "Healthy",
            "reason": "No reports uploaded."
        }

    latest = sorted(
        reports,
        key=lambda x: x["uploaded_at"],
        reverse=True
    )[0]

    analysis = latest["analysis"]

    score = 100

    abnormal = len(analysis.get("abnormal_findings", []))
    risks = len(analysis.get("health_risks", []))
    doctor = analysis.get("doctor_consultation", {}).get("required", False)

    score -= abnormal * 5
    score -= risks * 10

    if doctor:
        score -= 15

    score = max(score, 0)

    if score >= 85:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "health_score": score,
        "risk_level": risk,
        "reason": analysis.get("summary", "")
    }

    
from bson import ObjectId

@router.get("/{report_id}")
async def get_report(
    report_id: str,
    current_user: str = Depends(get_current_user)
):
    report = await db.database.reports.find_one({
        "_id": ObjectId(report_id),
        "user_email": current_user
    })

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report["_id"] = str(report["_id"])

    return report
