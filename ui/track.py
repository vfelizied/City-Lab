import streamlit as st
from logic.report_service import get_report

def render(report_id: str):
    st.title("Seguimiento")

    report = get_report(report_id)

    if not report:
        st.error("No encontrado")
        return

    st.write(report)
