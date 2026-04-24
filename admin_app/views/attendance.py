import streamlit as st
import cv2
import numpy as np
from database.models import load_users
from modules.face_recognition import yolo, get_embedding, recognize
from modules.attendance import mark_attendance

def show_attendance():
    st.subheader("📷 Mark Attendance")

    cam = st.camera_input("Capture")

    if cam:
        frame = cv2.imdecode(np.frombuffer(cam.read(), np.uint8), cv2.IMREAD_COLOR)
        results = yolo(frame)[0]

        if len(results.boxes.data) == 0:
            st.error("❌ No face detected")
            return

        if len(results.boxes.data) > 1:
            st.error("❌ Multiple faces detected")
            return

        users = load_users()

        if not users:
            st.warning("⚠️ No approved users found")
            return

        x1, y1, x2, y2, _, _ = map(int, results.boxes.data[0].tolist())

        h, w, _ = frame.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        face = frame[y1:y2, x1:x2]

        emb = get_embedding(face)

        match, score = recognize(emb, users)

        if match:
            uid, name = match
            st.success(f"✅ Recognized: {name} ({score:.2f})")
            mark_attendance(uid, name)
            label = name
        else:
            st.warning(f"⚠️ Unknown Person ({score:.2f})")
            label = "Unknown"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))