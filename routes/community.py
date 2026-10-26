from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import ForumPost, ForumComment, ForumVote, Notification, User
from data import DOMAINS, MENTORS, EVENTS
from utils.helpers import err, uid, notify, log_activity

bp = Blueprint("community", __name__)
name_of = lambda i: (db.session.get(User, i).name if db.session.get(User, i) else "User")


# ---- Forum ----
@bp.get("/forum/posts")
@jwt_required()
def posts():
    q = ForumPost.query
    if request.args.get("domain"): q = q.filter_by(domain=request.args["domain"])
    voted = {v.post_id for v in ForumVote.query.filter_by(user_id=uid())}
    return jsonify({"domains": list(DOMAINS), "posts": [
        {**p.to_dict(), "author": name_of(p.user_id), "comments": ForumComment.query.filter_by(post_id=p.id).count(), "voted": p.id in voted}
        for p in q.order_by(ForumPost.upvotes.desc(), ForumPost.id.desc()).limit(50)]})


@bp.post("/forum/posts")
@jwt_required()
def create_post():
    d = request.get_json(silent=True) or {}
    title, body = (d.get("title") or "").strip(), (d.get("body") or "").strip()
    if d.get("domain") not in DOMAINS: return err("Choose a domain")
    if len(title) < 5 or len(title) > 200: return err("Title must be 5-200 characters")
    if len(body) < 10 or len(body) > 3000: return err("Post must be 10-3000 characters")
    p = ForumPost(user_id=uid(), domain=d["domain"], title=title, body=body)
    db.session.add(p); db.session.commit()
    log_activity(uid(), "forum", f"Posted: {title}")
    return jsonify({"message": "Posted", "id": p.id}), 201


@bp.post("/forum/posts/<int:pid>/upvote")
@jwt_required()
def upvote(pid):
    p = db.session.get(ForumPost, pid)
    if not p: return err("Post not found", 404)
    v = ForumVote.query.filter_by(user_id=uid(), post_id=pid).first()
    if v: db.session.delete(v); p.upvotes = max(0, p.upvotes - 1)
    else: db.session.add(ForumVote(user_id=uid(), post_id=pid)); p.upvotes += 1
    db.session.commit()
    return jsonify({"upvotes": p.upvotes, "voted": not v})


@bp.get("/forum/comments")
@jwt_required()
def comments():
    rows = ForumComment.query.filter_by(post_id=request.args.get("post_id", type=int)).order_by(ForumComment.id).all()
    return jsonify([{**c.to_dict(), "author": name_of(c.user_id)} for c in rows])


@bp.post("/forum/comments")
@jwt_required()
def add_comment():
    d = request.get_json(silent=True) or {}
    p, body = db.session.get(ForumPost, d.get("post_id")), (d.get("body") or "").strip()
    if not p: return err("Post not found", 404)
    if not 2 <= len(body) <= 1000: return err("Comment must be 2-1000 characters")
    db.session.add(ForumComment(post_id=p.id, user_id=uid(), body=body))
    if p.user_id != uid(): notify(p.user_id, "New comment on your post", f"{name_of(uid())} commented on \"{p.title[:60]}\".")
    db.session.commit()
    return jsonify({"message": "Comment added"}), 201


# ---- Mentors & events ----
@bp.get("/mentors")
@jwt_required()
def mentors():
    dom = request.args.get("domain")
    return jsonify([m for m in MENTORS if not dom or m["domain"] == dom])


@bp.post("/mentors/connect")
@jwt_required()
def connect():
    m = next((x for x in MENTORS if x["id"] == (request.get_json(silent=True) or {}).get("mentor_id")), None)
    if not m: return err("Mentor not found", 404)
    notify(uid(), "Mentor request sent", f"Your request to {m['name']} was sent. They usually reply within 3 days.")
    db.session.commit()
    return jsonify({"message": f"Request sent to {m['name']}"})


@bp.get("/events")
@jwt_required()
def events():
    return jsonify(EVENTS)


@bp.post("/events/register")
@jwt_required()
def register_event():
    e = next((x for x in EVENTS if x["id"] == (request.get_json(silent=True) or {}).get("event_id")), None)
    if not e: return err("Event not found", 404)
    notify(uid(), "Event registration confirmed", f"You are registered for {e['title']} ({e['date']}).")
    db.session.commit()
    return jsonify({"message": f"Registered for {e['title']}"})


# ---- Notifications ----
@bp.get("/notifications")
@jwt_required()
def notifications():
    rows = Notification.query.filter_by(user_id=uid()).order_by(Notification.id.desc()).limit(50).all()
    return jsonify({"items": [r.to_dict() for r in rows], "unread": sum(1 for r in rows if not r.read)})


@bp.post("/notifications/read")
@jwt_required()
def mark_read():
    nid = (request.get_json(silent=True) or {}).get("id")
    q = Notification.query.filter_by(user_id=uid())
    if nid: q = q.filter_by(id=nid)
    q.update({"read": True}); db.session.commit()
    return jsonify({"message": "Updated"})
