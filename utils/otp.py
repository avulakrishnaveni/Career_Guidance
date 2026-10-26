import os, random
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


def send_otp_email(email, code, purpose):
    # DEMO: OTP is printed to the backend terminal.
    print(f"\n[CareerVerse OTP] {purpose} code for {email}: {code}\n", flush=True)
    # PRODUCTION: set MAIL_SERVER etc. in .env; Flask-Mail then sends a real email.
    if os.getenv("MAIL_SERVER"):
        try:
            from flask_mail import Mail, Message
            Mail(current_app).send(Message("Your CareerVerse verification code", recipients=[email],
                                           body=f"Your code is {code}. It expires in 10 minutes."))
        except Exception as e:
            print("Email sending failed:", e)


def issue_otp(user, purpose):
    code = f"{random.SystemRandom().randint(0, 999999):06d}"
    user.otp_hash = generate_password_hash(code)
    user.otp_purpose = purpose
    user.otp_expires = datetime.utcnow() + timedelta(minutes=10)
    user.otp_attempts = 0
    send_otp_email(user.email, code, purpose)
    return code


def check_otp(user, purpose, code):
    if not user.otp_hash or user.otp_purpose != purpose: return False, "Request a new code first"
    if datetime.utcnow() > user.otp_expires: return False, "Code expired. Request a new one"
    if (user.otp_attempts or 0) >= 5: return False, "Too many attempts. Request a new code"
    user.otp_attempts = (user.otp_attempts or 0) + 1
    if not check_password_hash(user.otp_hash, str(code).strip()): return False, "Incorrect code"
    user.otp_hash = None
    return True, ""
