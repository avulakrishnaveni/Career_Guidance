import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Bookmark, BookmarkCheck, MapPin } from "lucide-react";
import api, { msg, ago } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { Skeleton, Empty, ErrorBox, Bar } from "../components/ui.jsx";

const STATUSES = ["Applied", "Interview", "Offer", "Rejected"];

export default function Jobs() {
  const toast = useToast();
  const [tab, setTab] = useState("all");
  const [f, setF] = useState({ q: "", domain: "", location: "", experience: "", job_type: "" });
  const [domains, setDomains] = useState([]); const [data, setData] = useState(null); const [apps, setApps] = useState(null); const [error, setError] = useState("");

  const loadJobs = () => api.get("/jobs", { params: { ...Object.fromEntries(Object.entries(f).filter(([, v]) => v)), view: tab === "saved" ? "saved" : undefined } })
    .then(({ data }) => setData(data)).catch((e) => setError(msg(e)));
  const loadApps = () => api.get("/jobs/applications").then(({ data }) => setApps(data)).catch((e) => setError(msg(e)));

  useEffect(() => { api.get("/career/domains").then(({ data }) => setDomains(data.domains.map((d) => d.name))).catch(() => {}); }, []);
  useEffect(() => { if (tab === "apps") loadApps(); else { const t = setTimeout(loadJobs, 250); return () => clearTimeout(t); } }, [tab, f]);

  const save = async (j) => { try { const { data: r } = await api.post("/jobs/save", { job_id: j.id }); setData((d) => ({ ...d, jobs: d.jobs.map((x) => x.id === j.id ? { ...x, saved: r.saved } : x).filter((x) => tab !== "saved" || x.saved) })); toast(r.saved ? "Job saved" : "Removed from saved"); } catch (e) { setError(msg(e)); } };
  const apply = async (j, status = "Applied", open = true) => {
    try { await api.post("/jobs/apply", { job_id: j.id, status }); toast(`Marked as ${status}`); if (open && j.apply_url) window.open(j.apply_url, "_blank", "noopener"); tab === "apps" ? loadApps() : loadJobs(); }
    catch (e) { setError(msg(e)); }
  };
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  return (<>
    <div className="tabs">{[["all", "Recommended"], ["saved", "Saved"], ["apps", "My applications"]].map(([k, l]) => <button key={k} className={"tab" + (tab === k ? " on" : "")} onClick={() => { setTab(k); setError(""); }}>{l}</button>)}</div>
    <ErrorBox>{error}</ErrorBox>
    {tab !== "apps" && (<>
      <div className="panel"><div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit,minmax(150px,1fr))" }}>
        <input placeholder="Search title" value={f.q} onChange={set("q")} aria-label="Search" />
        <select value={f.domain} onChange={set("domain")} aria-label="Domain"><option value="">All domains</option>{domains.map((d) => <option key={d}>{d}</option>)}</select>
        <input placeholder="Location" value={f.location} onChange={set("location")} aria-label="Location" />
        <select value={f.experience} onChange={set("experience")} aria-label="Experience"><option value="">Any experience</option>{["Fresher", "Junior", "Mid", "Senior"].map((x) => <option key={x}>{x}</option>)}</select>
        <select value={f.job_type} onChange={set("job_type")} aria-label="Job type"><option value="">Any type</option>{["Full-time", "Internship", "Contract"].map((x) => <option key={x}>{x}</option>)}</select></div></div>
      {data && !data.has_skills && <div className="demo">Add skills in your <Link to="/profile">profile</Link> to improve match scores.</div>}
      {!data ? <Skeleton h={130} n={3} /> : data.jobs.length === 0 ? <Empty>No jobs match these filters.</Empty> : data.jobs.map((j) => (
        <div className="panel" key={j.id}>
          <div className="between"><div><h3 style={{ margin: 0 }}>{j.title}</h3><span className="muted">{j.company} | <MapPin size={12} style={{ verticalAlign: "-1px" }} /> {j.location} | {j.salary}</span></div>
            <div style={{ minWidth: 110, textAlign: "right" }}><b style={{ color: j.match >= 70 ? "var(--ok)" : "var(--ink)" }}>{j.match}% match</b><Bar value={j.match} /></div></div>
          <p>{j.description}</p>
          <span className="chip">{j.domain}</span><span className="chip">{j.experience_level}</span><span className="chip">{j.job_type}</span>
          <div>{j.skills.map((s) => <span key={s} className="chip">{s}</span>)}</div>
          <div style={{ display: "flex", gap: ".5rem", flexWrap: "wrap", marginTop: ".5rem" }}>
            <button className="btn small" onClick={() => apply(j)}>{j.status ? `Status: ${j.status}` : "Apply now"}</button>
            <button className="btn outline small" onClick={() => save(j)}>{j.saved ? <><BookmarkCheck size={14} /> Saved</> : <><Bookmark size={14} /> Save</>}</button></div>
        </div>))}
    </>)}
    {tab === "apps" && (!apps ? <Skeleton h={90} n={2} /> : (<>
      <div className="grid">{STATUSES.map((s) => <div key={s} className="panel stat"><span>{s}</span><b>{apps.counts[s]}</b></div>)}</div>
      {apps.applications.length === 0 ? <Empty>No applications yet. Use "Apply now" on a job to start tracking.</Empty> : (
        <div className="panel">{apps.applications.map((a) => (
          <div key={a.job_id} className="between" style={{ padding: ".6rem 0", borderBottom: "1px solid var(--line)" }}>
            <div><b>{a.title}</b><div className="muted" style={{ fontSize: ".85rem" }}>{a.company} | {a.location} | updated {ago(a.updated_at)}</div></div>
            <select value={a.status} style={{ width: "auto" }} onChange={(e) => apply({ id: a.job_id }, e.target.value, false)} aria-label={`Status for ${a.title}`}>{STATUSES.map((s) => <option key={s}>{s}</option>)}</select>
          </div>))}</div>)}
    </>))}
  </>);
}
