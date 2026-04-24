import re


def validate_registration_input(name, email, phone, dob, img):
    if not name or name.strip() == "":
        return False, "Enter valid name"

    if not email or not validate_email(email):
        return False, "Enter valid email"

    if not phone or not validate_phone(phone):
        return False, "Enter valid phone number"

    if not dob:
        return False, "Select date of birth"

    if not img:
        return False, "Capture face image"

    return True, ""


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def validate_phone(phone):
    return phone.isdigit() and len(phone) in [10, 12]


def validate_face_count(results):
    if len(results.boxes.data) == 0:
        return False, "❌ No face detected"

    if len(results.boxes.data) > 1:
        return False, "❌ Multiple faces detected"

    return True, ""