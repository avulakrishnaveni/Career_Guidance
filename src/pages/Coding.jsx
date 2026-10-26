import { useEffect, useState } from "react";
import { CheckCircle2, Flame, Lightbulb, Trophy } from "lucide-react";
import api, { msg } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox, Skeleton, Empty } from "../components/ui.jsx";

export default function Coding() {
  const toast = useToast();
  const [tab, setTab] = useState("practice"); const [list, setList] = useState(null); const [domain, setDomain] = useState("");
  const [diff, setDiff] = useState(""); const [cur, setCur] = useState(null); const [code, setCode] = useState("");
  const [res, setRes] = useState(null); const [hints, setHints] = useState([]); const [sol, setSol] = useState("");
  const [board, setBoard] = useState(null); const [error, setError] = useState(""); const [busy, setBusy] = useState(false);

  const load = (keep) => api.get("/coding/challenges").then(({ data }) => { setList(data.challenges); setDomain(data.domain); if (!keep && data.challenges[0]) pick(data.challenges[0]); }).catch((e) => setError(msg(e)));
  const loadBoard = () => api.get("/coding/leaderboard").then(({ data }) => setBoard(data)).catch((e) => setError(msg(e)));
  useEffect(() => { load(); loadBoard(); }, []);
  const pick = (c) => { setCur(c); setCode(c.starter_code); setRes(null); setHints([]); setSol(""); setError(""); };

  const run = async () => {
    setBusy(true); setError(""); setRes(null);
    try {
      const { data } = await api.post("/coding/submit", { challenge_id: cur.id, code }); setRes(data);
      if (data.passed) { toast(data.points_earned ? `Solved! +${data.points_earned} points` : "All tests passed"); load(true); loadBoard(); }
    } catch (e) { setError(msg(e)); } finally { setBusy(false); }
  };
  const nextHint = async () => {
    try { const { data } = await api.get(`/coding/challenges/${cur.id}/hint`, { params: { n: hints.length + 1 } }); setHints([...hints, data.hint]); }
    catch (e) { setError(msg(e)); }
  };
  const showSol = async () => {
    if (!window.confirm("Reveal the solution? Try a hint first.")) return;
    try { const { data } = await api.get(`/coding/challenges/${cur.id}/solution`); setSol(data.solution); } catch (e) { setError(msg(e)); }
  };
  const onKey = (e) => {
    if (e.key !== "Tab") return;
    e.preventDefault(); const s = e.target.selectionStart, en = e.target.selectionEnd;
    setCode(code.slice(0, s) + "    " + code.slice(en)); requestAnimationFrame(() => { e.target.selectionStart = e.target.selectionEnd = s + 4; });
  };

  if (!list) return error ? <ErrorBox>{error}</ErrorBox> : <Skeleton h={200} n={2} />;
  const shown = list.filter((c) => !diff || c.difficulty === diff);

  return (<>
    <div className="between"><div className="tabs">{[["practice", "Practice"], ["board", "Leaderboard"]].map(([k, l]) => <button key={k} className={"tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>)}</div>
      {board && <span className="chip"><Flame size={12} style={{ verticalAlign: "-2px" }} /> {board.streak}-day streak{board.me ? ` | ${board.me.points} pts | rank #${board.me.rank}` : ""}</span>}</div>

    {tab === "board" && <div className="panel"><h2><Trophy size={18} style={{ verticalAlign: "-3px" }} /> Top solvers</h2>
      {!board || !board.leaderboard.length ? <Empty>Nobody has solved a challenge yet. Be the first!</Empty> : board.leaderboard.map((r) => (
        <div key={r.rank} className="between" style={{ padding: ".5rem 0", borderBottom: "1px solid var(--line)", fontWeight: r.me ? 700 : 400 }}>
          <span>#{r.rank} {r.name} {r.me && <span className="chip">You</span>}</span><span>{r.points} pts | {r.solved} solved</span></div>))}</div>}

    {tab === "practice" && <div className="split">
      <div className="panel">
        <div className="between"><h3>Problems{domain ? ` (${domain})` : ""}</h3>
          <select value={diff} onChange={(e) => setDiff(e.target.value)} style={{ width: "auto" }} aria-label="Difficulty"><option value="">All levels</option><option>easy</option><option>medium</option><option>hard</option></select></div>
        {shown.map((c) => <button key={c.id} className={"choice" + (cur?.id === c.id ? " on" : "")} style={{ display: "flex", width: "100%", justifyContent: "space-between", margin: "0 0 .4rem" }} onClick={() => pick(c)}>
          <span>{c.solved && <CheckCircle2 size={14} color="#10b981" style={{ verticalAlign: "-2px" }} />} {c.title}</span><span className={"chip " + c.difficulty}>{c.difficulty} | {c.points}</span></button>)}
        {cur && <><h3 style={{ marginTop: "1rem" }}>{cur.title}</h3><p>{cur.description}</p><b>Examples</b>
          <ul className="clean">{cur.examples.map((t, k) => <li key={k}><code>solution({t.input.map((x) => JSON.stringify(x)).join(", ")})</code> returns <code>{JSON.stringify(t.expected)}</code></li>)}</ul>
          <p className="muted" style={{ fontSize: ".85rem" }}>Write a Python function named <code>solution</code>. Some tests are hidden. Imports of os, sys and similar are blocked.</p></>}
      </div>
      <div className="panel">
        <ErrorBox>{error}</ErrorBox>
        <textarea className="code" value={code} onChange={(e) => setCode(e.target.value)} onKeyDown={onKey} spellCheck={false} aria-label="Code editor" />
        <div style={{ display: "flex", gap: ".5rem", flexWrap: "wrap", marginTop: ".6rem" }}>
          <button className="btn" onClick={run} disabled={busy || !cur}>{busy ? "Running..." : "Run tests"}</button>
          <button className="btn outline" onClick={nextHint} disabled={!cur || hints.length >= (cur?.hint_count || 0)}><Lightbulb size={14} /> Hint ({hints.length}/{cur?.hint_count || 0})</button>
          <button className="btn outline" onClick={showSol} disabled={!cur}>Show solution</button></div>
        {hints.map((h, k) => <div key={k} className="demo">Hint {k + 1}: {h}</div>)}
        {sol && <pre className="demo" style={{ overflowX: "auto" }}>{sol}</pre>}
        {res && <div style={{ marginTop: "1rem" }}>
          {res.error && <ErrorBox>{res.error}</ErrorBox>}
          {res.results.length > 0 && <><h3 className={res.passed ? "pass" : "fail"}>{res.passed ? "All tests passed" : `${res.passed_count} of ${res.total} tests passed`}</h3>
            {res.results.map((r, k) => <p key={k} style={{ margin: ".2rem 0" }}><span className={r.ok ? "pass" : "fail"}>{r.ok ? "Pass" : "Fail"}</span> | {r.hidden ? `Hidden test ${k + 1}` : `Test ${k + 1}`}
              {!r.ok && !r.hidden && <> | got <code>{r.got}</code>, expected <code>{JSON.stringify(r.expected)}</code></>}{!r.ok && r.hidden && <> | got <code>{r.got}</code></>}</p>)}</>}
        </div>}
      </div>
    </div>}
  </>);
}
