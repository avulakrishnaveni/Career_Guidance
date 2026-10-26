import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ResponsiveContainer, BarChart, Bar as RBar, XAxis, YAxis, Tooltip, CartesianGrid, LineChart, Line, Cell } from "recharts";
import { Download } from "lucide-react";
import api, { msg } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ScoreRing, Skeleton, Bar, ErrorBox, Empty } from "../components/ui.jsx";

const Sec = ({ n, title, children }) => <div className="panel"><h2>{n}. {title}</h2>{children}</div>;

export default function Report() {
  const toast = useToast();
  const [d, setD] = useState(null); const [error, setError] = useState(""); const [dl, setDl] = useState(false);
  useEffect(() => { api.get("/report/readiness").then(({ data }) => setD(data)).catch((e) => setError(msg(e))); }, []);

  const pdf = async () => {
    setDl(true);
    try {
      const { data } = await api.get("/report/readiness/pdf", { responseType: "blob" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(data); a.download = "CareerVerse_Job_Readiness_Report.pdf"; a.click(); URL.revokeObjectURL(a.href);
      toast("PDF downloaded");
    } catch (e) { setError("Could not generate the PDF. Please try again."); } finally { setDl(false); }
  };

  if (!d) return error ? <ErrorBox>{error}</ErrorBox> : <><Skeleton h={160} /><Skeleton h={200} n={2} /></>;
  const { profile: p, resume: r, interview: i, technical: t, learning: l, skills: k, jobs: j, action_plan: ap } = d;
  const comps = d.components.map((c) => ({ name: c.label, score: c.score }));
  const cats = Object.entries(i.by_category);

  return (<>
    <div className="hero">
      <ScoreRing value={d.score} color="#fff" size={130} label="Readiness" />
      <div className="grow"><h1>Job Readiness Report</h1>
        <p><span className="badge-level" style={{ background: d.color }}>{d.level}</span> {d.domain ? `for ${d.domain}` : ""}</p>
        <p style={{ marginTop: ".4rem" }}>Beginner 0-40 | Developing 41-60 | Job-Ready 61-80 | Interview-Ready 81-100</p></div>
      <button className="btn" style={{ background: "rgba(255,255,255,.2)" }} onClick={pdf} disabled={dl}><Download size={16} /> {dl ? "Preparing..." : "Download PDF"}</button>
    </div>
    <ErrorBox>{error}</ErrorBox>
    {!d.domain && <div className="demo">Choose a <Link to="/career">career path</Link> to unlock skill match, learning and job-fit scoring.</div>}

    <div className="grid2">
      <div className="panel"><h2>1. Overall score breakdown</h2>
        <div className="chart"><ResponsiveContainer><BarChart data={comps} layout="vertical" margin={{ left: 20 }}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis type="number" domain={[0, 100]} fontSize={11} /><YAxis type="category" dataKey="name" fontSize={11} width={80} /><Tooltip />
          <RBar dataKey="score" radius={[0, 6, 6, 0]}>{comps.map((_, x) => <Cell key={x} fill={x % 2 ? "#7C3AED" : "#4F46E5"} />)}</RBar></BarChart></ResponsiveContainer></div>
        <p className="muted" style={{ fontSize: ".82rem" }}>Weights: {d.components.map((c) => `${c.label} ${c.weight}%`).join(", ")}</p></div>
      <div className="panel"><h2>Readiness trend</h2>{d.history.length < 2 ? <Empty>Your trend appears after a second day of activity. Today: {d.score}.</Empty> :
        <div className="chart"><ResponsiveContainer><LineChart data={d.history}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis dataKey="day" fontSize={11} /><YAxis domain={[0, 100]} fontSize={11} /><Tooltip /><Line dataKey="score" stroke="#4F46E5" strokeWidth={3} /></LineChart></ResponsiveContainer></div>}</div>
    </div>

    <Sec n={2} title="Profile strength"><div className="between"><span>Completeness</span><b>{p.completeness}%</b></div><Bar value={p.completeness} />
      <p>Education / role: <b>{p.education || "Not set"}</b> | Skills listed: <b>{p.skills_count}</b></p>
      {p.missing.length > 0 && <><b>Missing sections</b><div>{p.missing.map((m) => <span className="chip bad" key={m}>{m}</span>)}</div></>}
      <h3 style={{ marginTop: ".6rem" }}>Skills vs target role</h3>{k.required.length === 0 ? <Empty>Select a career path first.</Empty> : <>
        {k.matched.map((s) => <span className="chip ok" key={s}>{s}</span>)}{k.gap.map((s) => <span className="chip bad" key={s}>{s}</span>)}</>}</Sec>

    <Sec n={3} title="Resume readiness">{!r.uploaded ? <p>No resume analyzed yet. <Link to="/resume">Upload your resume</Link>.</p> : <>
      <p>Score <b>{r.score}/100</b> | ATS <b>{r.ats_rating} ({r.ats_pct}%)</b></p>
      {r.missing_keywords.length > 0 && <><b>Missing keywords</b><div>{r.missing_keywords.map((m) => <span className="chip bad" key={m}>{m}</span>)}</div></>}
      {r.improvements.length > 0 && <><b>Priority improvements</b><ul className="clean">{r.improvements.map((m) => <li key={m}>{m}</li>)}</ul></>}</>}</Sec>

    <Sec n={4} title="Interview readiness">{i.sessions === 0 ? <p>No completed mock interviews. <Link to="/interview">Start one</Link>.</p> : <>
      <p>Sessions <b>{i.sessions}</b> | Average <b>{i.avg}/10</b> | Weakest area <b>{i.weakest}</b></p>
      {cats.map(([c, v]) => <div key={c} style={{ marginBottom: ".5rem" }}><div className="between"><span>{c}</span><b>{v}/10</b></div><Bar value={v * 10} /></div>)}</>}</Sec>

    <Sec n={5} title="Technical skill readiness"><p>Solved <b>{t.solved}</b> of {t.available} | Success rate <b>{t.success_rate}%</b> | Attempts {t.attempts}</p>
      {t.recommended.length > 0 && <><b>Recommended challenges</b><div>{t.recommended.map((c) => <Link key={c.id} to="/coding" className={"chip " + c.difficulty}>{c.title}</Link>)}</div></>}</Sec>

    <Sec n={6} title="Learning progress"><div className="between"><span>{l.done} of {l.total} modules</span><b>{l.percent}%</b></div><Bar value={l.percent} />
      <p>About <b>{l.weeks_left} weeks</b> to finish the roadmap ({l.hours_left} hours left).</p>
      {l.pending_modules.length > 0 && <><b>Pending</b><ul className="clean">{l.pending_modules.map((m) => <li key={m}>{m}</li>)}</ul></>}</Sec>

    <Sec n={7} title="Job match analysis">
      {j.top.map((x) => <div key={x.id} className="between" style={{ padding: ".5rem 0", borderBottom: "1px solid var(--line)" }}>
        <div><b>{x.title}</b> <span className="muted">at {x.company}</span>{x.skills_gap.length > 0 && <div className="muted" style={{ fontSize: ".82rem" }}>Skills to add: {x.skills_gap.join(", ")}</div>}</div><b>{x.match}%</b></div>)}
      <p className="muted">Applications: {j.applied} applied, {j.interviews} interviews, {j.offers} offers, {j.rejected} rejected | Saved: {j.saved}</p></Sec>

    <Sec n={8} title="Personalized action plan">
      {ap.actions.length === 0 ? <Empty>Everything is in great shape.</Empty> : ap.actions.map((a) => <Link key={a.title} to={a.link} className="tile" style={{ marginBottom: ".5rem" }}><div><b>{a.priority}. {a.title}</b><div className="muted" style={{ fontSize: ".85rem" }}>{a.detail}</div></div></Link>)}
      <div className="grid2"><div><h3>Weekly goals</h3><ul className="clean">{ap.weekly_goals.map((g) => <li key={g}>{g}</li>)}</ul></div>
        <div><h3>Recommended resources</h3><ul className="clean">{ap.resources.map((g) => <li key={g}>{g}</li>)}</ul></div></div>
      <p><b>Timeline:</b> about {ap.timeline.to_job_ready_weeks} weeks to Job-Ready and {ap.timeline.to_interview_ready_weeks} weeks to Interview-Ready at about 4 points per week.</p></Sec>

    <Sec n={9} title="Readiness level badge"><span className="badge-level" style={{ background: d.color, fontSize: "1.2rem" }}>{d.level}</span>
      <div style={{ marginTop: ".6rem" }}>{d.badges.map((b) => <span key={b} className="chip">{b}</span>)}</div></Sec>
  </>);
}
