import { useEffect, useState } from "react";
import api, { msg, ago } from "../utils/api";
import { ErrorBox, Skeleton, Empty } from "../components/ui.jsx";

export default function Notifications() {
  const [d, setD] = useState(null); const [error, setError] = useState("");
  const load = () => api.get("/notifications").then(({ data }) => setD(data)).catch((e) => setError(msg(e)));
  useEffect(() => { load(); }, []);
  const readAll = async () => { try { await api.post("/notifications/read", {}); load(); } catch (e) { setError(msg(e)); } };
  if (!d) return error ? <ErrorBox>{error}</ErrorBox> : <Skeleton h={80} n={3} />;
  return (<div className="panel"><div className="between"><h2>Notifications ({d.unread} unread)</h2><button className="btn outline small" onClick={readAll} disabled={!d.unread}>Mark all as read</button></div>
    <ErrorBox>{error}</ErrorBox>
    {d.items.length === 0 ? <Empty>You're all caught up.</Empty> : d.items.map((n) => (
      <div key={n.id} style={{ padding: ".7rem 0", borderBottom: "1px solid var(--line)", opacity: n.read ? .65 : 1 }}>
        <b>{n.title}</b>{!n.read && <span className="chip" style={{ marginLeft: ".5rem" }}>New</span>}<div>{n.message}</div><div className="muted" style={{ fontSize: ".8rem" }}>{ago(n.created_at + "Z")}</div></div>))}</div>);
}
