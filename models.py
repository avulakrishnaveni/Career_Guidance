from datetime import datetime, date
from extensions import db


def _ser(v):
    return v.isoformat() if isinstance(v, (datetime, date)) else v


class Base(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: _ser(getattr(self, c.name)) for c in self.__table__.columns}


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    otp_hash = db.Column(db.String(256))
    otp_purpose = db.Column(db.String(20))
    otp_expires = db.Column(db.DateTime)
    otp_attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Profile(Base):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    profile_type = db.Column(db.String(20), default="student")
    education_level = db.Column(db.String(40))
    institution = db.Column(db.String(150))
    edu_start_year = db.Column(db.String(4))
    edu_end_year = db.Column(db.String(10))
    degree = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    grade = db.Column(db.String(20))
    company = db.Column(db.String(150))
    designation = db.Column(db.String(100))
    work_start_year = db.Column(db.String(4))
    work_end_year = db.Column(db.String(10))
    total_experience = db.Column(db.String(20))
    is_current = db.Column(db.Boolean, default=False)
    skills = db.Column(db.JSON, default=list)
    bio = db.Column(db.Text)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    photo = db.Column(db.Text)  # small data-URL image

    FIELDS = ["profile_type", "education_level", "institution", "edu_start_year", "edu_end_year", "degree", "branch",
              "grade", "company", "designation", "work_start_year", "work_end_year", "total_experience", "is_current",
              "skills", "bio", "linkedin", "github", "photo"]


class CareerSelection(Base):
    __tablename__ = "career_selections"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    domain = db.Column(db.String(60))
    role = db.Column(db.String(100))
    experience_level = db.Column(db.String(30))
    goal = db.Column(db.String(60))


class Resume(Base):
    __tablename__ = "resumes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(200))
    score = db.Column(db.Integer)
    analysis = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Job(Base):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    company = db.Column(db.String(120))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(60))
    job_type = db.Column(db.String(30))
    experience_level = db.Column(db.String(20))
    domain = db.Column(db.String(60))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    skills = db.Column(db.JSON, default=list)
    apply_url = db.Column(db.String(300), default="#")


class JobApplication(Base):
    __tablename__ = "job_applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    saved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20))  # Applied | Interview | Offer | Rejected
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id", "job_id"),)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(10))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(30))
    question_ids = db.Column(db.JSON, default=list)
    answers = db.Column(db.JSON, default=list)
    avg_score = db.Column(db.Float, default=0)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CodingChallenge(Base):
    __tablename__ = "coding_challenges"
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(60))
    title = db.Column(db.String(120))
    difficulty = db.Column(db.String(10))
    points = db.Column(db.Integer, default=10)
    description = db.Column(db.Text)
    starter_code = db.Column(db.Text)
    tests = db.Column(db.JSON)
    hints = db.Column(db.JSON, default=list)
    solution = db.Column(db.Text)


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("coding_challenges.id"), nullable=False)
    passed = db.Column(db.Boolean, default=False)
    passed_count = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LearningModule(Base):
    __tablename__ = "learning_modules"
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(60), index=True)
    position = db.Column(db.Integer)
    title = db.Column(db.String(150))
    hours = db.Column(db.Integer)
    lessons = db.Column(db.JSON, default=list)
    resource = db.Column(db.String(200))


class Progress(Base):
    __tablename__ = "progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("learning_modules.id"), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint("user_id", "module_id"),)


class ForumPost(Base):
    __tablename__ = "forum_posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    domain = db.Column(db.String(60))
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    upvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ForumComment(Base):
    __tablename__ = "forum_comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("forum_posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ForumVote(Base):
    __tablename__ = "forum_votes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("forum_posts.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint("user_id", "post_id"),)


class Notification(Base):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150))
    message = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReadinessReport(Base):
    __tablename__ = "readiness_reports"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer)
    level = db.Column(db.String(20))
    data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id", "day"),)


class Activity(Base):
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    kind = db.Column(db.String(30))
    detail = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
