from ui._brand import inject_brand
from config import STATUSES
from logic.report_service import get_reports, change_status

def render():
    st.title("Panel de administración")

    reports = get_reports()

    if not reports:
        st.info("No hay reportes aún")
        return

    for r in reports:
        st.divider()
        st.write(f"ID: {r['id']}")
        st.write(f"Estado actual: {r['status']}")

        new = st.selectbox(
            "Cambiar estado",
            STATUSES,
            key=r["id"]
        )

        if st.button("Actualizar", key="btn_" + r["id"]):
            with st.spinner("Actualizando..."):
                change_status(r["id"], new)

            st.success("Estado actualizado")
            st.rerun()
