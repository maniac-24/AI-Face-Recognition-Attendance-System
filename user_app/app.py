import streamlit as st

from views.register import show_register
from views.status import show_status
from views.attendance import show_attendance

# ---------------- CONFIG ---------------- #
st.set_page_config(
    page_title="User Attendance System",
    layout="wide"
)

# ---------------- TITLE ---------------- #
st.title("👤 Smart Attendance - User Portal")

# ---------------- SIDEBAR ---------------- #
menu = st.sidebar.selectbox(
    "Menu",
    ["Register", "Check Status", "Mark Attendance"]
)

# ---------------- ROUTING ---------------- #
if menu == "Register":
    show_register()

elif menu == "Check Status":
    show_status()

elif menu == "Mark Attendance":
    show_attendance()