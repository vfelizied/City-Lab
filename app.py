import streamlit as st
import sqlite3
import uuid
import datetime
import pandas as pd

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Reporte Ciudadano",
    page_icon="📍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ADMIN_PASSWORD = "admin123"  # Cambia en producción → usa st.secrets["admin_password"]
DB_PATH = "reports.db"

CATEGORIES = [
    "Alumbrado público",
    "Vías y andenes",
    "Basuras y limpieza",
    "Parques y espacio público",
    "Seguridad",
    "Agua y alcantarillado",
    "Otro",
]

STATUSES = ["Recibido", "En revisión", "En proceso", "Resuelto", "Cerrado"]

STATUS_META = {
    "Recibido":    {"icon": "🟡", "color": "#F59E0B"},
    "En revisión": {"icon": "🔵", "color": "#3B82F6"},
    "En proceso":  {"icon": "🟠", "color": "#F97316"},
    "Resuelto":    {"icon": "🟢", "color": "#22C55E"},
    "Cerrado":     {"icon": "⚫", "color": "#6B7280"},
}

# ─────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id          TEXT PRIMARY KEY,
                name        TEXT,
                category    TEXT,
                description TEXT,
                location    TEXT,
                status      TEXT DEFAULT 'Recibido',
                created_at  TEXT,
                updated_at  TEXT
            )
        """)
        conn.commit()

def create_report(name, category, description, location):
    report_id = str(uuid.uuid4())[:8].upper()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO reports
               (id, name, category, description, location, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, 'Recibido', ?, ?)""",
            (report_id, name or "Anónimo", category, description, location, now, now),
        )
        conn.commit()
    return report_id

def get_report(report_id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM reports WHERE id = ?", (report_id.strip().upper(),)
        ).fetchone()
        return dict(row) if row else None

def get_all_reports():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM reports ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]

def update_status(report_id: str, new_status: str):
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute(
            "UPDATE reports SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, now, report_id.upper()),
        )
        conn.commit()

init_db()

# ─────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    color: #0F172A;
    margin-bottom: 0.3rem;
}

.hero-sub {
    font-size: 1rem;
    color: #64748B;
    margin-bottom: 1.5rem;
}

.case-number {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: 6px;
    color: #0F172A;
    background: #F1F5F9;
    padding: 16px 24px;
    border-radius: 12px;
    text-align: center;
    border: 2px dashed #CBD5E1;
    margin: 12px 0;
}

.report-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.status-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    margin: 6px 0;
}

.field-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-bottom: 2px;
}

.field-value {
    font-size: 0.95rem;
    color: #1E293B;
    margin-bottom: 12px;
}

.nav-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 28px;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 16px;
}

.warning-box {
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: #9A3412;
    margin-bottom: 16px;
}

/* Streamlit overrides */
div[data-testid="stForm"] {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px !important;
}

.stButton > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

.stButton > button[kind="primary"] {
    background: #0F172A !important;
    border: none !important;
    color: white !important;
}

