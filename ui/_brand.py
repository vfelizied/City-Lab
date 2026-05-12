import streamlit as st

def inject_brand():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&family=JetBrains+Mono:wght@400&display=swap');

        :root {
            --primary: #0F172A;
            --secondary: #F1F5F9;
            --accent: #22C55E;
            --bg: #FFFFFF;
            --surface: #F8FAFC;
            --text: #0F172A;

            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 16px;
        }

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
            background-color: var(--bg);
            color: var(--text);
        }

        h1, h2, h3 {
            font-family: 'Syne', sans-serif;
            color: var(--primary);
            letter-spacing: -0.02em;
        }

        /* BUTTONS */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            border-radius: var(--radius-md);
            border: none;
            padding: 10px 16px;
            font-weight: 500;
        }

        .stButton > button:hover {
            opacity: 0.92;
        }

        /* INPUTS */
        .stTextInput input, .stTextArea textarea, .stSelectbox div {
            border-radius: var(--radius-md);
            border: 1px solid #E2E8F0;
            background: var(--surface);
        }

        /* CARDS */
        div[data-testid="stForm"] {
            background: var(--surface);
            border-radius: var(--radius-lg);
            padding: 20px;
            border: 1px solid #E2E8F0;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: var(--secondary);
        }

        /* STATUS TEXT */
        .status {
            font-family: 'JetBrains Mono', monospace;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
