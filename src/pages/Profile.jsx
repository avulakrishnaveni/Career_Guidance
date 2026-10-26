import { useEffect, useState } from "react";
import api, { msg } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox, Skeleton, Bar } from "../components/ui.jsx";

const LEVELS = ["10th", "12th", "Diploma", "B.Tech/B.E", "B.Sc", "B.Com", "BBA", "M.Tech", "M.Sc", "MBA", "PhD"];
const EMPTY = { profile_type: "student", education_level: "", institution: "", edu_start_year: "", edu_end_year: "", degree: "", branch: "", grade: "",
  company: "", designation: "", work_start_year: "", work_end_year: "", total_experience: "", is_current: false, skills: [], bio: "", linkedin: "", github: "", photo: "" };

export default function Profile() {
  const toast = useToast();
  const [f, setF] = useState(EMPTY); const [info, setInfo] = useState({ completeness: 0, missing: [] }); const [name, setName] = useState("");
  const [tag, setTag] = useState(""); const [error, setError] = useState(""); const [loading, setLoading] = useState(true);
  const set = (k) => (e) => setF({ ...f, [k]: e.target.type === "checkbox" ? e.target.checked : e.target.value });

  const apply = (data) => {
    setInfo({ completeness: data.completeness, missing: data.missing }); setName(data.user.name);
    if (data.profile) setF({ ...EMPTY, ...Object.fromEntries(Object.entries(data.profile).filter(([k]) => k in EMPTY).map(([k, v]) => [k, v ?? EMPTY[k]])) });
  };
  useEffect(() => { api.get("/profile").then(({ data }) => apply(data)).catch((e) => setError(msg(e))).finally(() => setLoading(false)); }, []);

  const addTag = () => { const t = tag.trim().replace(/,$/, ""); if (t && !f.skills.includes(t)) setF({ ...f, skills: [...f.skills, t] }); setTag(""); };
  const photo = (e) => {
    const file = e.target.files[0]; if (!file) return;
    if (!file.type.startsWith("image/") || file.size > 300 * 1024) return setError("Photo must be an image under 300 KB");
    const r = new FileReader(); r.onload = () => { setF({ ...f, photo: r.result }); setError(""); }; r.readAsDataURL(file);
  };
  const save = async (e) => {
    e.preventDefault(); setError("");
    try { const { data } = await api.post("/profile", { ...f, skills: tag.trim() ? [...f.skills, tag.trim()] : f.skills }); apply(data); setTag(""); toast("Profile saved"); }
    catch (err) { setError(msg(err)); }
  };

  if (loading) return <Skeleton h={200} n={2} />;
  const student = f.profile_type === "student";
  return (
    <form onSubmit={save}>
      <div className="panel">
        <div className="between"><h2>Profile completeness</h2><b>{info.completeness}%</b></div><Bar value={info.completeness} />
        {info.missing.length > 0 && <p className="muted" style={{ fontSize: ".85rem" }}>To finish: {info.missing.slice(0, 5).join(", ")}</p>}
      </div>
      <div className="panel">
        <div style={{ display: "flex", gap: "1rem", alignItems: "center", flexWrap: "wrap" }}>
          {f.photo ? <img className="avatar" src={f.photo} alt="Profile" /> : <div className="avatar">{name[0]}</div>}
          <div><b>{name}</b><br /><label className="btn outline small" style={{ display: "inline-block", margin: ".3rem 0 0", cursor: "pointer" }}>Upload photo<input type="file" accept="image/*" hidden onChange={photo} /></label></div>
        </div>
        <ErrorBox>{error}</ErrorBox>
        <label>I am a</label>
        {[["student", "Student"], ["employee", "Working professional"]].map(([v, t]) => <button type="button" key={v} className={"choice" + (f.profile_type === v ? " on" : "")} onClick={() => setF({ ...f, profile_type: v })}>{t}</button>)}
        {student ? (<>
          <label>Highest education</label><select value={f.education_level} onChange={set("education_level")}><option value="">Select</option>{LEVELS.map((l) => <option key={l}>{l}</option>)}</select>
          <label>College / school name</label><input value={f.institution} onChange={set("institution")} />
          <div className="row"><div><label>Start year</label><input maxLength={4} value={f.edu_start_year} onChange={set("edu_start_year")} /></div><div><label>End year</label><input maxLength={4} value={f.edu_end_year} onChange={set("edu_end_year")} /></div></div>
          <div className="row"><div><label>Degree</label><input value={f.degree} onChange={set("degree")} /></div><div><label>Branch / specialization</label><input value={f.branch} onChange={set("branch")} /></div></div>
          <label>CGPA or percentage</label><input value={f.grade} onChange={set("grade")} />
        </>) : (<>
          <label>Company</label><input value={f.company} onChange={set("company")} />
          <label>Designation</label><input value={f.designation} onChange={set("designation")} />
          <div className="row"><div><label>Start year</label><input maxLength={4} value={f.work_start_year} onChange={set("work_start_year")} /></div>
            <div><label>End year</label><input disabled={f.is_current} value={f.is_current ? "Present" : f.work_end_year} onChange={set("work_end_year")} /></div></div>
          <label style={{ display: "flex", gap: ".5rem", alignItems: "center" }}><input type="checkbox" checked={f.is_current} onChange={set("is_current")} />I currently work here</label>
          <label>Total experience (years)</label><input value={f.total_experience} onChange={set("total_experience")} placeholder="e.g. 2.5" />
        </>)}
        <label>Skills (press Enter or comma to add)</label>
        <div className="tags">{f.skills.map((s) => <span className="chip" key={s}>{s}<button type="button" aria-label={`Remove ${s}`} onClick={() => setF({ ...f, skills: f.skills.filter((x) => x !== s) })}>×</button></span>)}
          <input value={tag} onChange={(e) => setTag(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" || e.key === ",") { e.preventDefault(); addTag(); } }} placeholder="Python, React, SQL" aria-label="Add skill" /></div>
        <label>Bio</label><textarea rows={3} value={f.bio} onChange={set("bio")} maxLength={500} />
        <div className="row"><div><label>LinkedIn URL</label><input value={f.linkedin} onChange={set("linkedin")} placeholder="https://linkedin.com/in/..." /></div>
          <div><label>GitHub URL</label><input value={f.github} onChange={set("github")} placeholder="https://github.com/..." /></div></div>
        <button className="btn block">Save profile</button>
      </div>
    </form>
  );
}
