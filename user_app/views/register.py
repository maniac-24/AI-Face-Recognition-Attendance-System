import streamlit as st
import cv2
import numpy as np

from database.models import register_user
from modules.face_recognition import get_embedding
from utils.validators import validate_registration_input, validate_face_count

# ⚠️ If YOLO is optional, import safely
try:
    from modules.face_recognition import yolo
except:
    yolo = None


def show_register():
    st.subheader("📝 User Registration")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone")
    dob = st.date_input("Date of Birth")

    st.warning("📸 Capture a clear face (only one person)")

    img = st.camera_input("Capture Face")

    if st.button("Register"):

        # ---------------- VALIDATE INPUT ---------------- #
        is_valid, msg = validate_registration_input(name, email, phone, dob, img)
        if not is_valid:
            st.error(msg)
            return

        # ---------------- IMAGE PROCESS ---------------- #
        frame = cv2.imdecode(
            np.frombuffer(img.read(), np.uint8),
            cv2.IMREAD_COLOR
        )

        # ---------------- FACE DETECTION ---------------- #
        if yolo:
            results = yolo(frame)[0]

            is_valid_face, face_msg = validate_face_count(results)
            if not is_valid_face:
                st.error(face_msg)
                return

            x1, y1, x2, y2, _, _ = map(int, results.boxes.data[0].tolist())

            h, w, _ = frame.shape
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            face = frame[y1:y2, x1:x2]

        else:
            # fallback (no YOLO)
            face = frame

        st.image(face, caption="Captured Face", width=150)

        # ---------------- EMBEDDING ---------------- #
        emb = get_embedding(face)

        if emb is None:
            st.error("❌ Face not detected properly. Try again.")
            return

        # ---------------- SAVE TO DB ---------------- #
        success, message = register_user(name, email, phone, dob, face, emb)

        if success:
            st.success(message)
        else:
            st.error(message)