import { useEffect, useRef, useState } from "react";
import { MessageCircle, X, Send, Trash2 } from "lucide-react";
import api, { msg } from "../utils/api";

const CHIPS = ["Resume tips", "Interview prep", "Find jobs", "Coding practice", "Career roadmap"];

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [msgs, setMsgs] = useState([]); const [text, setText] = useState("");
  const [busy, setBusy] = useState(false); const [error, setError] = useState("");
  const end = useRef(null);

  useEffect(() => { if (open && msgs.length === 0) api.get("/chat/history").then(({ data }) => setMsgs(data)).catch((e) => setError(msg(e))); }, [open]);
  useEffect(() => { end.current?.scrollIntoView({ behavior: "smooth" }); }, [msgs, busy, open]);

  const send = async (t) => {
    t = (t ?? text).trim(); if (!t || busy) return;
    setText(""); setError(""); setBusy(true);
    setMsgs((m) => [...m, { role: "user", text: t }]);
    try { const { data } = await api.post("/chat", { message: t }); setMsgs((m) => [...m, { role: "bot", text: data.reply }]); }
    catch (e) { setError(msg(e)); } finally { setBusy(false); }
  };
  const clear = async () => { try { await api.delete("/chat/history"); setMsgs([]); } catch (e) { setError(msg(e)); } };

  return (
    <>
      {!open && <button className="fab" onClick={() => setOpen(true)} aria-label="Open CareerMate chat"><MessageCircle size={24} /></button>}
      {open && (
        <section className="chatwin" aria-label="CareerMate chat">
          <div className="chat-head"><b>CareerMate</b><span style={{ flex: 1 }} />
            <button className="icon-btn light" onClick={clear} aria-label="Clear history"><Trash2 size={16} /></button>
            <button className="icon-btn light" onClick={() => setOpen(false)} aria-label="Close chat"><X size={18} /></button></div>
          <div className="chatbox" aria-live="polite">
            {msgs.length === 0 && <p className="muted">Hi, I'm CareerMate. Ask me about careers, resumes, jobs, interviews or coding.</p>}
            {msgs.map((m, i) => <div key={i} className={"bubble " + m.role}>{m.text}</div>)}
            {busy && <div className="bubble bot typing"><i /><i /><i /></div>}
            <div ref={end} />
          </div>
          {error && <div className="error" style={{ margin: "0 .6rem" }}>{error}</div>}
          <div className="chips">{CHIPS.map((c) => <button key={c} className="chip btn-chip" onClick={() => send(c)}>{c}</button>)}</div>
          <form className="send" onSubmit={(e) => { e.preventDefault(); send(); }}>
            <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Type your question" aria-label="Message" maxLength={500} />
            <button className="btn" disabled={busy} aria-label="Send"><Send size={16} /></button>
          </form>
        </section>
      )}
    </>
  );
}