.stSelectbox > div > div {
    border-radius: 10px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────
# ROUTING via query params
# ─────────────────────────────────────────
params = st.query_params
page = params.get("page", "home")
id_param = params.get("id", "")

# ─────────────────────────────────────────
# NAV (se omite en track con id directo)
# ─────────────────────────────────────────
def render_nav(active):
    col_logo, col_track, col_admin = st.columns([3, 1, 1])
    with col_logo:
        st.markdown('<div class="hero-title">📍 Reporte<br>Ciudadano</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Tu problema, visible. Sin desaparecer en el vacío.</div>', unsafe_allow_html=True)
    with col_track:
        if active != "track":
            if st.button("🔍 Mi reporte", use_container_width=True):
                st.query_params["page"] = "track"
                st.rerun()
    with col_admin:
        if active != "admin":
            if st.button("⚙️ Admin", use_container_width=True):
                st.query_params["page"] = "admin"
                st.rerun()
    st.markdown("---")

# ─────────────────────────────────────────
# PAGE: HOME — Enviar reporte
# ─────────────────────────────────────────
if page == "home":
    render_nav("home")

    st.markdown('<div class="warning-box">⚠️ <strong>Nota técnica:</strong> Los datos se guardan en SQLite local. En Streamlit Community Cloud el almacenamiento es efímero — se borra en cada reinicio. Para producción, conecta Supabase via <code>supabase-py</code> y <code>st.secrets</code>.</div>', unsafe_allow_html=True)

    with st.form("report_form", clear_on_submit=True):
        st.markdown("### Nuevo reporte")
        name = st.text_input("Tu nombre (opcional)", placeholder="Anónimo si prefieres")
        category = st.selectbox("Categoría del problema", CATEGORIES)
        location = st.text_input(
            "¿Dónde está el problema? *",
            placeholder="Ej: Calle 45 con Carrera 12, barrio El Prado",
        )
        description = st.text_area(
            "Describe el problema *",
            placeholder="Sé específico: qué es, cuánto tiempo lleva, cómo afecta al barrio...",
            height=130,
        )
        submitted = st.form_submit_button(
            "Enviar reporte →", use_container_width=True, type="primary"
        )

    if submitted:
        if not location.strip() or not description.strip():
            st.error("Por favor completa la ubicación y la descripción.")
        else:
            report_id = create_report(name, category, description, location)
            st.success("✅ Reporte recibido correctamente")
            st.markdown("**Tu número de caso:**")
            st.markdown(f'<div class="case-number">{report_id}</div>', unsafe_allow_html=True)
            st.caption("Guarda este número. Con él puedes ver el estado de tu reporte en cualquier momento.")
            track_url = f"?page=track&id={report_id}"
            st.markdown(f"[🔗 Ver estado público de este reporte]({track_url})")
            st.info("💡 Comparte este enlace con vecinos o en redes sociales. Mientras más gente lo vea, más difícil es ignorarlo.")

# ─────────────────────────────────────────
# PAGE: TRACK — Seguir reporte
# ─────────────────────────────────────────
elif page == "track":
    if not id_param:
        render_nav("track")
        st.markdown("### 🔍 Seguir mi reporte")
        search_id = st.text_input(
            "Número de caso", placeholder="Ej: A1B2C3D4", max_chars=8
        ).upper()
        if st.button("Buscar", type="primary"):
            st.query_params["page"] = "track"
            st.query_params["id"] = search_id
            st.rerun()
    else:
        report = get_report(id_param)

        if not report:
            render_nav("track")
            st.error(f"No encontramos el caso **{id_param}**. Verifica que lo escribiste correctamente.")
            if st.button("← Reportar un problema"):
                st.query_params["page"] = "home"
                st.query_params.pop("id", None)
                st.rerun()
        else:
            meta = STATUS_META.get(report["status"], {"icon": "⚪", "color": "#94A3B8"})
            icon = meta["icon"]
            color = meta["color"]

            # Minimal nav without logo block
            col_home, _, col_admin = st.columns([2, 2, 1])
            with col_home:
                if st.button("← Nuevo reporte"):
                    st.query_params["page"] = "home"
                    st.query_params.pop("id", None)
                    st.rerun()
            with col_admin:
                if st.button("⚙️ Admin"):
                    st.query_params["page"] = "admin"
                    st.query_params.pop("id", None)
                    st.rerun()

            st.markdown(f"### Caso #{report['id']}")
            st.markdown(
                f'<span class="status-pill" style="background:{color}22; color:{color};">'
                f'{icon} {report["status"]}</span>',
                unsafe_allow_html=True,
            )

            st.markdown('<div class="report-card">', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="field-label">Categoría</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{report["category"]}</div>', unsafe_allow_html=True)
                st.markdown('<div class="field-label">Reportado por</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{report["name"]}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="field-label">Fecha de reporte</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{report["created_at"][:10]}</div>', unsafe_allow_html=True)
                st.markdown('<div class="field-label">Última actualización</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{report["updated_at"][:10]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="field-label">Ubicación</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="field-value">{report["location"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="field-label">Descripción</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="field-value">{report["description"]}</div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            share_url = f"?page=track&id={report['id']}"
            st.markdown(f"[🔗 Compartir este reporte]({share_url})")

# ─────────────────────────────────────────
# PAGE: ADMIN — Panel de operador
# ─────────────────────────────────────────
elif page == "admin":
    render_nav("admin")
    st.markdown("### ⚙️ Panel de operador")

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        pwd = st.text_input("Contraseña", type="password")
        if st.button("Entrar", type="primary"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    else:
        reports = get_all_reports()

        if not reports:
            st.info("No hay reportes aún.")
        else:
            df = pd.DataFrame(reports)

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                cat_filter = st.selectbox("Categoría", ["Todas"] + CATEGORIES)
            with col_f2:
                status_filter = st.selectbox("Estado", ["Todos"] + STATUSES)

            filtered = df.copy()
            if cat_filter != "Todas":
                filtered = filtered[filtered["category"] == cat_filter]
            if status_filter != "Todos":
                filtered = filtered[filtered["status"] == status_filter]

            st.caption(f"{len(filtered)} reporte(s)")

            for _, row in filtered.iterrows():
                meta = STATUS_META.get(row["status"], {"icon": "⚪", "color": "#94A3B8"})
                label = f"{meta['icon']} #{row['id']} — {row['category']} · {str(row['location'])[:40]}"

                with st.expander(label):
                    st.markdown(f"**Descripción:** {row['description']}")
                    st.markdown(f"**Reportado por:** {row['name']} · {str(row['created_at'])[:10]}")

                    new_status = st.selectbox(
                        "Cambiar estado",
                        STATUSES,
                        index=STATUSES.index(row["status"]) if row["status"] in STATUSES else 0,
                        key=f"sel_{row['id']}",
                    )

                    col_btn, col_link = st.columns([1, 2])
                    with col_btn:
                        if st.button("Actualizar estado", key=f"upd_{row['id']}", type="primary"):
                            update_status(row["id"], new_status)
                            st.success("Estado actualizado.")
                            st.rerun()
                    with col_link:
                        st.markdown(f"[🔗 Ver reporte público](?page=track&id={row['id']})")

        st.markdown("---")
        if st.button("Cerrar sesión"):
            st.session_state.admin_auth = False
            st.query_params["page"] = "home"
            st.rerun()
