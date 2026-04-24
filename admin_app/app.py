import streamlit as st

# -------- IMPORTS -------- #
from database.models import load_data

from views.dashboard import show_dashboard
from views.analytics import show_analytics
from views.admin_panel import show_admin_panel

from components.sidebar import show_sidebar
from components.navbar import show_navbar

from modules.auth import login

# -------- CONFIG -------- #
st.set_page_config(page_title="Smart Attendance", layout="wide")

# -------- SESSION -------- #
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# -------- LOGIN -------- #
if not st.session_state.admin_logged_in:
    login()
    st.stop()

# -------- NAVBAR -------- #
show_navbar("Smart Attendance System")

# -------- LOAD DATA -------- #
df = load_data()

# -------- SIDEBAR -------- #
menu = show_sidebar()

# -------- ROUTING -------- #
if menu == "Dashboard":
    show_dashboard(df)

elif menu == "Analytics":
    show_analytics(df)

elif menu == "Admin Panel":
    show_admin_panel()
