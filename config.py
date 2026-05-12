import streamlit as st

APP_NAME = "Reporte Ciudadano"

def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return default

SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

CATEGORIES = [
    "Alumbrado",
    "Vías",
    "Basuras",
    "Parques",
    "Seguridad",
    "Agua",
    "Otro"
]

STATUSES = ["Recibido", "En revisión", "En proceso", "Resuelto"]

DEFAULT_STATUS = "Recibido"
