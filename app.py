# /app.py

```python
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = "ciudad_lab.db"
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Ciudad Lab MVP", layout="wide")


# -----------------------------
# DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            neighborhood TEXT,
            category TEXT,
            status TEXT,
            support_count INTEGER,
            image_path TEXT,
            created_at TEXT
        )
        """
    )

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# HELPERS
# -----------------------------
def create_report(title, description, neighborhood, category, image_file):
    image_path = ""

    if image_file:
        file_path = UPLOAD_DIR / image_file.name
        with open(file_path, "wb") as f:
            f.write(image_file.getbuffer())
        image_path = str(file_path)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports (
            title,
            description,
            neighborhood,
            category,
            status,
            support_count,
            image_path,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            neighborhood,
            category,
            "Recibido",
            1,
            image_path,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )

    conn.commit()
    conn.close()



def get_reports():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM reports ORDER BY id DESC",
        conn
    )

    conn.close()
    return df



def support_report(report_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reports
        SET support_count = support_count + 1
        WHERE id = ?
        """,
        (report_id,)
    )

    conn.commit()
    conn.close()


# -----------------------------
# UI
# -----------------------------
st.title("Ciudad Lab MVP")
st.caption("Reporta problemáticas reales de tu barrio")

left_col, right_col = st.columns([1, 1.2])


# -----------------------------
# CREATE REPORT
# -----------------------------
with left_col:
    st.subheader("Nuevo reporte")

    with st.form("report_form"):
        title = st.text_input("Título del problema")

        neighborhood = st.text_input("Barrio")

        category = st.selectbox(
            "Categoría",
            [
                "Basura",
                "Iluminación",
                "Huecos",
                "Ruido",
                "Seguridad",
                "Espacios públicos",
                "Otro"
            ]
        )

        description = st.text_area(
            "Describe qué está pasando"
        )

        image = st.file_uploader(
            "Sube una foto",
            type=["png", "jpg", "jpeg"]
        )

        submitted = st.form_submit_button("Enviar reporte")

        if submitted:
            if not title or not neighborhood or not description:
                st.error("Completa todos los campos obligatorios.")
            else:
                create_report(
                    title,
                    description,
                    neighborhood,
                    category,
                    image
                )

                st.success("Reporte enviado correctamente.")
                st.rerun()


# -----------------------------
# PUBLIC FEED
# -----------------------------
with right_col:
    st.subheader("Reportes activos")

    reports_df = get_reports()

    if reports_df.empty:
        st.info("Todavía no hay reportes.")

    else:
        for _, row in reports_df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"### {row['title']}")
                    st.write(row['description'])

                    st.caption(
                        f"📍 {row['neighborhood']} · "
                        f"{row['category']} · "
                        f"{row['created_at']}"
                    )

                    st.markdown(
                        f"**Estado:** {row['status']}"
                    )

                    st.markdown(
                        f"**Apoyos vecinales:** {row['support_count']}"
                    )

                    if row['image_path']:
                        st.image(row['image_path'])

                with col2:
                    if st.button(
                        "Apoyar",
                        key=f"support_{row['id']}"
                    ):
                        support_report(row['id'])
                        st.rerun()


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("Objetivo")

    st.write(
        "Este MVP combate el vacío institucional "
        "mostrando reportes públicos y visibles "
        "para cada barrio."
    )

    st.divider()

    st.header("Estados")

    st.markdown(
        "- Recibido\n"
        "- En revisión\n"
        "- Priorizado"
    )
```

---

# /requirements.txt

```txt
streamlit==1.39.0
pandas==2.2.3
```

---

# /runtime.txt

```txt
python-3.11
```

---

# /README.md

```md
# Ciudad Lab MVP

MVP de participación ciudadana construido con Streamlit.

## Features

- Crear reportes ciudadanos
- Subir imágenes
- Feed público de incidentes
- Sistema de apoyos vecinales
- Estados visibles de seguimiento

## Deploy

1. Sube este repositorio a GitHub
2. Ve a share.streamlit.io
3. Conecta el repo
4. Deploy
```
