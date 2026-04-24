import cv2
import numpy as np
from datetime import datetime
from database.db import get_conn


# ---------------- REGISTER USER ---------------- #
def register_user(name, email, phone, dob, face_img, embedding):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Encode face image
        _, img_encoded = cv2.imencode('.jpg', face_img)

        cursor.execute(
            """
            INSERT INTO users 
            (name, email, phone, dob, embedding, photo, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', GETDATE())
            """,
            (
                name,
                email,
                phone,
                dob,
                embedding.astype(np.float32).tobytes(),
                img_encoded.tobytes()
            )
        )

        conn.commit()
        return True, "✅ Registration successful! Wait for admin approval."

    except Exception as e:
        return False, f"❌ Registration failed: {e}"

    finally:
        if conn:
            conn.close()


# ---------------- GET USER STATUS ---------------- #
def get_user_status(email):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, status, rejection_reason
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    return user  # (name, status, reason)


# ---------------- LOAD APPROVED USERS ---------------- #
def load_approved_users():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, embedding
        FROM users
        WHERE status='approved'
        """
    )

    users = [
        (
            row[0],
            row[1],
            np.frombuffer(row[2], dtype=np.float32)
        )
        for row in cursor.fetchall()
    ]

    conn.close()
    return users


# ---------------- MARK ATTENDANCE ---------------- #
def mark_attendance(user_id, name):
    conn = get_conn()
    cursor = conn.cursor()

    now = datetime.now()
    today = now.date()

    # Check existing record
    cursor.execute(
        """
        SELECT id, check_in, check_out 
        FROM attendance
        WHERE user_id=? AND date=?
        """,
        (user_id, today)
    )

    record = cursor.fetchone()

    if record is None:
        # First entry → Check-in
        cursor.execute(
            """
            INSERT INTO attendance (user_id, name, date, check_in, status)
            VALUES (?, ?, ?, ?, 'Present')
            """,
            (user_id, name, today, now)
        )
        message = f"✅ Check-in recorded for {name}"

    else:
        # Update check-out
        cursor.execute(
            """
            UPDATE attendance
            SET check_out=?
            WHERE user_id=? AND date=?
            """,
            (now, user_id, today)
        )
        message = f"👋 Check-out recorded for {name}"

    conn.commit()
    conn.close()

    return message