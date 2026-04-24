import streamlit as st
from database.models import get_user_status


def show_status():
    st.subheader("🔍 Check Registration Status")

    email = st.text_input("Enter your registered Email")

    if st.button("Check Status"):

        if not email:
            st.warning("Please enter email")
            return

        user = get_user_status(email)

        if not user:
            st.error("❌ No user found with this email")
            return

        name, status, reason = user

        st.write(f"👤 Name: **{name}**")

        # ---------------- STATUS DISPLAY ---------------- #
        if status == "pending":
            st.warning("🟡 Your registration is under verification")

        elif status == "approved":
            st.success("🟢 You are approved! You can mark attendance now.")

        elif status == "rejected":
            st.error("🔴 Your registration was rejected")

            if reason:
                st.info(f"Reason: {reason}")

            st.write("Please register again with correct details.")

        else:
            st.write(f"Status: {status}")