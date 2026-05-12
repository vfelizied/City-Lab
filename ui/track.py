import streamlit as st
from ui._brand import inject_brand

inject_brand()
from logic.report_service import get_report

def render(report_id: str):
    st.title("Seguimiento del reporte")

    if not report_id:
        st.warning("Ingresa un ID de reporte")
        return

    with st.spinner("Buscando reporte..."):
        report = get_report(report_id)

    if not report:
        st.error("No encontramos este reporte")
        return

    status = report["status"]

    st.subheader(f"Estado: {status}")
    st.write("Ubicación:", report["location"])
    st.write("Descripción:", report["description"])
