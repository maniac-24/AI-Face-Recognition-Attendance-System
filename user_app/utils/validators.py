import re


# ---------------- REGISTRATION VALIDATION ---------------- #
def validate_registration_input(name, email, phone, dob, img):
    if not name.strip():
        return False, "Name is required"

    if not email.strip():
        return False, "Email is required"

    # Basic email format check
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    if not phone.strip():
        return False, "Phone number is required"

    # Simple phone validation (10 digits)
    if not phone.isdigit() or len(phone) != 10:
        return False, "Phone must be 10 digits"

    if not dob:
        return False, "Date of Birth is required"

    if img is None:
        return False, "Please capture your face"

    return True, ""


# ---------------- FACE DETECTION VALIDATION ---------------- #
def validate_face_count(results):
    try:
        if len(results.boxes.data) == 0:
            return False, "❌ No face detected"

        if len(results.boxes.data) > 1:
            return False, "❌ Multiple faces detected"

        return True, ""

    except Exception:
        return False, "❌ Face detection failed"


# ---------------- EMAIL ONLY VALIDATION (STATUS PAGE) ---------------- #
def validate_email_input(email):
    if not email.strip():
        return False, "Email is required"

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, ""