import streamlit as st
from datetime import datetime
from database.db import get_conn
from services.email_service import send_email

def mark_attendance(uid, name):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # 🔐 Check approval
        cursor.execute("SELECT status FROM users WHERE id=?", uid)
        user_status = cursor.fetchone()

        if user_status and user_status.status != "approved":
            st.error("❌ Your account is not approved yet")
            return

        today = datetime.now().date()
        now = datetime.now()

        check_in_time = datetime.strptime("09:00", "%H:%M").time()
        check_out_time = datetime.strptime("17:00", "%H:%M").time()

        cursor.execute("SELECT * FROM attendance WHERE user_id=? AND date=?", uid, today)
        record = cursor.fetchone()

        # CHECK-IN
        if record is None:
            cursor.execute(
                "INSERT INTO attendance (user_id, name, date, check_in, status) VALUES (?, ?, ?, ?, ?)",
                uid, name, today, now, "In Progress"
            )
            send_email("Check-In", f"{name} checked in at {now}")
            st.success(f"✅ {name} checked in successfully")

        # Prevent duplicate check-out
        elif record.check_out is not None:
            st.warning("⚠️ Attendance already completed for today")
            return

        # CHECK-OUT
        else:
            check_in = record.check_in.time()
            check_out = now.time()

            if check_in <= check_in_time and check_out >= check_out_time:
                status = "Full Day"
            elif check_in > check_in_time and check_out >= check_out_time:
                status = "Late Full Day"
            elif check_out < check_out_time:
                status = "Half Day"
            else:
                status = "Half Day"

            cursor.execute(
                "UPDATE attendance SET check_out=?, status=? WHERE id=?",
                now, status, record.id
            )

            send_email("Check-Out", f"{name} checked out at {now} ({status})")
            st.success(f"✅ {name} checked out ({status})")

        conn.commit()

    except Exception as e:
        st.error(f"Error marking attendance: {e}")

    finally:
        if conn:
            conn.close()