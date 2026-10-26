import os, uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from extensions import db
from models import Resume, CareerSelection
from utils.helpers import err, uid, log_activity, notify
from utils.resume_analyzer import extract_text, analyze

bp = Blueprint("resume", __name__)
UPLOADS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
ALLOWED = {"pdf", "doc", "docx"}


@bp.post("/resume/upload")
@jwt_required()
def upload():
    f = request.files.get("resume")
    if not f or not f.filename: return err("Choose a resume file")
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED: return err("Only PDF, DOC and DOCX files are allowed")
    os.makedirs(UPLOADS, exist_ok=True)
    path = os.path.join(UPLOADS, f"{uuid.uuid4().hex}_{secure_filename(f.filename)}")
    f.save(path)
    try:
        text = extract_text(path, ext)
    except Exception:
        return err("Could not read this file. Try a text-based PDF or a DOCX")
    finally:
        if os.path.exists(path): os.remove(path)  # only the analysis is kept, not the file
    if len(text.strip()) < 50: return err("No readable text found. Scanned images are not supported")
    cs = CareerSelection.query.filter_by(user_id=uid()).first()
    result = analyze(text, cs.domain if cs else None)
    row = Resume(user_id=uid(), filename=f.filename[:200], score=result["score"], analysis=result)
    db.session.add(row)
    notify(uid(), "Resume analyzed", f"{f.filename} scored {result['score']}/100.")
    db.session.commit()
    log_activity(uid(), "resume", f"Resume scored {result['score']}")
    return jsonify({**result, "id": row.id, "filename": row.filename})


@bp.get("/resume/history")
@jwt_required()
def history():
    rows = Resume.query.filter_by(user_id=uid()).order_by(Resume.id).all()
    return jsonify([{"id": r.id, "filename": r.filename, "score": r.score, "created_at": r.created_at.isoformat(), "analysis": r.analysis} for r in rows])
