import math
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from extensions import db
from models import CareerSelection, LearningModule, Progress
from data import DOMAINS
from utils.helpers import err, uid, log_activity, streak

bp = Blueprint("career", __name__)
LEVELS, GOALS = ["Beginner", "Intermediate", "Advanced"], ["Job-ready", "Skill upgrade", "Career switch"]
HOURS_PER_WEEK = {"Job-ready": 10, "Skill upgrade": 8, "Career switch": 12}


def roadmap_for(user_id):
    cs = CareerSelection.query.filter_by(user_id=user_id).first()
    if not cs: return None
    mods = LearningModule.query.filter_by(domain=cs.domain).order_by(LearningModule.position).all()
    done = {r.module_id for r in Progress.query.filter_by(user_id=user_id, completed=True)}
    hpw, week, items = HOURS_PER_WEEK.get(cs.goal, 8), 1, []
    for m in mods:
        weeks = max(1, math.ceil(m.hours / hpw))
        items.append({"id": m.id, "position": m.position, "title": m.title, "hours": m.hours, "lessons": m.lessons, "resource": m.resource,
                      "start_week": week, "end_week": week + weeks - 1, "completed": m.id in done})
        week += weeks
    n_done = sum(i["completed"] for i in items)
    return {"path": cs.to_dict(), "milestones": items, "total_weeks": week - 1, "total_hours": sum(i["hours"] for i in items), "hours_per_week": hpw,
            "required_skills": DOMAINS[cs.domain]["skills"], "completed": n_done, "total": len(items), "percent": round(n_done / len(items) * 100) if items else 0}


@bp.get("/career/domains")
@jwt_required()
def domains():
    return jsonify({"domains": [{"name": k, "roles": v["roles"], "skills": v["skills"], "modules": len(v["modules"]), "hours": sum(m["hours"] for m in v["modules"])} for k, v in DOMAINS.items()],
                    "levels": LEVELS, "goals": GOALS})


@bp.post("/career/select")
@jwt_required()
def select():
    d = request.get_json(silent=True) or {}
    if d.get("domain") not in DOMAINS: return err("Choose a valid domain")
    if d.get("role") not in DOMAINS[d["domain"]]["roles"]: return err("Choose a role in this domain")
    c = CareerSelection.query.filter_by(user_id=uid()).first() or CareerSelection(user_id=uid())
    c.domain, c.role = d["domain"], d["role"]
    c.experience_level = d.get("experience_level") if d.get("experience_level") in LEVELS else "Beginner"
    c.goal = d.get("goal") if d.get("goal") in GOALS else "Job-ready"
    db.session.add(c); db.session.commit()
    log_activity(uid(), "career", f"Selected {c.domain} / {c.role}")
    return jsonify({"message": "Career path saved", "roadmap": roadmap_for(uid())})


@bp.get("/career/my-path")
@jwt_required()
def my_path():
    cs = CareerSelection.query.filter_by(user_id=uid()).first()
    return jsonify({"path": cs.to_dict() if cs else None})


@bp.get("/career/roadmap")
@jwt_required()
def roadmap():
    return jsonify({"roadmap": roadmap_for(uid())})


# ---- Learning & progress ----
@bp.get("/learning/roadmap")
@jwt_required()
def learning_roadmap():
    return jsonify({"roadmap": roadmap_for(uid())})


@bp.get("/progress")
@jwt_required()
def progress():
    r = roadmap_for(uid())
    if not r: return jsonify({"roadmap": None})
    week_ago = datetime.utcnow().timestamp() - 7 * 86400
    rows = Progress.query.filter_by(user_id=uid(), completed=True).all()
    this_week = sum(1 for x in rows if x.completed_at and x.completed_at.timestamp() >= week_ago)
    left = sum(m["hours"] for m in r["milestones"] if not m["completed"])
    return jsonify({"roadmap": r, "streak": streak(uid(), "learning"), "weekly_goal": {"target": 2, "done": this_week},
                    "hours_left": left, "weeks_left": math.ceil(left / r["hours_per_week"]) if left else 0})


@bp.post("/progress/update")
@jwt_required()
def progress_update():
    d = request.get_json(silent=True) or {}
    m = db.session.get(LearningModule, d.get("module_id"))
    if not m: return err("Module not found", 404)
    row = Progress.query.filter_by(user_id=uid(), module_id=m.id).first() or Progress(user_id=uid(), module_id=m.id)
    row.completed = bool(d.get("completed"))
    row.completed_at = datetime.utcnow() if row.completed else None
    db.session.add(row); db.session.commit()
    if row.completed: log_activity(uid(), "learning", f"Completed module: {m.title}")
    else: log_activity(uid(), "learning_undo", f"Reopened module: {m.title}")
    return progress()
