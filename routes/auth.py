import os
from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
from utils.helpers import err, notify, password_problem, EMAIL_RE, MOBILE_RE
from utils.otp import issue_otp, check_otp

bp = Blueprint("auth", __name__)
SHOW_OTP = os.getenv("SHOW_OTP_IN_RESPONSE", "false").lower() == "true"


def _otp_response(user, purpose, message):
    code = issue_otp(user, purpose)
    db.session.commit()
    out = {"message": message, "email": user.email}
    if SHOW_OTP: out["dev_otp"] = code  # demo only: disable in production
    return jsonify(out)


def _token_response(u):
    token = create_access_token(identity=str(u.id), expires_delta=timedelta(hours=24))
    return jsonify({"token": token, "user": {"id": u.id, "name": u.name, "email": u.email}})


@bp.post("/register")
def register():
    d = request.get_json(silent=True) or {}
    name, email = (d.get("name") or "").strip(), (d.get("email") or "").strip().lower()
    mobile, pw = (d.get("mobile") or "").strip(), d.get("password") or ""
    if len(name) < 2: return err("Enter your full name")
    if not EMAIL_RE.match(email): return err("Enter a valid email address")
    if not MOBILE_RE.match(mobile): return err("Mobile must be 10 digits starting with 6, 7, 8 or 9")
    p = password_problem(pw)
    if p: return err(p)
    u = User.query.filter_by(email=email).first()
    if u and u.verified: return err("This email is already registered", 409)
    if not u:
        u = User(email=email); db.session.add(u)
    u.name, u.mobile = name, mobile
    u.password_hash = generate_password_hash(pw)
    return _otp_response(u, "verify", "Verification code sent. Check your email (or the backend terminal in demo mode).")


@bp.post("/send-otp")
def send_otp():
    d = request.get_json(silent=True) or {}
    purpose = "reset" if d.get("purpose") == "reset" else "verify"
    u = User.query.filter_by(email=(d.get("email") or "").strip().lower()).first()
    if not u or (purpose == "verify" and u.verified): return jsonify({"message": "If the account exists, a code has been sent."})
    return _otp_response(u, purpose, "A new code has been sent.")


@bp.post("/verify-otp")
def verify_otp():
    d = request.get_json(silent=True) or {}
    u = User.query.filter_by(email=(d.get("email") or "").strip().lower()).first()
    if not u: return err("Account not found", 404)
    ok, msg = check_otp(u, "verify", d.get("otp") or "")
    db.session.commit()
    if not ok: return err(msg)
    u.verified = True
    notify(u.id, "Welcome to CareerVerse", "Complete your profile and pick a career path to get your Job Readiness Report.")
    db.session.commit()
    return _token_response(u)


@bp.post("/login")
def login():
    d = request.get_json(silent=True) or {}
    u = User.query.filter_by(email=(d.get("email") or "").strip().lower()).first()
    if not u or not check_password_hash(u.password_hash, d.get("password") or ""): return err("Incorrect email or password", 401)
    if not u.verified: return err("Verify your email to continue", 403, needs_verification=True, email=u.email)
    return _token_response(u)


@bp.post("/forgot-password")
def forgot_password():
    d = request.get_json(silent=True) or {}
    u = User.query.filter_by(email=(d.get("email") or "").strip().lower()).first()
    if u and u.verified: return _otp_response(u, "reset", "If the account exists, a reset code has been sent.")
    return jsonify({"message": "If the account exists, a reset code has been sent."})


@bp.post("/reset-password")
def reset_password():
    d = request.get_json(silent=True) or {}
    u = User.query.filter_by(email=(d.get("email") or "").strip().lower()).first()
    if not u: return err("Invalid code")
    p = password_problem(d.get("password") or "")
    if p: return err(p)
    ok, msg = check_otp(u, "reset", d.get("otp") or "")
    db.session.commit()
    if not ok: return err(msg)
    u.password_hash = generate_password_hash(d["password"])
    db.session.commit()
    return jsonify({"message": "Password updated. You can log in now."})
