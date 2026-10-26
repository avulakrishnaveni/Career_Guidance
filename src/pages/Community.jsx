import { useEffect, useState } from "react";
import { ChevronUp, MessageSquare } from "lucide-react";
import api, { msg, ago } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox, Skeleton, Empty } from "../components/ui.jsx";

function Post({ p, onVote }) {
  const [open, setOpen] = useState(false); const [cs, setCs] = useState(null); const [text, setText] = useState(""); const [error, setError] = useState("");
  const load = () => api.get("/forum/comments", { params: { post_id: p.id } }).then(({ data }) => setCs(data)).catch((e) => setError(msg(e)));
  const send = async (e) => { e.preventDefault(); setError(""); try { await api.post("/forum/comments", { post_id: p.id, body: text }); setText(""); load(); } catch (er) { setError(msg(er)); } };
  return (
    <div className="panel"><div style={{ display: "flex", gap: ".8rem" }}>
      <button className={"choice" + (p.voted ? " on" : "")} style={{ margin: 0, textAlign: "center", padding: ".3rem .6rem" }} onClick={() => onVote(p)} aria-label="Upvote"><ChevronUp size={16} /><br />{p.upvotes}</button>
      <div style={{ flex: 1 }}><h3 style={{ margin: 0 }}>{p.title}</h3><span className="muted" style={{ fontSize: ".82rem" }}>{p.author} | {p.domain} | {ago(p.created_at + "Z")}</span>
        <p>{p.body}</p>
        <button className="btn outline small" onClick={() => { setOpen(!open); if (!cs) load(); }}><MessageSquare size={13} /> {p.comments} comments</button>
        {open && <div style={{ marginTop: ".6rem" }}>{(cs || []).map((c) => <p key={c.id} style={{ margin: ".3rem 0" }}><b>{c.author}:</b> {c.body}</p>)}
          <ErrorBox>{error}</ErrorBox><form className="send" style={{ padding: 0 }} onSubmit={send}><input value={text} onChange={(e) => setText(e.target.value)} placeholder="Write a comment" aria-label="Comment" /><button className="btn small">Post</button></form></div>}
      </div></div></div>
  );
}

function Forum() {
  const toast = useToast();
  const [domains, setDomains] = useState([]); const [posts, setPosts] = useState(null); const [dom, setDom] = useState("");
  const [form, setForm] = useState({ domain: "", title: "", body: "" }); const [error, setError] = useState("");
  const load = () => api.get("/forum/posts", { params: dom ? { domain: dom } : {} }).then(({ data }) => { setPosts(data.posts); setDomains(data.domains); }).catch((e) => setError(msg(e)));
  useEffect(() => { load(); }, [dom]);
  const create = async (e) => { e.preventDefault(); setError(""); try { await api.post("/forum/posts", form); setForm({ domain: form.domain, title: "", body: "" }); toast("Posted"); load(); } catch (er) { setError(msg(er)); } };
  const vote = async (p) => { try { const { data } = await api.post(`/forum/posts/${p.id}/upvote`); setPosts((l) => l.map((x) => x.id === p.id ? { ...x, upvotes: data.upvotes, voted: data.voted } : x)); } catch (e) { setError(msg(e)); } };
  return (<>
    <form className="panel" onSubmit={create}><h2>Start a discussion</h2><ErrorBox>{error}</ErrorBox>
      <div className="row"><div><label>Domain</label><select value={form.domain} onChange={(e) => setForm({ ...form, domain: e.target.value })}><option value="">Select</option>{domains.map((d) => <option key={d}>{d}</option>)}</select></div>
        <div><label>Title</label><input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} maxLength={200} /></div></div>
      <label>Details</label><textarea rows={3} value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} maxLength={3000} /><button className="btn block">Post</button></form>
    <select value={dom} onChange={(e) => setDom(e.target.value)} style={{ width: "auto", marginBottom: "1rem" }} aria-label="Filter by domain"><option value="">All domains</option>{domains.map((d) => <option key={d}>{d}</option>)}</select>
    {!posts ? <Skeleton h={100} n={2} /> : posts.length === 0 ? <Empty>No posts yet. Start the first discussion.</Empty> : posts.map((p) => <Post key={p.id} p={p} onVote={vote} />)}
  </>);
}

function Mentors() {
  const toast = useToast(); const [m, setM] = useState(null);
  useEffect(() => { api.get("/mentors").then(({ data }) => setM(data)).catch(() => setM([])); }, []);
  const connect = async (x) => { try { const { data } = await api.post("/mentors/connect", { mentor_id: x.id }); toast(data.message); } catch (e) { toast(msg(e), "error"); } };
  return !m ? <Skeleton h={120} n={2} /> : <div className="grid">{m.map((x) => <div className="panel" key={x.id}><h3>{x.name}</h3><p className="muted" style={{ margin: 0 }}>{x.title}, {x.company}</p><span className="chip">{x.domain}</span><span className="chip">{x.experience}</span><p>{x.bio}</p><button className="btn small" onClick={() => connect(x)}>Connect</button></div>)}</div>;
}

function Events() {
  const toast = useToast(); const [e, setE] = useState(null);
  useEffect(() => { api.get("/events").then(({ data }) => setE(data)).catch(() => setE([])); }, []);
  const reg = async (x) => { try { const { data } = await api.post("/events/register", { event_id: x.id }); toast(data.message); } catch (er) { toast(msg(er), "error"); } };
  return !e ? <Skeleton h={100} n={2} /> : <div className="grid">{e.map((x) => <div className="panel" key={x.id}><h3>{x.title}</h3><span className="chip">{x.mode}</span><p className="muted" style={{ margin: ".2rem 0" }}>{x.date}</p><p>{x.description}</p><button className="btn small" onClick={() => reg(x)}>Register</button></div>)}</div>;
}

export default function Community() {
  const [tab, setTab] = useState("forum");
  return (<><div className="tabs">{[["forum", "Discussion forum"], ["mentors", "Mentors"], ["events", "Events & webinars"]].map(([k, l]) => <button key={k} className={"tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>)}</div>
    {tab === "forum" ? <Forum /> : tab === "mentors" ? <Mentors /> : <Events />}</>);
}
