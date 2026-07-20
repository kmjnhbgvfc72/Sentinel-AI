from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.reporting.report_service import ReportService
from models import Report
from database.soar_repository import get_db

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def reports(db: Session = Depends(get_db)):
    return [
        {
            "id": r.id,
            "type": r.report_type,
            "title": r.title,
            "content": r.content,
            "created_at": r.created_at,
        }
        for r in db.query(Report).order_by(Report.id.desc()).all()
    ]


@router.post("", status_code=201)
def generate_report(db: Session = Depends(get_db)):
    return ReportService(db).generate()
