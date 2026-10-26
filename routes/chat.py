from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import ChatMessage, CareerSelection
from utils.helpers import err, uid
from utils.chatbot import reply

bp = Blueprint("chat", __name__)


@bp.post("/chat")
@jwt_required()
def chat():
    text = ((request.get_json(silent=True) or {}).get("message") or "").strip()
    if not text: return err("Type a message first")
    if len(text) > 500: return err("Keep messages under 500 characters")
    cs = CareerSelection.query.filter_by(user_id=uid()).first()
    answer = reply(text, cs.domain if cs else None)
    db.session.add_all([ChatMessage(user_id=uid(), role="user", text=text), ChatMessage(user_id=uid(), role="bot", text=answer)])
    db.session.commit()
    return jsonify({"reply": answer})


@bp.get("/chat/history")
@jwt_required()
def history():
    rows = ChatMessage.query.filter_by(user_id=uid()).order_by(ChatMessage.id.desc()).limit(100).all()
    return jsonify([r.to_dict() for r in reversed(rows)])


@bp.delete("/chat/history")
@jwt_required()
def clear():
    ChatMessage.query.filter_by(user_id=uid()).delete(); db.session.commit()
    return jsonify({"message": "Chat history cleared"})
