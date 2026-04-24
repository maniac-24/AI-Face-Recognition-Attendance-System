import streamlit as st


def show_navbar(title="AI Attendance System"):
    col1, col2, col3 = st.columns([6, 2, 1])

    # 🏷️ Title
    with col1:
        st.markdown(f"### 🤖 {title}")

    # 👤 Admin Info
    with col2:
        if st.session_state.get("admin_logged_in"):
            st.markdown("👤 **Admin**")

    # 🚪 Logout
    with col3:
        if st.session_state.get("admin_logged_in"):
            if st.button("Logout"):
                st.session_state["admin_logged_in"] = False
                st.rerun()

    st.markdown("---")