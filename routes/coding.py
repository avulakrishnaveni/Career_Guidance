from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import CodingChallenge, CodingSubmission, CareerSelection, User
from utils.helpers import err, uid, log_activity, notify, streak
from utils.sandbox import run_tests

bp = Blueprint("coding", __name__)


@bp.get("/coding/challenges")
@jwt_required()
def challenges():
    cs = CareerSelection.query.filter_by(user_id=uid()).first()
    scope = request.args.get("scope", "domain")
    domain = request.args.get("domain") or (cs.domain if cs else None)
    q = CodingChallenge.query
    if scope != "all" and domain: q = q.filter(CodingChallenge.domain.in_(["all", domain]))
    solved = {s.challenge_id for s in CodingSubmission.query.filter_by(user_id=uid(), passed=True)}
    return jsonify({"domain": domain, "challenges": [
        {"id": c.id, "domain": c.domain, "title": c.title, "difficulty": c.difficulty, "points": c.points, "description": c.description,
         "starter_code": c.starter_code, "examples": c.tests[:2], "hint_count": len(c.hints or []), "solved": c.id in solved} for c in q.order_by(CodingChallenge.id)]})


@bp.get("/coding/challenges/<int:cid>/hint")
@jwt_required()
def hint(cid):
    c = db.session.get(CodingChallenge, cid)
    n = request.args.get("n", 1, type=int)
    if not c: return err("Challenge not found", 404)
    if n < 1 or n > len(c.hints or []): return err("No more hints")
    return jsonify({"hint": c.hints[n - 1], "n": n, "total": len(c.hints)})


@bp.get("/coding/challenges/<int:cid>/solution")
@jwt_required()
def solution(cid):
    c = db.session.get(CodingChallenge, cid)
    if not c: return err("Challenge not found", 404)
    return jsonify({"solution": c.solution})


@bp.post("/coding/submit")
@jwt_required()
def submit():
    d = request.get_json(silent=True) or {}
    c = db.session.get(CodingChallenge, d.get("challenge_id"))
    code = d.get("code") or ""
    if not c: return err("Challenge not found", 404)
    if not code.strip() or len(code) > 10000: return err("Write your solution first (max 10,000 characters)")
    out = run_tests(code, c.tests)
    res = out["results"]
    passed = bool(res) and all(x["ok"] for x in res)
    first_time = passed and not CodingSubmission.query.filter_by(user_id=uid(), challenge_id=c.id, passed=True).first()
    db.session.add(CodingSubmission(user_id=uid(), challenge_id=c.id, passed=passed, passed_count=sum(x["ok"] for x in res), total=len(c.tests)))
    if first_time: notify(uid(), "Challenge solved", f"You solved {c.title} and earned {c.points} points.")
    db.session.commit()
    log_activity(uid(), "coding", f"{'Solved' if passed else 'Attempted'}: {c.title}")
    for i, x in enumerate(res):  # reveal expected output only for the example tests
        x["input"], x["hidden"] = c.tests[i]["input"], i >= 2
        if i < 2: x["expected"] = c.tests[i]["expected"]
        else: x["input"] = None
    return jsonify({"passed": passed, "error": out["error"], "results": res, "total": len(c.tests), "passed_count": sum(x["ok"] for x in res),
                    "points_earned": c.points if first_time else 0})


@bp.get("/coding/leaderboard")
@jwt_required()
def leaderboard():
    pts = {c.id: c.points for c in CodingChallenge.query.all()}
    per = {}
    for u, cid in db.session.query(CodingSubmission.user_id, CodingSubmission.challenge_id).filter(CodingSubmission.passed.is_(True)).distinct():
        per.setdefault(u, []).append(cid)
    rows = sorted(((sum(pts[c] for c in cids), len(cids), u) for u, cids in per.items()), reverse=True)
    names = {u.id: u.name for u in User.query.filter(User.id.in_([r[2] for r in rows])).all()}
    board = [{"rank": i + 1, "name": names.get(u, "User"), "points": p, "solved": n, "me": u == uid()} for i, (p, n, u) in enumerate(rows[:10])]
    mine = next(((i + 1, p, n) for i, (p, n, u) in enumerate(rows) if u == uid()), None)
    return jsonify({"leaderboard": board, "me": {"rank": mine[0], "points": mine[1], "solved": mine[2]} if mine else None, "streak": streak(uid(), "coding")})
