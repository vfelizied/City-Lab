import streamlit as st
from config import CATEGORIES
from logic.report_service import create_report
from logic.validators import validate_report

def render():
    st.title("Reporte Ciudadano")

    with st.form("report"):
        name = st.text_input("Nombre")
        category = st.selectbox("Categoría", CATEGORIES)
        location = st.text_input("Ubicación")
        description = st.text_area("Descripción")

        ok = st.form_submit_button("Enviar")

        if ok:
            err = validate_report(name, location, description)
            if err:
                st.error(err)
                return

            rid = create_report(name, category, description, location)
            st.success(f"Reporte creado: {rid}")
