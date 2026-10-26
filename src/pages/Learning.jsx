import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Flame } from "lucide-react";
import api, { msg } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox, Skeleton, Bar } from "../components/ui.jsx";

export default function Learning() {
  const toast = useToast();
  const [d, setD] = useState(null); const [error, setError] = useState(""); const [open, setOpen] = useState(null);
  useEffect(() => { api.get("/progress").then(({ data }) => setD(data)).catch((e) => setError(msg(e))); }, []);

  const toggle = async (m) => {
    try { const { data } = await api.post("/progress/update", { module_id: m.id, completed: !m.completed }); setD(data); if (!m.completed) toast(`Completed: ${m.title}`); }
    catch (e) { setError(msg(e)); }
  };

  if (!d) return error ? <ErrorBox>{error}</ErrorBox> : <Skeleton h={120} n={3} />;
  if (!d.roadmap) return <div className="panel"><h2>No learning path yet</h2><p><Link to="/career">Choose a career path</Link> and your modules will appear here.</p></div>;
  const r = d.roadmap;
  return (<>
    <div className="grid">
      <div className="panel stat"><span>Completion</span><b>{r.percent}%</b><Bar value={r.percent} /></div>
      <div className="panel stat"><span>Modules done</span><b>{r.completed} / {r.total}</b></div>
      <div className="panel stat"><span>Learning streak</span><b><Flame size={20} color="#f59e0b" style={{ verticalAlign: "-3px" }} /> {d.streak} days</b></div>
      <div className="panel stat"><span>Weekly goal (2 modules)</span><b>{Math.min(d.weekly_goal.done, 2)} / 2</b><Bar value={d.weekly_goal.done / 2 * 100} /></div>
      <div className="panel stat"><span>Time to finish</span><b>{d.weeks_left} wk</b><span>{d.hours_left} hours left</span></div>
    </div>
    <div className="panel"><h2>{r.path.domain}: modules</h2><ErrorBox>{error}</ErrorBox>
      {r.milestones.map((m) => (
        <div key={m.id} className={"mod" + (m.completed ? " done" : "")}>
          <div className="head">
            <input type="checkbox" checked={m.completed} onChange={() => toggle(m)} aria-label={`Mark ${m.title} complete`} />
            <div style={{ flex: 1 }}><h3 style={{ margin: 0 }}>{m.title}</h3><span className="muted" style={{ fontSize: ".85rem" }}>Weeks {m.start_week}-{m.end_week} | {m.hours} hours</span></div>
            <button className="btn outline small" onClick={() => setOpen(open === m.id ? null : m.id)}>{open === m.id ? "Hide" : "Lessons"}</button>
          </div>
          {open === m.id && <div style={{ marginLeft: "1.9rem", marginTop: ".5rem" }}><ul className="clean">{m.lessons.map((l) => <li key={l}>{l}</li>)}</ul><span className="muted">Resource: {m.resource}</span></div>}
        </div>))}
    </div>
  </>);
}
