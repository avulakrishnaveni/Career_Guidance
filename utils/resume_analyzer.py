import re
from data import DOMAINS

try:
    from PyPDF2 import PdfReader
except ImportError:  # newer environments
    from pypdf import PdfReader
from docx import Document

SKILLS = ["python", "java", "javascript", "typescript", "react", "node", "flask", "django", "sql", "mongodb", "html", "css", "git",
          "docker", "kubernetes", "aws", "azure", "gcp", "linux", "machine learning", "deep learning", "tensorflow", "pytorch", "pandas",
          "numpy", "excel", "power bi", "tableau", "c++", "kotlin", "swift", "flutter", "rest", "api", "nlp", "figma", "terraform", "jenkins",
          "ci/cd", "networking", "firebase", "agile", "statistics"]
VERBS = ["developed", "built", "designed", "led", "implemented", "created", "improved", "optimized", "managed", "delivered", "launched", "reduced"]
HEADINGS = {
    "summary": r"summary|objective|profile|about me",
    "education": r"education|academic",
    "experience": r"experience|employment|work history|internship",
    "projects": r"projects?",
    "skills": r"(technical )?skills|technologies|tech stack",
    "certifications": r"certifications?|courses|achievements|awards",
}
WEIGHTS = {"contact": 10, "summary": 10, "education": 15, "experience": 20, "projects": 20, "skills": 15, "certifications": 10}


def extract_text(path, ext):
    if ext == "pdf":
        return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    if ext == "docx":
        return "\n".join(p.text for p in Document(path).paragraphs)
    with open(path, "rb") as f:  # legacy .doc: best-effort
        return re.sub(r"[^\x20-\x7E\n]", " ", f.read().decode("latin-1"))


def _split_sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        s = line.strip().strip(":").strip()
        if 0 < len(s) <= 40:
            for name, pat in HEADINGS.items():
                if re.fullmatch(rf"(?i)({pat})", s):
                    cur = name; out.setdefault(cur, []); break
            else:
                if cur: out[cur].append(line)
        elif cur:
            out[cur].append(line)
    return {k: " ".join(v) for k, v in out.items()}


def analyze(text, domain=None):
    low = text.lower()
    words = len(text.split())
    secs = _split_sections(text)
    found_skills = sorted({s for s in SKILLS if re.search(r"(?<![a-z])" + re.escape(s) + r"(?![a-z])", low)})
    verbs = sum(low.count(v) for v in VERBS)
    has_metric = bool(re.search(r"\d+\s*%|\$\s*\d+|₹\s*\d+|\b\d{2,}\+?\s*(users|customers|projects|clients)", low))

    scores = {}
    c = (40 if "@" in text else 0) + (30 if re.search(r"\b\d{10}\b|\+\d{2}[\s\d-]{8,}", text) else 0) + (30 if re.search(r"linkedin|github", low) else 0)
    scores["contact"] = c
    for name in HEADINGS:
        body = secs.get(name, "")
        n = len(body.split())
        present = name in secs or (name == "skills" and len(found_skills) >= 4)
        base = 0 if not present else 50 + min(40, n * 1.5)
        if name in ("experience", "projects") and present: base += min(10, verbs * 2) if has_metric or verbs else 0
        scores[name] = min(100, round(base))

    domain_skills = DOMAINS.get(domain, {}).get("skills", []) if domain else []
    pool = domain_skills or ["Python", "SQL", "Git", "REST", "Agile"]
    matched = [k for k in pool if k.lower() in low]
    missing_kw = [k for k in pool if k.lower() not in low]
    ats_pct = round(len(matched) / len(pool) * 100)

    section_avg = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS) / sum(WEIGHTS.values())
    fmt = 100 if 200 <= words <= 900 else 60 if 100 <= words <= 1200 else 30
    overall = round(section_avg * 0.6 + ats_pct * 0.25 + fmt * 0.15)

    missing_sections = [k.capitalize() for k in WEIGHTS if scores[k] == 0]
    strengths, improve = [], []
    for k, v in scores.items():
        if v >= 75: strengths.append(f"Strong {k} section")
    if len(found_skills) >= 6: strengths.append(f"Broad skill coverage ({len(found_skills)} detected)")
    if has_metric: strengths.append("Quantified achievements")
    if ats_pct >= 60: strengths.append(f"Good ATS keyword match ({ats_pct}%)")
    for s in missing_sections: improve.append(f"Add a {s} section")
    if not has_metric: improve.append("Add measurable results (e.g. 'reduced load time by 30%')")
    if verbs < 3: improve.append("Start bullets with strong action verbs (built, led, optimized)")
    if fmt < 100: improve.append("Aim for 200-900 words (one page for freshers)")
    if scores["contact"] < 100: improve.append("Complete your contact block: email, phone, LinkedIn/GitHub")
    if ats_pct < 60: improve.append(f"Work these keywords in naturally: {', '.join(missing_kw[:5])}")

    recs = ["Tailor the resume to each job description's keywords.", "Link 2-3 projects with GitHub or live demos.",
            "Keep formatting simple (no tables or images) so ATS parsers read it correctly."]
    return {"score": overall, "sections": [{"name": k.capitalize(), "score": scores[k], "present": scores[k] > 0} for k in WEIGHTS],
            "missing_sections": missing_sections, "ats": {"pct": ats_pct, "rating": "Strong" if ats_pct >= 70 else "Fair" if ats_pct >= 40 else "Weak",
                                                        "matched": matched, "missing": missing_kw[:10]},
            "skills": found_skills, "strengths": strengths, "improvements": improve, "recommendations": recs, "word_count": words, "domain": domain}
