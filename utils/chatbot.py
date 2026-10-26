RULES = [
    (["resume", "cv", "ats"], "Resume tips: keep it to one page, lead with impact (action verb + metric), mirror keywords from the job description, and add 2-3 projects with links. Upload it in Resume Analyzer to get a score."),
    (["interview", "mock", "hr round"], "Interview prep: use the STAR method (Situation, Task, Action, Result), research the company, and rehearse a 60-second intro. Try the Mock Interview with voice."),
    (["job", "apply", "opening", "hiring", "placement"], "Job search: tailor your resume per role, use LinkedIn and company career pages, and track applications. Open Jobs to see openings ranked by your match percentage."),
    (["code", "coding", "dsa", "algorithm", "leetcode", "problem"], "Coding practice: start with arrays and strings, then hash maps, stacks and recursion. Solve one problem daily to build a streak in the Coding Arena."),
    (["readiness", "ready", "score report"], "Your Job Readiness Report combines profile, resume, interviews, coding, learning and skill match into one score with an action plan. Open Readiness Report from the menu."),
    (["career", "path", "roadmap", "domain", "confused"], "Pick the domain that fits your interests: AI & ML, Web, Data Science, Cybersecurity, Cloud, Mobile, DevOps or UI/UX. Choose it under Career Path to get a roadmap with timeline."),
    (["python"], "Python is a great first language for AI, data and web backends. Learn basics, lists/dicts, functions, OOP, then Flask or Pandas."),
    (["react", "javascript", "web", "frontend"], "For web: HTML/CSS, JavaScript, React, a backend (Flask or Node), a database, then deploy. Build 3 projects and put them on GitHub."),
    (["cloud", "aws", "azure"], "For cloud: learn Linux and networking, then AWS or Azure fundamentals, Docker, and Terraform. A cloud practitioner certification helps freshers."),
    (["security", "cyber", "hacking"], "For cybersecurity: networking and Linux first, then OWASP Top 10, Nmap/Burp Suite labs, and a SOC analyst path. TryHackMe is a good start."),
    (["salary", "pay", "ctc"], "Salary depends on skills, location and company. Compare several sources, build a strong portfolio, and negotiate using market data."),
    (["skill", "learn", "study"], "Focus on one roadmap at a time. Check Learning Path for modules and mark them done to build your streak."),
    (["thank"], "You're welcome! Ask anytime."),
    (["hello", "hi", "hey"], "Hi! I'm CareerMate. I can help with careers, resumes, jobs, interviews and coding. What would you like to know?"),
    (["help"], "I can answer questions on career guidance, resume tips, job search, interview preparation and coding practice."),
]


def reply(text, domain=None):
    """Keyword-based replies. To upgrade, replace this body with an LLM API call and pass `domain` as context."""
    t = " " + text.lower() + " "
    for keys, answer in RULES:
        if any((" " + k + " ") in t or (len(k) > 3 and k in t) for k in keys):
            extra = f" Your selected domain is {domain}." if domain and keys[0] in ("career", "skill") else ""
            return answer + extra
    return "I'm not sure about that yet. Try asking about careers, resumes, jobs, interviews, coding practice or your readiness report."
