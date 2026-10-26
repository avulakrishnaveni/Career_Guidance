import random
from collections import Counter
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import InterviewSession
from data import INTERVIEW_QUESTIONS
from utils.helpers import err, uid, log_activity, notify
from utils.interview_eval import evaluate

bp = Blueprint("interview", __name__)
QUESTIONS = [{**q, "id": i + 1} for i, q in enumerate(INTERVIEW_QUESTIONS)]
CATEGORIES = ["HR", "Technical", "Behavioral", "Situational"]
public = lambda q: {k: v for k, v in q.items() if k != "keywords"}


@bp.get("/interview/questions")
@jwt_required()
def questions():
    cat = request.args.get("category")
    return jsonify({"categories": CATEGORIES, "questions": [public(q) for q in QUESTIONS if not cat or q["category"] == cat]})


@bp.post("/interview/start")
@jwt_required()
def start():
    d = request.get_json(silent=True) or {}
    cat = d.get("category")
    if cat not in CATEGORIES: return err("Choose HR, Technical, Behavioral or Situational")
    pool = [q for q in QUESTIONS if q["category"] == cat]
    try: count = max(1, min(int(d.get("count") or 5), len(pool)))
    except (TypeError, ValueError): count = 5
    chosen = random.sample(pool, count)
    s = InterviewSession(user_id=uid(), category=cat, question_ids=[q["id"] for q in chosen], answers=[])
    db.session.add(s); db.session.commit()
    return jsonify({"session_id": s.id, "category": cat, "questions": [public(q) for q in chosen]})


def _final(s):
    tips = Counter(t for a in s.answers for t in a["improvements"])
    return {"avg_score": s.avg_score, "category": s.category, "answered": len(s.answers),
            "per_question": [{"question": QUESTIONS[a["question_id"] - 1]["question"], "score": a["score"]} for a in s.answers],
            "top_improvements": [t for t, _ in tips.most_common(3)],
            "verdict": "Excellent" if s.avg_score >= 8 else "Good" if s.avg_score >= 6 else "Needs practice"}


@bp.post("/interview/submit")
@jwt_required()
def submit():
    d = request.get_json(silent=True) or {}
    s = InterviewSession.query.filter_by(id=d.get("session_id"), user_id=uid()).first()
    q = next((x for x in QUESTIONS if x["id"] == d.get("question_id")), None)
    ans = (d.get("answer") or "").strip()
    if not s or not q or q["id"] not in s.question_ids: return err("Interview session or question not found", 404)
    if not ans: return err("No answer recorded")
    fb = evaluate(q, ans[:3000])
    rec = {"question_id": q["id"], "answer": ans[:3000], **{k: fb[k] for k in ("score", "strengths", "improvements", "star")}}
    s.answers = [a for a in (s.answers or []) if a["question_id"] != q["id"]] + [rec]   # reassign so JSON change is detected
    s.avg_score = round(sum(a["score"] for a in s.answers) / len(s.answers), 1)
    complete = len(s.answers) >= len(s.question_ids)
    if complete and not s.completed:
        s.completed = True
        notify(uid(), "Interview complete", f"{s.category} interview: average score {s.avg_score}/10.")
    db.session.commit()
    if complete: log_activity(uid(), "interview", f"{s.category} interview: {s.avg_score}/10")
    return jsonify({**fb, "complete": complete, "report": _final(s) if complete else None})


@bp.get("/interview/history")
@jwt_required()
def history():
    rows = InterviewSession.query.filter_by(user_id=uid(), completed=True).order_by(InterviewSession.id).all()
    by = {}
    for r in rows: by.setdefault(r.category, []).append(r.avg_score)
    return jsonify({"sessions": [{"id": r.id, "category": r.category, "avg_score": r.avg_score, "date": r.created_at.isoformat()} for r in rows],
                    "by_category": {k: round(sum(v) / len(v), 1) for k, v in by.items()}})
