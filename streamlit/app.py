import streamlit as st

# --- BLOCKBUSTER THEME (INLINE CSS) ---
st.markdown(
    """
    <style>

    /* White background everywhere */
    .main, body, html {
        background-color: #FFFFFF !important;
    }

    /* Sidebar also white */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
    }

    /* Headings = Blockbuster Yellow */
    h1, h2, h3 {
        color: #FFD200 !important;
        font-weight: 700 !important;
    }

    /* All normal text = Blockbuster Blue */
    p, div, span, label {
        color: #0046AD !important;
    }

    /* Buttons, sliders, radio buttons etc. (yellow highlight) */
    .stSlider > div > div > div[data-testid="stTickBar"] div {
        background-color: #FFD200 !important;
    }
    .stSlider > div > div > div[data-testid="stSliderThumb"] {
        background-color: #FFD200 !important;
        border: 2px solid #0046AD !important;
    }

    /* Radio buttons */
    div[role="radiogroup"] label {
        color: #0046AD !important;
    }

    /* Select dropdown text */
    .stSelectbox div[data-baseweb="select"] * {
        color: #0046AD !important;
    }

    /* Banners (info/success/warning boxes) */
    div[data-testid="stAlert"] {
        border-radius: 8px;
        border-left: 6px solid #FFD200;
        background-color: #FFF9E0;
        color: #0046AD !important;
    }
    div[data-testid="stAlert"] svg {
        fill: #FFD200 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Blockbuster Rental Analytics",
    layout="wide",
)

st.title("🎬 Blockbuster Rental Analytics Dashboard")

st.write(
    """
Welcome to the team dashboard for the DVD rental project.

Use the **menu on the left** to navigate to each person's analysis page:

- **page1-Sailesh** – Blockbuster insights by revenue and category
- **page2-Sophia** – Blockbuster insights by category, country, rating & customers
- **page3-Gurvir** – Blockbuster insights by customer country 
- **page3-Daniel** - Blockbuster insights by film ratings

Each page can have its own visuals, filters and commentary.
"""
)


st.caption("This landing page is just a simple entry point. All the detailed analysis lives on the individual pages.")
