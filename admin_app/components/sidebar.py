import streamlit as st

def show_sidebar():
    st.sidebar.title("📂 Navigation")

    menu = st.sidebar.radio(
        "Go to",
        [
            "Dashboard",
            "Analytics",
            "Admin Panel"
        ]
    )

    return menu