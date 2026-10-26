import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api, { msg } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox, Skeleton } from "../components/ui.jsx";

export function Roadmap({ r }) {
  return (<div className="panel">
    <div className="between"><h2>Roadmap: {r.path.domain} / {r.path.role}</h2><span className="chip">{r.total_hours} hours, about {r.total_weeks} weeks at {r.hours_per_week} h/week</span></div>
    <p className="muted">Goal: {r.path.goal} | Level: {r.path.experience_level}</p>
    <div className="timeline">{r.milestones.map((m) => (
      <div className="t" key={m.id}><b>Weeks {m.start_week}-{m.end_week}: {m.title}</b> {m.completed && <span className="chip ok">Done</span>}
        <div className="muted" style={{ fontSize: ".88rem" }}>{m.hours} hours | Resource: {m.resource}</div>
        <div>{m.lessons.map((l) => <span className="chip" key={l}>{l}</span>)}</div></div>))}</div>
    <h3>Required skills</h3>{r.required_skills.map((s) => <span className="chip" key={s}>{s}</span>)}
    <p><Link to="/learning" className="btn small">Track progress</Link></p>
  </div>);
}

export default function Career() {
  const toast = useToast();
  const [meta, setMeta] = useState(null); const [road, setRoad] = useState(null);
  const [sel, setSel] = useState({ domain: "", role: "", experience_level: "Beginner", goal: "Job-ready" }); const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api.get("/career/domains"), api.get("/career/roadmap")]).then(([a, b]) => {
      setMeta(a.data);
      if (b.data.roadmap) { setRoad(b.data.roadmap); setSel({ ...sel, ...b.data.roadmap.path }); }
    }).catch((e) => setError(msg(e)));
  }, []);

  const save = async () => {
    setError("");
    if (!sel.domain || !sel.role) return setError("Choose a domain and a role");
    try { const { data } = await api.post("/career/select", sel); setRoad(data.roadmap); toast("Career path saved. Roadmap ready."); }
    catch (e) { setError(msg(e)); }
  };

  if (!meta) return error ? <ErrorBox>{error}</ErrorBox> : <Skeleton h={160} n={2} />;
  const cur = meta.domains.find((d) => d.name === sel.domain);
  return (<>
    <div className="panel">
      <h2>Choose your domain</h2><ErrorBox>{error}</ErrorBox>
      <div className="grid">{meta.domains.map((d) => (
        <button key={d.name} className={"choice" + (sel.domain === d.name ? " on" : "")} style={{ textAlign: "left", margin: 0 }} onClick={() => setSel({ ...sel, domain: d.name, role: "" })}>
          <b>{d.name}</b><div className="muted" style={{ fontSize: ".8rem" }}>{d.modules} modules, {d.hours} hours</div></button>))}</div>
      {cur && (<>
        <div className="row">
          <div><label>Role</label><select value={sel.role} onChange={(e) => setSel({ ...sel, role: e.target.value })}><option value="">Select</option>{cur.roles.map((r) => <option key={r}>{r}</option>)}</select></div>
          <div><label>Experience level</label><select value={sel.experience_level} onChange={(e) => setSel({ ...sel, experience_level: e.target.value })}>{meta.levels.map((l) => <option key={l}>{l}</option>)}</select></div>
        </div>
        <label>Learning goal</label>{meta.goals.map((g) => <button key={g} className={"choice" + (sel.goal === g ? " on" : "")} onClick={() => setSel({ ...sel, goal: g })}>{g}</button>)}
        <button className="btn block" onClick={save}>Save and generate roadmap</button>
      </>)}
    </div>
    {road && <Roadmap r={road} />}
  </>);
}
