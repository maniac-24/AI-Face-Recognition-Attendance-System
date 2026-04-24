import base64
import cv2
import numpy as np


# ---------------- IMAGE → BASE64 ---------------- #
def img_to_base64(blob):
    try:
        return "data:image/jpeg;base64," + base64.b64encode(blob).decode("utf-8")
    except:
        return None


# ---------------- CAMERA IMAGE → CV2 FRAME ---------------- #
def camera_to_frame(img_file):
    try:
        return cv2.imdecode(
            np.frombuffer(img_file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )
    except:
        return None


# ---------------- SAFE FACE CROP ---------------- #
def crop_face(frame, box):
    try:
        x1, y1, x2, y2 = map(int, box)

        h, w, _ = frame.shape

        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        return frame[y1:y2, x1:x2]

    except:
        return None


# ---------------- FORMAT DATETIME ---------------- #
def format_datetime(dt):
    try:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(dt)