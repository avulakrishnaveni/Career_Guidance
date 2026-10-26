from io import BytesIO
from datetime import datetime
from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import jwt_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String
from extensions import db
from models import User
from utils.helpers import uid
from utils.readiness import snapshot, history

bp = Blueprint("report", __name__)
INDIGO, VIOLET = colors.HexColor("#4F46E5"), colors.HexColor("#7C3AED")


@bp.get("/report/readiness")
@jwt_required()
def readiness():
    d = snapshot(uid())
    return jsonify({**d, "history": history(uid())})


def _bars(components):
    h = 22 * len(components)
    dr = Drawing(480, h)
    for i, c in enumerate(components):
        y = h - 22 * (i + 1) + 4
        dr.add(String(0, y + 3, f"{c['label']}", fontSize=9, fillColor=colors.HexColor("#374151")))
        dr.add(Rect(90, y, 300, 12, fillColor=colors.HexColor("#E5E7EB"), strokeColor=None))
        dr.add(Rect(90, y, 3 * max(c["score"], 0), 12, fillColor=INDIGO, strokeColor=None))
        dr.add(String(398, y + 3, f"{c['score']}/100 (weight {c['weight']}%)", fontSize=8, fillColor=colors.HexColor("#374151")))
    return dr


@bp.get("/report/readiness/pdf")
@jwt_required()
def readiness_pdf():
    d = snapshot(uid())
    user = db.session.get(User, uid())
    ss = getSampleStyleSheet()
    H1 = ParagraphStyle("h1", parent=ss["Title"], textColor=INDIGO, fontSize=22, spaceAfter=4)
    H2 = ParagraphStyle("h2", parent=ss["Heading2"], textColor=VIOLET, spaceBefore=12, spaceAfter=4)
    B = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9.5, leading=13)
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    bullets = lambda items: [Paragraph("• " + esc(i), B) for i in items] or [Paragraph("None", B)]

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm, title="Job Readiness Report")
    s = [Paragraph("CareerVerse: Job Readiness Report", H1),
         Paragraph(f"{esc(user.name)} &nbsp;|&nbsp; Target domain: {esc(d['domain'] or 'Not selected')} &nbsp;|&nbsp; {datetime.utcnow():%d %b %Y}", B), Spacer(1, 8)]
    badge = Table([[f"{d['score']}/100", d["level"]]], colWidths=[4 * cm, 8 * cm], rowHeights=[1.4 * cm])
    badge.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(d["color"])), ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                               ("FONTSIZE", (0, 0), (-1, -1), 18), ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    s += [badge, Paragraph("Score breakdown", H2), _bars(d["components"])]

    p, r, i, t, l, k = d["profile"], d["resume"], d["interview"], d["technical"], d["learning"], d["skills"]
    s += [Paragraph("Profile strength", H2), Paragraph(f"Completeness: {p['completeness']}%. Skills listed: {p['skills_count']}.", B)]
    s += bullets([f"Missing: {m}" for m in p["missing"][:6]])
    s += [Paragraph("Resume readiness", H2), Paragraph(f"Score: {r['score']}/100. ATS rating: {r['ats_rating']} ({r['ats_pct']}%).", B)]
    s += bullets([f"Missing keyword: {m}" for m in r["missing_keywords"][:6]] + r["improvements"][:3])
    cats = ", ".join(f"{a}: {b}/10" for a, b in i["by_category"].items()) or "No completed interviews yet"
    s += [Paragraph("Interview readiness", H2), Paragraph(f"Sessions: {i['sessions']}. Average: {i['avg']}/10. {esc(cats)}. Weakest area: {esc(i['weakest'] or 'n/a')}.", B)]
    s += [Paragraph("Technical skill readiness", H2), Paragraph(f"Solved {t['solved']} of {t['available']} problems. Success rate {t['success_rate']}%.", B)]
    s += bullets([f"Skill gap: {g}" for g in k["gap"][:6]] + [f"Recommended: {c['title']} ({c['difficulty']})" for c in t["recommended"]])
    s += [Paragraph("Learning progress", H2), Paragraph(f"{l['percent']}% complete ({l['done']} of {l['total']} modules). About {l['weeks_left']} weeks to finish at 8 hours/week.", B)]
    s += bullets([f"Pending: {m}" for m in l["pending_modules"]])

    rows = [["Job", "Company", "Match", "Skills to add"]] + [[j["title"], j["company"], f"{j['match']}%", ", ".join(j["skills_gap"][:3]) or "None"] for j in d["jobs"]["top"]]
    tb = Table(rows, colWidths=[5 * cm, 3.5 * cm, 1.8 * cm, 6 * cm], repeatRows=1)
    tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INDIGO), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D5DB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    j = d["jobs"]
    s += [KeepTogether([Paragraph("Job match analysis", H2), tb, Spacer(1, 4),
                        Paragraph(f"Applications: {j['applied']} applied, {j['interviews']} interviews, {j['offers']} offers, {j['rejected']} rejected. Saved: {j['saved']}.", B)])]

    ap = d["action_plan"]
    s += [KeepTogether([Paragraph("Personalized action plan", H2)] + [Paragraph(f"{a['priority']}. <b>{esc(a['title'])}</b>: {esc(a['detail'])}", B) for a in ap["actions"]]),
          Paragraph("Weekly goals", H2)] + bullets(ap["weekly_goals"]) + [Paragraph("Recommended resources", H2)] + bullets(ap["resources"])
    tl = ap["timeline"]
    s += [Paragraph("Readiness timeline", H2), Paragraph(f"Estimated {tl['to_job_ready_weeks']} weeks to reach Job-Ready and {tl['to_interview_ready_weeks']} weeks to reach Interview-Ready at your current pace.", B)]
    doc.build(s)
    buf.seek(0)
    return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name="CareerVerse_Job_Readiness_Report.pdf")
