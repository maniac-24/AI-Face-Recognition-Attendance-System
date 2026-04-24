def img_to_base64(blob, mime_type="image/jpeg"):
    if blob is None:
        return "https://api.dicebear.com/7.x/initials/svg?seed=User"

    try:
        encoded = base64.b64encode(blob).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"
    except Exception:
        return None