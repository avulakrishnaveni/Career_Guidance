from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Profile, User
from utils.helpers import err, uid, completeness, log_activity

bp = Blueprint("profile", __name__)


def _payload(p, u):
    pct, missing = completeness(p)
    return {"user": {"name": u.name, "email": u.email, "mobile": u.mobile}, "profile": p.to_dict() if p else None, "completeness": pct, "missing": missing}


@bp.get("/profile")
@jwt_required()
def get_profile():
    return jsonify(_payload(Profile.query.filter_by(user_id=uid()).first(), db.session.get(User, uid())))


@bp.route("/profile", methods=["POST", "PUT"])
@jwt_required()
def save_profile():
    d = request.get_json(silent=True) or {}
    if d.get("profile_type") not in ("student", "employee"): return err("Choose Student or Working Professional")
    if d["profile_type"] == "student" and not (d.get("education_level") and d.get("institution")):
        return err("Education level and college/school name are required")
    if d["profile_type"] == "employee" and not (d.get("company") and d.get("designation")):
        return err("Company and designation are required")
    skills = d.get("skills", [])
    if isinstance(skills, str): skills = [s.strip() for s in skills.split(",")]
    d["skills"] = [s.strip()[:40] for s in skills if s and s.strip()][:40]
    if d.get("photo") and (not str(d["photo"]).startswith("data:image/") or len(d["photo"]) > 400_000):
        return err("Profile photo must be an image under 300 KB")
    for k in ("linkedin", "github"):
        if d.get(k) and not str(d[k]).startswith("http"): return err(f"{k.capitalize()} link must start with http:// or https://")
    p = Profile.query.filter_by(user_id=uid()).first() or Profile(user_id=uid())
    for f in Profile.FIELDS:
        if f in d: setattr(p, f, d[f])
    db.session.add(p); db.session.commit()
    log_activity(uid(), "profile", "Updated profile")
    return jsonify({**_payload(p, db.session.get(User, uid())), "message": "Profile saved"})
