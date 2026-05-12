import streamlit as st

APP_NAME = "Reporte Ciudadano"

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

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
