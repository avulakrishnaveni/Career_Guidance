from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Job, JobApplication, Profile, CareerSelection
from utils.helpers import err, uid, job_match, years_of_experience, log_activity

bp = Blueprint("jobs", __name__)
STATUSES = ["Applied", "Interview", "Offer", "Rejected"]


def _ctx():
    p = Profile.query.filter_by(user_id=uid()).first()
    cs = CareerSelection.query.filter_by(user_id=uid()).first()
    return (p.skills if p else []) or [], (cs.domain if cs else None), years_of_experience(p)


@bp.get("/jobs")
@jwt_required()
def jobs():
    skills, domain, years = _ctx()
    a = request.args
    q = Job.query
    if a.get("domain"): q = q.filter_by(domain=a["domain"])
    if a.get("experience"): q = q.filter_by(experience_level=a["experience"])
    if a.get("job_type"): q = q.filter_by(job_type=a["job_type"])
    if a.get("location"): q = q.filter(Job.location.ilike(f"%{a['location']}%"))
    if a.get("q"): q = q.filter(Job.title.ilike(f"%{a['q']}%"))
    apps = {x.job_id: x for x in JobApplication.query.filter_by(user_id=uid()).all()}
    out = []
    for j in q.all():
        ap = apps.get(j.id)
        out.append({**j.to_dict(), "match": job_match(j, skills, domain, years), "saved": bool(ap and ap.saved), "status": ap.status if ap else None})
    out.sort(key=lambda x: -x["match"])
    if a.get("view") == "saved": out = [x for x in out if x["saved"]]
    return jsonify({"jobs": out, "domain": domain, "has_skills": bool(skills)})


def _row(job_id):
    return JobApplication.query.filter_by(user_id=uid(), job_id=job_id).first() or JobApplication(user_id=uid(), job_id=job_id)


@bp.post("/jobs/save")
@jwt_required()
def save():
    job = db.session.get(Job, (request.get_json(silent=True) or {}).get("job_id"))
    if not job: return err("Job not found", 404)
    r = _row(job.id); r.saved = not bool(r.saved); r.updated_at = datetime.utcnow()
    db.session.add(r); db.session.commit()
    return jsonify({"saved": r.saved})


@bp.post("/jobs/apply")
@jwt_required()
def apply():
    d = request.get_json(silent=True) or {}
    job = db.session.get(Job, d.get("job_id"))
    status = d.get("status") or "Applied"
    if not job: return err("Job not found", 404)
    if status not in STATUSES: return err("Invalid status")
    r = _row(job.id); r.status = status; r.updated_at = datetime.utcnow()
    db.session.add(r); db.session.commit()
    log_activity(uid(), "job", f"{status}: {job.title} at {job.company}")
    return jsonify({"status": r.status})


@bp.get("/jobs/applications")
@jwt_required()
def applications():
    rows = JobApplication.query.filter_by(user_id=uid()).filter(JobApplication.status.isnot(None)).order_by(JobApplication.updated_at.desc()).all()
    out = []
    for r in rows:
        j = db.session.get(Job, r.job_id)
        out.append({"job_id": j.id, "title": j.title, "company": j.company, "location": j.location, "status": r.status, "updated_at": r.updated_at.isoformat()})
    counts = {s: sum(1 for x in out if x["status"] == s) for s in STATUSES}
    return jsonify({"applications": out, "counts": counts, "statuses": STATUSES})
