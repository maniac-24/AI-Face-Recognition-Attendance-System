import cv2
import numpy as np

from database.models import load_approved_users, mark_attendance
from modules.face_recognition import get_embedding, yolo


# ---------------- NORMALIZE ---------------- #
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


# ---------------- FACE MATCH ---------------- #
def match_face(embedding, users, threshold=0.85):
    best_match = None
    min_dist = float("inf")

    for user_id, name, db_emb in users:
        dist = np.linalg.norm(embedding - db_emb)

        print(f"[DEBUG] {name} distance: {dist:.4f}")

        if dist < min_dist:
            min_dist = dist
            best_match = (user_id, name)

    print(f"[DEBUG] Best distance: {min_dist:.4f}")

    if min_dist < threshold:
        return best_match, min_dist
    else:
        return None, min_dist


# ---------------- START ATTENDANCE ---------------- #
def start_attendance():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "❌ Camera not accessible", None

    users = load_approved_users()

    if not users:
        cap.release()
        return "⚠️ No approved users found", None

    message = None
    preview_image = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("📸 Press 'q' to capture", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):

            embeddings = []

            # 🔁 Capture multiple frames for stability
            for _ in range(3):
                ret, temp_frame = cap.read()
                if not ret:
                    continue

                results = yolo(temp_frame)[0]

                if len(results.boxes) == 0:
                    continue

                x1, y1, x2, y2, _, _ = map(int, results.boxes.data[0].tolist())

                h, w, _ = temp_frame.shape

                # ✅ Add padding (VERY IMPORTANT)
                pad = 20
                x1 = max(0, x1 - pad)
                y1 = max(0, y1 - pad)
                x2 = min(w, x2 + pad)
                y2 = min(h, y2 + pad)

                face = temp_frame[y1:y2, x1:x2]

                # Save preview (last frame)
                preview_image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

                cv2.imshow("Detected Face", face)

                emb = get_embedding(face)

                if emb is not None:
                    embeddings.append(normalize(emb))

            # ❌ No valid embeddings
            if len(embeddings) == 0:
                message = "❌ Face encoding failed"
                break

            # ✅ Average embedding
            final_embedding = np.mean(embeddings, axis=0)

            # ---------------- MATCH ---------------- #
            match, dist = match_face(final_embedding, users)

            if match:
                user_id, name = match

                message = f"✅ {mark_attendance(user_id, name)} (distance: {dist:.2f})"

                cv2.putText(
                    frame,
                    f"Hello {name}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            else:
                message = f"❌ Face not recognized (distance: {dist:.2f})"

            break

    cap.release()
    cv2.destroyAllWindows()

    return message, preview_image