import re

FILLERS = re.compile(r"\b(um+|uh+|like|you know|basically|actually)\b", re.I)
STAR = {
    "Situation": r"\b(situation|when|during|once|at my|in my|last year|project|team)\b",
    "Task": r"\b(task|goal|responsible|needed to|had to|objective|assigned)\b",
    "Action": r"\b(i (did|led|built|decided|created|wrote|organized|talked|asked|started|implemented|worked)|implemented|created|organized)\b",
    "Result": r"\b(result|outcome|achieved|improved|reduced|increased|learned|delivered|successfully)\b",
}


def evaluate(q, answer):
    text = answer.strip()
    low = text.lower()
    words = len(text.split())
    hits = [k for k in q["keywords"] if k in low]
    score = min(4, words / 20)                     # depth (up to 4)
    score += min(3, len(hits) * 0.75)              # relevance (up to 3)
    strengths, tips, star = [], [], None
    fill = len(FILLERS.findall(text))

    if q["category"] in ("Behavioral", "Situational"):
        star = {k: bool(re.search(p, low)) for k, p in STAR.items()}
        score += sum(star.values()) * 0.75         # structure (up to 3)
        missing = [k for k, v in star.items() if not v]
        if not missing: strengths.append("Clear STAR structure (Situation, Task, Action, Result)")
        else: tips.append("Cover all STAR parts. Missing: " + ", ".join(missing))
    else:
        score += 3 if re.search(r"\b(because|for example|for instance|so that|therefore)\b", low) else 1
        if not re.search(r"\b(because|for example|for instance)\b", low): tips.append("Support your point with a reason or example")

    if words >= 50: strengths.append("Detailed answer with enough depth")
    else: tips.append("Aim for 50-120 words so you can show depth")
    if hits: strengths.append("Relevant points mentioned: " + ", ".join(hits[:4]))
    else: tips.append("Include role-relevant keywords and specifics")
    if re.search(r"\d", text): score += 0.5; strengths.append("Used concrete numbers or metrics")
    elif q["category"] != "HR": tips.append("Add a measurable detail (time saved, users, accuracy)")
    if fill > 3: score -= 1; tips.append(f"Reduce filler words ({fill} found)")
    if words > 200: tips.append("Tighten the answer: keep it under about two minutes")
    return {"score": max(0, min(10, round(score))), "out_of": 10, "strengths": strengths, "improvements": tips, "star": star, "word_count": words}
