import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()
from extensions import db, jwt
from routes import register_blueprints
from seed import seed

BASE = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL") or "sqlite:///" + os.path.join(BASE, "careerverse.db"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me-please-32chars"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
        MAIL_SERVER=os.getenv("MAIL_SERVER") or None, MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"), MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "true").lower() == "true", MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
    )
    CORS(app, origins=os.getenv("CORS_ORIGIN", "http://localhost:5173").split(","))
    db.init_app(app); jwt.init_app(app)

    @jwt.unauthorized_loader
    def _u(r): return jsonify({"error": "Please log in to continue"}), 401
    @jwt.expired_token_loader
    def _e(h, p): return jsonify({"error": "Session expired. Please log in again"}), 401
    @jwt.invalid_token_loader
    def _i(r): return jsonify({"error": "Invalid session. Please log in again"}), 401

    @app.errorhandler(413)
    def _big(e): return jsonify({"error": "File is too large (max 5 MB)"}), 413
    @app.errorhandler(404)
    def _nf(e): return jsonify({"error": "Not found"}), 404
    @app.errorhandler(500)
    def _ise(e): return jsonify({"error": "Server error. Please try again"}), 500

    @app.get("/api/health")
    def health(): return jsonify({"status": "ok"})

    register_blueprints(app)
    with app.app_context():
        db.create_all()
        seed()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
