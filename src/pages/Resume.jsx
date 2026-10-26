import { useEffect, useState } from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { Download } from "lucide-react";
import api, { msg, fmtDate } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ScoreRing, Bar, ErrorBox } from "../components/ui.jsx";

const List = ({ title, items }) => items?.length ? <><h3>{title}</h3><ul className="clean">{items.map((i) => <li key={i}>{i}</li>)}</ul></> : null;

function download(r) {
  const lines = [`CareerVerse Resume Analysis: ${r.filename || ""}`, `Overall score: ${r.score}/100`, `ATS: ${r.ats.rating} (${r.ats.pct}%)`, "",
    "Section scores:", ...r.sections.map((s) => `  ${s.name}: ${s.score}/100`), "", "Missing sections: " + (r.missing_sections.join(", ") || "none"),
    "Missing ATS keywords: " + (r.ats.missing.join(", ") || "none"), "Skills found: " + (r.skills.join(", ") || "none"), "",
    "Strengths:", ...r.strengths.map((x) => "  - " + x), "Improvements:", ...r.improvements.map((x) => "  - " + x), "Recommendations:", ...r.recommendations.map((x) => "  - " + x)];
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/plain" })); a.download = "resume-analysis.txt"; a.click(); URL.revokeObjectURL(a.href);
}

export default function Resume() {
  const toast = useToast();
  const [file, setFile] = useState(null); const [res, setRes] = useState(null); const [hist, setHist] = useState([]);
  const [loading, setLoading] = useState(false); const [error, setError] = useState("");
  const load = () => api.get("/resume/history").then(({ data }) => { setHist(data); if (data.length && !res) setRes({ ...data.at(-1).analysis, filename: data.at(-1).filename }); }).catch((e) => setError(msg(e)));
  useEffect(() => { load(); }, []);

  const upload = async () => {
    setError("");
    if (!file) return setError("Choose a PDF, DOC or DOCX file");
    if (file.size > 5 * 1024 * 1024) return setError("File must be under 5 MB");
    const fd = new FormData(); fd.append("resume", file); setLoading(true);
    try { const { data } = await api.post("/resume/upload", fd); setRes(data); toast(`Resume scored ${data.score}/100`); await load(); }
    catch (e) { setError(msg(e)); } finally { setLoading(false); }
  };

  return (<>
    <div className="panel"><h2>Upload your resume</h2>
      <input type="file" accept=".pdf,.doc,.docx" onChange={(e) => setFile(e.target.files[0])} aria-label="Resume file" />
      <ErrorBox>{error}</ErrorBox>
      <button className="btn block" onClick={upload} disabled={loading}>{loading ? "Analyzing..." : "Analyze resume"}</button>
      <p className="muted" style={{ fontSize: ".85rem" }}>Your file is read for analysis and not stored. ATS keywords are matched to your selected career domain.</p></div>
    {res && (<>
      <div className="panel"><div className="between"><div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <ScoreRing value={res.score} label="Overall" />
        <div><h2 style={{ margin: 0 }}>{res.filename}</h2><span className={"chip " + (res.ats.rating === "Strong" ? "ok" : res.ats.rating === "Weak" ? "bad" : "")}>ATS: {res.ats.rating} ({res.ats.pct}%)</span></div></div>
        <button className="btn outline" onClick={() => download(res)}><Download size={16} /> Download report</button></div></div>
      <div className="grid2">
        <div className="panel"><h2>Section scores</h2>{res.sections.map((s) => (
          <div key={s.name} style={{ marginBottom: ".6rem" }}><div className="between"><span>{s.name}</span><b className={s.present ? "" : "fail"}>{s.present ? s.score : "Missing"}</b></div><Bar value={s.score} /></div>))}</div>
        <div className="panel"><h2>ATS keywords</h2>
          <h3>Found</h3>{res.ats.matched.length ? res.ats.matched.map((k) => <span className="chip ok" key={k}>{k}</span>) : <p className="muted">None found</p>}
          <h3>Suggested additions</h3>{res.ats.missing.map((k) => <span className="chip bad" key={k}>{k}</span>)}
          <h3>Skills detected</h3>{res.skills.length ? res.skills.map((k) => <span className="chip" key={k}>{k}</span>) : <p className="muted">No known skills detected</p>}</div>
      </div>
      <div className="panel"><List title="Strengths" items={res.strengths} /><List title="Areas to improve" items={res.improvements} /><List title="Recommendations" items={res.recommendations} /></div>
    </>)}
    {hist.length > 0 && <div className="panel"><h2>Score history</h2>
      <div className="chart"><ResponsiveContainer><LineChart data={hist.map((h) => ({ date: fmtDate(h.created_at), score: h.score }))}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis dataKey="date" fontSize={11} /><YAxis domain={[0, 100]} fontSize={11} /><Tooltip /><Line type="monotone" dataKey="score" stroke="#4F46E5" strokeWidth={3} /></LineChart></ResponsiveContainer></div></div>}
  </>);
}
