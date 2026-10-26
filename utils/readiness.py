"""Job Readiness engine: aggregates every module into one score, report sections and an action plan."""
import math
from datetime import datetime
from extensions import db
from models import (User, Profile, CareerSelection, Resume, Job, JobApplication, InterviewSession, CodingChallenge,
                    CodingSubmission, LearningModule, Progress, ReadinessReport)
from data import DOMAINS
from utils.helpers import completeness, skill_overlap, job_match, years_of_experience, streak

WEIGHTS = {"profile": 15, "resume": 20, "interview": 20, "coding": 15, "learning": 15, "skills": 15}
LABELS = {"profile": "Profile", "resume": "Resume", "interview": "Interview", "coding": "Coding", "learning": "Learning", "skills": "Skill match"}
LEVELS = [(40, "Beginner", "#ef4444"), (60, "Developing", "#f59e0b"), (80, "Job-Ready", "#10b981"), (100, "Interview-Ready", "#4f46e5")]
DIFF = {"easy": 0, "medium": 1, "hard": 2}


def level_for(score):
    for top, name, color in LEVELS:
        if score <= top: return name, color
    return LEVELS[-1][1], LEVELS[-1][2]


def collect(uid):
    p = Profile.query.filter_by(user_id=uid).first()
    cs = CareerSelection.query.filter_by(user_id=uid).first()
    domain = cs.domain if cs else None
    skills = (p.skills if p else []) or []
    prof_pct, missing_fields = completeness(p)

    # Resume
    resumes = Resume.query.filter_by(user_id=uid).order_by(Resume.id).all()
    last = resumes[-1] if resumes else None
    an = (last.analysis or {}) if last else {}
    resume = {"uploaded": bool(last), "score": last.score if last else 0, "ats_pct": an.get("ats", {}).get("pct", 0),
              "ats_rating": an.get("ats", {}).get("rating", "Not analyzed"), "missing_keywords": an.get("ats", {}).get("missing", []),
              "improvements": an.get("improvements", [])[:5], "missing_sections": an.get("missing_sections", [])}

    # Interview
    sessions = InterviewSession.query.filter_by(user_id=uid, completed=True).all()
    by_cat = {}
    for s in sessions: by_cat.setdefault(s.category, []).append(s.avg_score)
    cat_avg = {k: round(sum(v) / len(v), 1) for k, v in by_cat.items()}
    avg = round(sum(s.avg_score for s in sessions) / len(sessions), 1) if sessions else 0
    interview = {"sessions": len(sessions), "avg": avg, "by_category": cat_avg, "weakest": min(cat_avg, key=cat_avg.get) if cat_avg else None}

    # Coding
    subs = CodingSubmission.query.filter_by(user_id=uid).all()
    solved = {s.challenge_id for s in subs if s.passed}
    pool = CodingChallenge.query.filter(CodingChallenge.domain.in_(["all", domain or "all"])).all()
    success = round(sum(1 for s in subs if s.passed) / len(subs) * 100) if subs else 0
    rec = sorted([c for c in pool if c.id not in solved], key=lambda c: DIFF[c.difficulty])[:3]
    coding = {"solved": len(solved), "available": len(pool), "attempts": len(subs), "success_rate": success,
              "recommended": [{"id": c.id, "title": c.title, "difficulty": c.difficulty} for c in rec]}

    # Learning
    mods = LearningModule.query.filter_by(domain=domain).order_by(LearningModule.position).all() if domain else []
    done_ids = {r.module_id for r in Progress.query.filter_by(user_id=uid, completed=True).all()}
    done = [m for m in mods if m.id in done_ids]
    pending = [m for m in mods if m.id not in done_ids]
    learn_pct = round(len(done) / len(mods) * 100) if mods else 0
    hours_left = sum(m.hours for m in pending)
    learning = {"percent": learn_pct, "done": len(done), "pending": len(pending), "total": len(mods), "hours_left": hours_left,
                "weeks_left": math.ceil(hours_left / 8) if hours_left else 0, "pending_modules": [m.title for m in pending][:5]}

    # Skills
    required = DOMAINS.get(domain, {}).get("skills", []) if domain else []
    matched, gap = skill_overlap(required, skills)
    skill_pct = round(len(matched) / len(required) * 100) if required else 0
    skills_info = {"required": required, "matched": matched, "gap": gap, "pct": skill_pct}

    # Jobs
    years = years_of_experience(p)
    ranked = sorted(((job_match(j, skills, domain, years), j) for j in Job.query.all()), key=lambda x: -x[0])[:5]
    apps = JobApplication.query.filter_by(user_id=uid).all()
    jobs = {"top": [{"id": j.id, "title": j.title, "company": j.company, "match": m, "skills_gap": skill_overlap(j.skills or [], skills)[1]} for m, j in ranked],
            "saved": sum(1 for a in apps if a.saved), "applied": sum(1 for a in apps if a.status == "Applied"),
            "interviews": sum(1 for a in apps if a.status == "Interview"), "offers": sum(1 for a in apps if a.status == "Offer"),
            "rejected": sum(1 for a in apps if a.status == "Rejected")}

    coding_score = round((min(1, len(solved) / 5) * 0.5 + success / 100 * 0.5) * 100)
    comps = {"profile": prof_pct, "resume": resume["score"], "interview": round(avg * 10), "coding": coding_score, "learning": learn_pct, "skills": skill_pct}
    score = round(sum(comps[k] * WEIGHTS[k] for k in WEIGHTS) / sum(WEIGHTS.values()))
    level, color = level_for(score)

    badges = []
    if prof_pct >= 80: badges.append("Profile Pro")
    if resume["score"] >= 70: badges.append("Resume Ace")
    if len(solved) >= 1: badges.append("Code Starter")
    if len(solved) >= 10: badges.append("Problem Solver")
    if len(sessions) >= 1 and avg >= 7: badges.append("Interview Star")
    if len(done) >= 1: badges.append("Learner")
    if learning["total"] and learn_pct == 100: badges.append("Roadmap Finisher")
    if streak(uid) >= 3: badges.append("On Fire (3-day streak)")

    # Action plan: biggest weighted gaps first
    cands = [
        ("profile", "Complete your profile", f"Missing: {', '.join(missing_fields[:4]) or 'nothing'}", "/profile"),
        ("resume", "Upload and improve your resume", (resume["improvements"][0] if resume["improvements"] else "Upload your resume to get a score and ATS keywords"), "/resume"),
        ("interview", "Practise mock interviews", f"Weakest area: {interview['weakest']}" if interview["weakest"] else "Complete a full mock interview", "/interview"),
        ("coding", "Solve coding challenges", f"Try: {coding['recommended'][0]['title']}" if coding["recommended"] else "Solve at least 5 problems", "/coding"),
        ("learning", "Continue your learning roadmap", f"Next: {learning['pending_modules'][0]}" if learning["pending_modules"] else "Choose a career path to unlock your roadmap", "/learning"),
        ("skills", "Close your skill gaps", f"Learn: {', '.join(gap[:4])}" if gap else "Choose a career path to see required skills", "/career"),
    ]
    actions = sorted(((WEIGHTS[k] * (100 - comps[k]), k, t, d, l) for k, t, d, l in cands), reverse=True)
    actions = [{"title": t, "detail": d, "link": l, "component": k, "priority": i + 1} for i, (g, k, t, d, l) in enumerate(actions) if g > 0][:5]

    weekly = ["Complete 2 learning modules", "Solve 3 coding challenges", "Take 1 mock interview",
              "Raise resume score above 80" if resume["score"] < 80 else "Apply to 3 matched jobs"]
    resources = [f"{m.title}: {m.resource}" for m in pending[:3]] or ["Pick a career path to get recommended resources"]
    resources += [f"Skill to learn: {g}" for g in gap[:2]]
    gap_pts = lambda t: max(0, t - score)
    timeline = {"to_job_ready_weeks": math.ceil(gap_pts(61) / 4), "to_interview_ready_weeks": math.ceil(gap_pts(81) / 4), "learning_weeks": learning["weeks_left"]}

    return {"score": score, "level": level, "color": color, "domain": domain,
            "components": [{"key": k, "label": LABELS[k], "score": comps[k], "weight": WEIGHTS[k]} for k in WEIGHTS],
            "profile": {"completeness": prof_pct, "missing": missing_fields, "education": (p.education_level if p and p.profile_type == "student" else (p.designation if p else None)),
                        "skills_count": len(skills)},
            "resume": resume, "interview": interview, "technical": coding, "learning": learning, "skills": skills_info, "jobs": jobs,
            "action_plan": {"actions": actions, "weekly_goals": weekly, "resources": resources, "timeline": timeline},
            "badges": badges, "streak": streak(uid), "generated_at": datetime.utcnow().isoformat() + "Z"}


def snapshot(uid):
    d = collect(uid)
    today = datetime.utcnow().date()
    row = ReadinessReport.query.filter_by(user_id=uid, day=today).first() or ReadinessReport(user_id=uid, day=today)
    row.score, row.level, row.data = d["score"], d["level"], {"components": d["components"]}
    db.session.add(row); db.session.commit()
    return d


def history(uid, n=30):
    rows = ReadinessReport.query.filter_by(user_id=uid).order_by(ReadinessReport.day.desc()).limit(n).all()
    return [{"day": r.day.isoformat(), "score": r.score, "level": r.level} for r in reversed(rows)]
