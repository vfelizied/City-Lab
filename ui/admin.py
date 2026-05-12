import streamlit as st
from config import STATUSES
from logic.report_service import get_reports, change_status

def render():
    st.title("Admin")

    reports = get_reports()

    for r in reports:
        st.write(r["id"], r["status"])

        new = st.selectbox(
            "Estado",
            STATUSES,
            key=r["id"]
        )

        if st.button("Actualizar", key="btn_" + r["id"]):
            change_status(r["id"], new)
            st.rerun()
