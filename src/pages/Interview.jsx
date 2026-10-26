import { useEffect, useRef, useState } from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar as RBar } from "recharts";
import { Mic, Square, Volume2 } from "lucide-react";
import api, { msg, fmtDate } from "../utils/api";
import { ErrorBox, Empty } from "../components/ui.jsx";

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const CATS = [["HR", "HR / Introduction"], ["Technical", "Technical"], ["Behavioral", "Behavioral"], ["Situational", "Situational"]];

export default function Interview() {
  const [view, setView] = useState("setup"); const [sess, setSess] = useState(null); const [i, setI] = useState(0);
  const [answer, setAnswer] = useState(""); const [listening, setListening] = useState(false);
  const [fb, setFb] = useState({}); const [report, setReport] = useState(null); const [hist, setHist] = useState(null);
  const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  const rec = useRef(null); const base = useRef("");

  const loadHist = () => api.get("/interview/history").then(({ data }) => setHist(data)).catch(() => {});
  useEffect(() => { loadHist(); return () => { window.speechSynthesis?.cancel(); rec.current?.stop(); }; }, []);

  const speak = (t) => { if (!("speechSynthesis" in window)) return; window.speechSynthesis.cancel(); window.speechSynthesis.speak(new SpeechSynthesisUtterance(t)); };

  const start = async (category) => {
    setError("");
    try { const { data } = await api.post("/interview/start", { category }); setSess(data); setFb({}); setReport(null); setI(0); setAnswer(""); setView("run"); speak(data.questions[0].question); }
    catch (e) { setError(msg(e)); }
  };

  const toggleMic = () => {
    if (!SR) return setError("Speech recognition isn't supported in this browser. Use Chrome or Edge, or type your answer.");
    if (listening) return rec.current?.stop();
    const r = new SR(); r.lang = "en-IN"; r.continuous = true; r.interimResults = true; base.current = answer;
    r.onresult = (ev) => {
      let fin = "", interim = "";
      for (let k = ev.resultIndex; k < ev.results.length; k++) (ev.results[k].isFinal ? (fin += ev.results[k][0].transcript) : (interim += ev.results[k][0].transcript));
      if (fin) base.current = (base.current + " " + fin).trim();
      setAnswer((base.current + " " + interim).trim());
    };
    r.onerror = (e) => { setError(e.error === "not-allowed" ? "Microphone access is blocked. Allow it in your browser settings." : "Microphone error: " + e.error); setListening(false); };
    r.onend = () => setListening(false);
    rec.current = r; r.start(); setListening(true); setError("");
  };

  const submit = async () => {
    rec.current?.stop(); setError("");
    if (!answer.trim()) return setError("Record or type an answer first");
    setBusy(true);
    try {
      const q = sess.questions[i];
      const { data } = await api.post("/interview/submit", { session_id: sess.session_id, question_id: q.id, answer });
      setFb((f) => ({ ...f, [q.id]: data }));
      if (data.complete) { setReport(data.report); loadHist(); }
    } catch (e) { setError(msg(e)); } finally { setBusy(false); }
  };

  const go = (n) => { rec.current?.stop(); window.speechSynthesis?.cancel(); setI(n); setAnswer(""); setError(""); speak(sess.questions[n].question); };

  if (view === "setup") return (<>
    <div className="panel"><h2>Choose an interview type</h2><p className="muted">Five questions per round. Questions are read aloud and you can answer by voice or text.</p>
      <ErrorBox>{error}</ErrorBox>{CATS.map(([k, l]) => <button key={k} className="btn" style={{ marginRight: ".5rem", marginBottom: ".5rem" }} onClick={() => start(k)}>{l}</button>)}</div>
    <div className="grid2">
      <div className="panel"><h2>Score history</h2>{!hist || !hist.sessions.length ? <Empty>No completed interviews yet.</Empty> :
        <div className="chart"><ResponsiveContainer><LineChart data={hist.sessions.map((s) => ({ date: fmtDate(s.date), score: s.avg_score }))}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis dataKey="date" fontSize={11} /><YAxis domain={[0, 10]} fontSize={11} /><Tooltip /><Line dataKey="score" stroke="#4F46E5" strokeWidth={3} /></LineChart></ResponsiveContainer></div>}</div>
      <div className="panel"><h2>Average by category</h2>{!hist || !Object.keys(hist.by_category).length ? <Empty>Finish a round to see this.</Empty> :
        <div className="chart"><ResponsiveContainer><BarChart data={Object.entries(hist.by_category).map(([k, v]) => ({ date: k, score: v }))}><CartesianGrid strokeDasharray="3 3" stroke="var(--line)" /><XAxis dataKey="date" fontSize={11} /><YAxis domain={[0, 10]} fontSize={11} /><Tooltip /><RBar dataKey="score" fill="#7C3AED" radius={[6, 6, 0, 0]} /></BarChart></ResponsiveContainer></div>}</div>
    </div></>);

  if (view === "report" && report) return (
    <div className="panel"><h2>{report.category} interview report</h2>
      <div className="between"><b style={{ fontSize: "2rem" }}>{report.avg_score}/10</b><span className="chip">{report.verdict}</span></div>
      <h3>Per question</h3><ul className="clean">{report.per_question.map((p) => <li key={p.question}>{p.question} <b>({p.score}/10)</b></li>)}</ul>
      {report.top_improvements.length > 0 && <><h3>Focus areas</h3><ul className="clean">{report.top_improvements.map((t) => <li key={t}>{t}</li>)}</ul></>}
      <button className="btn" onClick={() => { setView("setup"); loadHist(); }}>Back to interviews</button></div>);

  const q = sess.questions[i], f = fb[q.id], last = i === sess.questions.length - 1;
  return (
    <div className="panel">
      <span className="chip">{q.category}</span><span className="muted">Question {i + 1} of {sess.questions.length}</span>
      <h2 style={{ marginTop: ".5rem" }}>{q.question}</h2>
      <button className="btn outline small" onClick={() => speak(q.question)}><Volume2 size={14} /> Read aloud</button>
      <label htmlFor="ans">Your answer {listening && <span className="chip bad">Recording...</span>}</label>
      <textarea id="ans" rows={6} value={answer} onChange={(e) => { setAnswer(e.target.value); base.current = e.target.value; }} placeholder="Speak with the mic or type here" />
      <ErrorBox>{error}</ErrorBox>
      <div style={{ display: "flex", gap: ".5rem", flexWrap: "wrap", marginTop: ".6rem" }}>
        <button className={"btn" + (listening ? " mic" : "")} onClick={toggleMic}>{listening ? <><Square size={14} /> Stop</> : <><Mic size={14} /> Record answer</>}</button>
        <button className="btn" onClick={submit} disabled={busy}>{busy ? "Scoring..." : "Get feedback"}</button></div>
      {f && <div className="success" style={{ marginTop: "1rem" }}><b>Score: {f.score}/{f.out_of}</b>
        {f.star && <div style={{ margin: ".4rem 0" }}>{Object.entries(f.star).map(([k, v]) => <span key={k} className={"chip " + (v ? "ok" : "bad")}>{k}</span>)}</div>}
        {f.strengths.length > 0 && <><div><b>Strengths</b></div><ul className="clean">{f.strengths.map((s) => <li key={s}>{s}</li>)}</ul></>}
        {f.improvements.length > 0 && <><div><b>To improve</b></div><ul className="clean">{f.improvements.map((s) => <li key={s}>{s}</li>)}</ul></>}</div>}
      <div className="between" style={{ marginTop: "1rem" }}>
        <button className="btn outline" disabled={i === 0} onClick={() => go(i - 1)}>Previous</button>
        {last ? <button className="btn" disabled={!report} onClick={() => setView("report")}>{report ? "See final report" : "Answer all questions to finish"}</button>
          : <button className="btn" onClick={() => go(i + 1)}>Next question</button>}
      </div>
    </div>
  );
}
