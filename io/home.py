import streamlit as st
from config import CATEGORIES
from logic.report_service import create_report
from logic.validators import validate_report

def render():
    st.title("📍 Reportar un problema")

    st.caption("No necesitas cuenta. Solo describe lo que está pasando.")

    with st.form("report"):
        name = st.text_input("Nombre (opcional)")
        category = st.selectbox("Tipo de problema", CATEGORIES)
        location = st.text_input("Ubicación exacta")
        description = st.text_area("Describe el problema")

        ok = st.form_submit_button("Enviar reporte")

        if ok:
            with st.spinner("Registrando tu reporte..."):
                err = validate_report(name, location, description)
                if err:
                    st.error(err)
                    return

                rid = create_report(name, category, description, location)

            st.success("Reporte registrado correctamente")
            st.info(f"Tu ID de seguimiento: {rid}")
            st.markdown(f"👉 Comparte este link: `?page=track&id={rid}`")
