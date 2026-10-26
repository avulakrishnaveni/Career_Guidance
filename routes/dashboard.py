from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import Resume, InterviewSession, Activity, Notification, CodingChallenge, CodingSubmission
from utils.helpers import uid, streak
from utils.readiness import collect, history
from routes.career import roadmap_for

bp = Blueprint("dashboard", __name__)


@bp.get("/dashboard/stats")
@jwt_required()
def stats():
    u = uid()
    d = collect(u)
    pts = {c.id: c.points for c in CodingChallenge.query.all()}
    solved = {s.challenge_id for s in CodingSubmission.query.filter_by(user_id=u, passed=True)}
    resumes = Resume.query.filter_by(user_id=u).order_by(Resume.id).all()[-10:]
    sessions = InterviewSession.query.filter_by(user_id=u, completed=True).order_by(InterviewSession.id).all()[-10:]
    acts = Activity.query.filter_by(user_id=u).order_by(Activity.id.desc()).limit(10).all()
    rm = roadmap_for(u)
    return jsonify({
        "readiness": {"score": d["score"], "level": d["level"], "color": d["color"], "history": history(u, 14)},
        "profile": d["profile"], "career": rm["path"] if rm else None, "roadmap_percent": rm["percent"] if rm else 0,
        "resume_trend": [{"date": r.created_at.strftime("%d %b"), "score": r.score} for r in resumes],
        "interview_trend": [{"date": s.created_at.strftime("%d %b"), "score": s.avg_score, "category": s.category} for s in sessions],
        "coding": {"solved": len(solved), "success_rate": d["technical"]["success_rate"], "points": sum(pts.get(i, 0) for i in solved), "streak": streak(u, "coding")},
        "learning": d["learning"], "jobs": d["jobs"], "top_job": d["jobs"]["top"][0] if d["jobs"]["top"] else None,
        "badges": d["badges"], "streak": d["streak"], "actions": d["action_plan"]["actions"][:3],
        "activity": [{"kind": a.kind, "detail": a.detail, "at": a.created_at.isoformat() + "Z"} for a in acts],
        "unread": Notification.query.filter_by(user_id=u, read=False).count()})
