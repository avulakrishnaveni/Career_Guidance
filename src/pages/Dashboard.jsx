import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar as RBar } from "recharts";
import { FileText, Mic, Code2, Briefcase, Compass, GraduationCap, Flame, Award } from "lucide-react";
import api, { msg, ago } from "../utils/api";
import { ScoreRing, Skeleton, Empty, ErrorBox, Bar } from "../components/ui.jsx";
import { useAuth } from "../context/AuthContext.jsx";

const QUICK = [["/resume", "Analyze resume", FileText], ["/interview", "Mock interview", Mic], ["/coding", "Solve a problem", Code2], ["/jobs", "Browse jobs", Briefcase], ["/career", "Career path", Compass], ["/learning", "Continue learning", GraduationCap]];

function Mini({ data, kind }) {
  if (!data.length) return <Empty>No data yet.</Empty>;
  return <div className="chart"><ResponsiveContainer>
    {kind === "bar" ? <BarChart data={data}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis dataKey="date" fontSize={11} /><YAxis domain={[0, 10]} fontSize={11} /><Tooltip /><RBar dataKey="score" fill="#7C3AED" radius={[6, 6, 0, 0]} /></BarChart>
      : <LineChart data={data}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis dataKey={kind === "day" ? "day" : "date"} fontSize={11} /><YAxis domain={[0, 100]} fontSize={11} /><Tooltip /><Line type="monotone" dataKey="score" stroke="#4F46E5" strokeWidth={3} dot={{ r: 3 }} /></LineChart>}
  </ResponsiveContainer></div>;
}

export default function Dashboard() {
  const { user } = useAuth();
  const [d, setD] = useState(null); const [error, setError] = useState("");
  useEffect(() => { api.get("/dashboard/stats").then(({ data }) => setD(data)).catch((e) => setError(msg(e))); }, []);

  if (error) return <ErrorBox>{error}</ErrorBox>;
  if (!d) return <><Skeleton h={150} /><Skeleton h={110} n={2} /></>;
  const lastResume = d.resume_trend.at(-1)?.score ?? "-";

  return (<>
    <div className="hero">
      <ScoreRing value={d.readiness.score} color="#fff" size={110} label="Readiness" />
      <div className="grow">
        <h1>Hello, {user?.name?.split(" ")[0]}</h1>
        <p>Your readiness level: <span className="badge-level" style={{ background: d.readiness.color }}>{d.readiness.level}</span></p>
        {d.career && <p style={{ marginTop: ".4rem" }}>Target: {d.career.role} ({d.career.domain})</p>}
      </div>
      <Link to="/report" className="btn" style={{ background: "rgba(255,255,255,.2)" }}>View full report</Link>
    </div>

    <div className="grid">
      <div className="panel stat"><span>Profile completeness</span><b>{d.profile.completeness}%</b><Bar value={d.profile.completeness} /></div>
      <div className="panel stat"><span>Roadmap progress</span><b>{d.roadmap_percent}%</b><Bar value={d.roadmap_percent} /></div>
      <div className="panel stat"><span>Latest resume score</span><b>{lastResume}</b></div>
      <div className="panel stat"><span>Coding solved / points</span><b>{d.coding.solved} / {d.coding.points}</b></div>
      <div className="panel stat"><span>Day streak</span><b><Flame size={22} color="#f59e0b" style={{ verticalAlign: "-3px" }} /> {d.streak}</b></div>
      <div className="panel stat"><span>Saved / applied jobs</span><b>{d.jobs.saved} / {d.jobs.applied}</b></div>
    </div>

    <div className="grid2">
      <div className="panel"><h2>Readiness trend</h2><Mini data={d.readiness.history} kind="day" /></div>
      <div className="panel"><h2>Resume score trend</h2><Mini data={d.resume_trend} /></div>
      <div className="panel"><h2>Interview performance</h2><Mini data={d.interview_trend} kind="bar" /></div>
      <div className="panel"><h2>Next best actions</h2>
        {d.actions.length === 0 ? <Empty>You're on track. Keep practising!</Empty> : d.actions.map((a) => (
          <Link key={a.title} to={a.link} className="tile" style={{ marginBottom: ".5rem" }}><div><b>{a.title}</b><div className="muted" style={{ fontSize: ".85rem" }}>{a.detail}</div></div></Link>))}
      </div>
    </div>

    <div className="grid2">
      <div className="panel"><h2>Quick actions</h2><div className="grid" style={{ gridTemplateColumns: "repeat(auto-fill,minmax(150px,1fr))" }}>
        {QUICK.map(([to, label, Icon]) => <Link key={to} to={to} className="tile"><Icon size={18} />{label}</Link>)}</div>
        {d.top_job && <p className="muted" style={{ marginTop: ".8rem" }}>Top job match: <b>{d.top_job.title}</b> at {d.top_job.company} ({d.top_job.match}%)</p>}</div>
      <div className="panel"><h2>Badges</h2>
        {d.badges.length ? d.badges.map((b) => <span key={b} className="chip"><Award size={12} style={{ verticalAlign: "-2px" }} /> {b}</span>) : <Empty>Complete activities to earn badges.</Empty>}
        <h2 style={{ marginTop: "1rem" }}>Recent activity</h2>
        {d.activity.length === 0 ? <Empty>No activity yet.</Empty> : <div className="timeline">{d.activity.map((a, i) => <div className="t" key={i}>{a.detail}<div className="muted" style={{ fontSize: ".8rem" }}>{ago(a.at)}</div></div>)}</div>}
      </div>
    </div>
  </>);
}
