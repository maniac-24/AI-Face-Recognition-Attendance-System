import smtplib
from email.mime.text import MIMEText
import streamlit as st

EMAIL_SENDER = st.secrets["email"]["sender"]
EMAIL_PASSWORD = st.secrets["email"]["password"]

def send_email(to_email, subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email   # ✅ send to user

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        server.quit()

    except Exception as e:
        st.error(f"Email Error: {e}")