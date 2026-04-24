import streamlit as st
from modules.attendance import start_attendance

def show_attendance():
    st.subheader("📸 Mark Attendance")

    if st.button("Start Camera"):
        message, img = start_attendance()

        if img is not None:
            st.image(img, caption="Captured Face", width=200)

        if "✅" in message:
            st.success(message)
        else:
            st.error(message)