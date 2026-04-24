import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
from database.db import get_conn


# ---------------- REGISTER USER ---------------- #
def register_user(name, email, phone, dob, face, emb):
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()

        _, img = cv2.imencode('.jpg', face)

        cursor.execute(
            """
            INSERT INTO users 
            (name, email, phone, dob, embedding, photo, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            name,
            email,
            phone,
            dob,
            emb.astype(np.float32).tobytes(),
            img.tobytes(),
            datetime.now()
        )

        conn.commit()
        load_users.clear()

    except Exception as e:
        st.error(f"Registration failed: {e}")

    finally:
        if conn:
            conn.close()


# ---------------- LOAD APPROVED USERS (FOR FACE MATCHING) ---------------- #
@st.cache_data(ttl=60)
def load_users():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, embedding 
        FROM users 
        WHERE status='approved'
    """)

    users = [
        (r.id, r.name, np.frombuffer(r.embedding, dtype=np.float32))
        for r in cursor.fetchall()
    ]

    conn.close()
    return users


# ---------------- LOAD DASHBOARD DATA ---------------- #
def load_data():
    conn = get_conn()

    df = pd.read_sql("""
        SELECT a.name, a.date, a.check_in, a.check_out, a.status, u.photo
        FROM attendance a
        JOIN users u ON a.user_id = u.id
        WHERE u.status = 'approved'
    """, conn)

    conn.close()

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date

    return df


# ---------------- ADMIN: GET PENDING USERS ---------------- #
def get_pending_users():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, photo, email, dob, phone
        FROM users
        WHERE status='pending'
    """)

    users = cursor.fetchall()
    conn.close()
    return users


# ---------------- ADMIN: GET ALL USERS ---------------- #
def get_all_users():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, photo, email, dob, phone, status, rejection_reason
        FROM users
    """)

    users = [tuple(row) for row in cursor.fetchall()]

    conn.close()
    return users

# ---------------- ADMIN: UPDATE STATUS ---------------- #
def update_user_status(user_id, status, reason=None):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users 
        SET status=?, rejection_reason=?, updated_at=?
        WHERE id=?
        """,
        status,
        reason,
        datetime.now(),
        user_id
    )

    conn.commit()
    conn.close()


# ---------------- ADMIN: DELETE USER ---------------- #
def delete_user(user_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    conn.commit()
    conn.close()


# ---------------- OPTIONAL: GET USER COUNT STATS ---------------- #
def get_user_stats():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            SUM(CASE WHEN status='approved' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) AS rejected
        FROM users
    """)

    result = cursor.fetchone()
    conn.close()

    return {
        "approved": result.approved or 0,
        "pending": result.pending or 0,
        "rejected": result.rejected or 0
    }