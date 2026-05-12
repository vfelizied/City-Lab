import uuid
from datetime import datetime
from data.reports_repo import insert_report, fetch_all, fetch_one, update_status
from config import DEFAULT_STATUS

def create_report(name, category, description, location):
    """Create report."""
    report = {
        "id": str(uuid.uuid4())[:8],
        "name": name or "Anónimo",
        "category": category,
        "description": description,
        "location": location,
        "status": DEFAULT_STATUS,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    insert_report(report)
    return report["id"]

def get_reports():
    return fetch_all()

def get_report(report_id):
    return fetch_one(report_id)

def change_status(report_id, status):
    update_status(report_id, status)
