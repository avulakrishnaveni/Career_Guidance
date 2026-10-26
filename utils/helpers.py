import re
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from extensions import db
from models import Notification, Activity

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MOBILE_RE = re.compile(r"^[6-9]\d{9}$")
EXP_RANGES = {"Fresher": (0, 1), "Junior": (1, 3), "Mid": (3, 6), "Senior": (6, 50)}


def err(msg, code=400, **extra):
    return jsonify({"error": msg, **extra}), code


def uid():
    return int(get_jwt_identity())


def password_problem(pw):
    if len(pw) < 8: return "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", pw): return "Password needs an uppercase letter"
    if not re.search(r"[a-z]", pw): return "Password needs a lowercase letter"
    if not re.search(r"\d", pw): return "Password needs a number"
    if not re.search(r"[^A-Za-z0-9]", pw): return "Password needs a special character"
    return None


def notify(user_id, title, message):
    db.session.add(Notification(user_id=user_id, title=title, message=message))


def log_activity(user_id, kind, detail=""):
    """Record an activity, then refresh today's readiness snapshot so the report stays current."""
    db.session.add(Activity(user_id=user_id, kind=kind, detail=detail[:200]))
    db.session.commit()
    try:
        from utils.readiness import snapshot
        snapshot(user_id)
    except Exception as e:  # never break the main action because of the report
        db.session.rollback()
        print("readiness snapshot failed:", e)


def streak(user_id, kind=None):
    q = db.session.query(db.func.date(Activity.created_at)).filter(Activity.user_id == user_id)
    if kind: q = q.filter(Activity.kind == kind)
    days = {str(r[0]) for r in q.distinct()}
    d = datetime.utcnow().date()
    if d.isoformat() not in days: d -= timedelta(days=1)
    n = 0
    while d.isoformat() in days:
        n += 1; d -= timedelta(days=1)
    return n


def completeness(p):
    if p is None:
        return 0, ["Profile type", "Education or work details", "Skills", "Bio", "LinkedIn", "GitHub", "Profile photo"]
    items = [("Profile type", p.profile_type)]
    if p.profile_type == "employee":
        items += [("Company", p.company), ("Designation", p.designation), ("Work start year", p.work_start_year), ("Total experience", p.total_experience)]
    else:
        items += [("Education level", p.education_level), ("College/School", p.institution), ("Education years", p.edu_start_year and p.edu_end_year),
                  ("Degree", p.degree), ("Branch", p.branch), ("CGPA/Percentage", p.grade)]
    items += [("At least 3 skills", len(p.skills or []) >= 3), ("Bio", p.bio), ("LinkedIn link", p.linkedin), ("GitHub link", p.github), ("Profile photo", p.photo)]
    done = [bool(v) for _, v in items]
    return round(sum(done) / len(items) * 100), [l for (l, _), d in zip(items, done) if not d]


def years_of_experience(p):
    if not p or p.profile_type != "employee" or not p.total_experience: return 0.0
    m = re.search(r"\d+(\.\d+)?", p.total_experience)
    return float(m.group()) if m else 0.0


def _hit(needle, haystack):
    n = needle.lower()
    return any(n == h or (len(n) >= 3 and len(h) >= 3 and (n in h or h in n)) for h in haystack)


def skill_overlap(required, have):
    have = [s.lower() for s in (have or [])]
    matched = [r for r in required if _hit(r, have)]
    return matched, [r for r in required if r not in matched]


def job_match(job, skills, domain, years):
    matched, _ = skill_overlap(job.skills or [], skills)
    skill_pct = len(matched) / len(job.skills) if job.skills else 0
    lo, hi = EXP_RANGES.get(job.experience_level, (0, 50))
    gap = 0 if lo <= years <= hi else (lo - years if years < lo else years - hi)
    exp = 1 if gap == 0 else (0.5 if gap <= 1 else 0)
    return round(skill_pct * 60 + (30 if domain and job.domain == domain else 0) + exp * 10)
