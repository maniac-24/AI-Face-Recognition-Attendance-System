import streamlit as st

def login():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if (
            username == st.secrets["admin"]["username"]
            and password == st.secrets["admin"]["password"]
        ):
            st.session_state["admin_logged_in"] = True
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")


def logout():
    st.session_state["admin_logged_in"] = False
    st.success("Logged out successfully")
    st.rerun()