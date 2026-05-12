import streamlit as st

from config import APP_TITLE
from data.database import initialize_database
from ui._brand import inject_brand_styles
from ui.home_page import render_home_page

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

initialize_database()
inject_brand_styles()

st.title(APP_TITLE)

render_home_page()
