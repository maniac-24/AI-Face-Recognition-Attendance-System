import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime

from database.models import (
    get_all_users,
    update_user_status,
    delete_user,
    load_data
)

from services.email_service import send_email


def show_admin_panel():
    st.title("🧑‍💼 Admin Control Panel")

    # ---------------- FILTER ---------------- #
    st.subheader("🔍 Filter Users")
    status_filter = st.selectbox(
        "Select Status",
        ["All", "pending", "approved", "rejected"]
    )

    # ---------------- LOAD USERS ---------------- #
    users = get_all_users()

    if not users:
        st.warning("No users found")
        return

    # ✅ Include photo column
    df_users = pd.DataFrame(users, columns=[
        "id", "name", "photo", "email", "dob",
        "phone", "status", "reason"
    ])

    # Apply filter
    if status_filter != "All":
        df_users = df_users[df_users["status"] == status_filter]

    # ---------------- TABLE VIEW ---------------- #
    st.subheader("📋 All Users (Table View)")
    st.dataframe(
        df_users.drop(columns=["photo"]),  # hide image in table
        use_container_width=True
    )

    st.markdown("---")

    # ---------------- CARD VIEW ---------------- #
    st.subheader("👤 User Actions")

    for _, row in df_users.iterrows():
        uid = row["id"]
        name = row["name"]
        email = row["email"]
        phone = row["phone"]
        dob = row["dob"]
        status = row["status"]
        reason = row["reason"]

        col1, col2 = st.columns([1, 3])

        # ---------------- IMAGE ---------------- #
        with col1:
            try:
                img = cv2.imdecode(
                    np.frombuffer(row["photo"], np.uint8),
                    cv2.IMREAD_COLOR
                )
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                st.image(img, width=130)

                # 🔍 View full image
                if st.button("🔍 View", key=f"view_{uid}"):
                    st.image(img, width=300)

            except:
                st.warning("No Image")

        # ---------------- DETAILS ---------------- #
        with col2:
            color = {
                "approved": "🟢",
                "rejected": "🔴",
                "pending": "🟡"
            }.get(status, "⚪")

            st.markdown(f"### {color} {name}")
            st.write(f"📧 {email}")
            st.write(f"📱 {phone}")
            st.write(f"🎂 {dob}")
            st.write(f"📌 Status: **{status}**")

            if reason:
                st.warning(f"Reason: {reason}")

            colA, colB, colC, colD = st.columns(4)

            # ✅ APPROVE
            with colA:
                if st.button("Approve", key=f"a_{uid}"):
                    update_user_status(uid, "approved")

                    send_email(
                        email,
                         "✅ Registration Approved - Smart Attendance System",
                        f""""
                        Hello {name}, 🎉 Congratulations!

                        Your registration has been successfully approved by the admin.

                        You can now:
                        ✔ Login to the system
                        ✔ Mark your attendance using face recognition
                        ✔ Access your dashboard and analytics

                        👉 Please ensure you mark attendance regularly.

                        If you face any issues, feel free to contact support.

                        Thank you,
                        Smart Attendance System
                        """
                    )

                    st.success("Approved")
                    st.rerun()

            # ❌ REJECT
            with colB:
                reject_reason = st.text_input(
                    "Reason", key=f"r_{uid}"
                )

                if st.button("Reject", key=f"rej_{uid}"):
                    if not reject_reason.strip():
                        st.warning("Enter reason")
                    else:
                        update_user_status(uid, "rejected", reject_reason)

                        send_email(
                            email,
                            "❌ Registration Rejected - Smart Attendance System",
                            f"""
                        Hello {name},

                        We regret to inform you that your registration request has been rejected.

                        📌 Reason:
                        {reject_reason}

                        👉 You can register again by:
                        ✔ Uploading a clear face image
                        ✔ Ensuring only one person is visible
                        ✔ Providing valid details

                        If you believe this was a mistake, please contact admin support.

                        Thank you,
                        Smart Attendance System
                        """
                        )

                        st.error("Rejected")
                        st.rerun()

            # 🔄 RESET
            with colC:
                if st.button("Reset", key=f"res_{uid}"):
                    update_user_status(uid, "pending")
                    st.info("Moved to pending")
                    st.rerun()

            # 🗑 DELETE
            with colD:
                confirm = st.checkbox("Confirm", key=f"c_{uid}")

                if st.button("Delete", key=f"d_{uid}"):
                    if confirm:
                        delete_user(uid)
                        st.warning("Deleted")
                        st.rerun()
                    else:
                        st.warning("Confirm delete first")

        st.markdown("---")

    # ---------------- ATTENDANCE MONITOR ---------------- #
    st.subheader("📊 Attendance Monitor (Today)")

    df = load_data()

    if not df.empty:
        today = datetime.today().date()
        today_df = df[df["date"] == today]

        present = set(today_df["name"])
        all_users = set(df["name"])
        absent = list(all_users - present)

        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ Present")
            st.write(list(present))

        with col2:
            st.error("❌ Absent")
            st.write(absent)
    else:
        st.warning("No attendance data available")