# ===============================
# 📌 USER STATUS
# ===============================

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"


# ===============================
# 📌 ATTENDANCE STATUS
# ===============================

ATTENDANCE_FULL_DAY = "Full Day"
ATTENDANCE_LATE_FULL_DAY = "Late Full Day"
ATTENDANCE_HALF_DAY = "Half Day"
ATTENDANCE_EARLY_LEAVE = "Early Leave"
ATTENDANCE_IN_PROGRESS = "In Progress"


VALID_PRESENT_STATUSES = [
    ATTENDANCE_FULL_DAY,
    ATTENDANCE_LATE_FULL_DAY,
    ATTENDANCE_HALF_DAY
]


VALID_LATE_STATUSES = [
    ATTENDANCE_LATE_FULL_DAY,
    ATTENDANCE_HALF_DAY
]


# ===============================
# 📌 TIME SETTINGS
# ===============================

CHECK_IN_TIME = "09:00"
CHECK_OUT_TIME = "17:00"


# ===============================
# 📌 FACE RECOGNITION
# ===============================

FACE_MATCH_THRESHOLD = 0.75
FACE_IMAGE_SIZE = (160, 160)


# ===============================
# 📌 UI LABELS
# ===============================

APP_TITLE = "AI Face Recognition Attendance System"
ADMIN_PANEL_TITLE = "Admin Approval Panel"
DASHBOARD_TITLE = "Attendance Dashboard"


# ===============================
# 📌 EMAIL SUBJECTS
# ===============================

EMAIL_APPROVED_SUBJECT = "Verification Approved"
EMAIL_REJECTED_SUBJECT = "Verification Rejected"


# ===============================
# 📌 MESSAGES
# ===============================

MSG_APPROVED = "Your attendance verification is complete. You can now mark attendance."
MSG_REJECTED = "Your verification was rejected. Please register again."
MSG_PENDING = "Your registration is under verification."


# ===============================
# 📌 PAGINATION
# ===============================

DEFAULT_ROWS_PER_PAGE = 10


# ===============================
# 📌 FILE PATHS
# ===============================

YOLO_MODEL_PATH = "models/yolov8n.pt"