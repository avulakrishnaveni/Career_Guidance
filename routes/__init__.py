from . import auth, profile, career, chat, resume, jobs, interview, coding, report, dashboard, community


def register_blueprints(app):
    for m in (auth, profile, career, chat, resume, jobs, interview, coding, report, dashboard, community):
        app.register_blueprint(m.bp, url_prefix="/api")
