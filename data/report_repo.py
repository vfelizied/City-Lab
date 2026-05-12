from datetime import datetime
from external.supabase_client import get_client
from config import DEFAULT_STATUS

client = get_client()

def insert_report(report: dict):
    """Insert report into Supabase."""
    client.table("reports").insert(report).execute()

def fetch_all():
    """Fetch all reports."""
    return client.table("reports").select("*").order("created_at", desc=True).execute().data

def fetch_one(report_id: str):
    """Fetch single report."""
    res = client.table("reports").select("*").eq("id", report_id).execute()
    return res.data[0] if res.data else None

def update_status(report_id: str, status: str):
    """Update report status."""
    client.table("reports").update({
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", report_id).execute()
