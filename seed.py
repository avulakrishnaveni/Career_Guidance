from extensions import db
from models import Job, CodingChallenge, LearningModule
from data import DOMAINS, JOBS, CHALLENGES


def seed():
    if Job.query.count() == 0:
        for t, c, l, sal, typ, lvl, dom, desc, sk in JOBS:
            db.session.add(Job(title=t, company=c, location=l, salary=sal, job_type=typ, experience_level=lvl, domain=dom,
                               description=desc, skills=sk, requirements="Skills: " + ", ".join(sk), apply_url="https://example.com/apply"))
    if CodingChallenge.query.count() == 0:
        for ch in CHALLENGES:
            db.session.add(CodingChallenge(**ch))
    if LearningModule.query.count() == 0:
        for dom, d in DOMAINS.items():
            for i, m in enumerate(d["modules"], 1):
                db.session.add(LearningModule(domain=dom, position=i, title=m["title"], hours=m["hours"], lessons=m["lessons"], resource=m["resource"]))
    db.session.commit()
