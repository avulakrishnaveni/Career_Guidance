import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { msg } from "../utils/api";
import { useAuth } from "../context/AuthContext.jsx";
import { ErrorBox } from "../components/ui.jsx";

export default function Login() {
  const nav = useNavigate(); const { login } = useAuth();
  const [f, setF] = useState({ email: "", password: "" });
  const [error, setError] = useState(""); const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault(); setError("");
    if (!f.email || !f.password) return setError("Enter your email and password");
    setLoading(true);
    try { const { data } = await api.post("/login", f); login(data); nav("/dashboard"); }
    catch (err) {
      if (err.response?.data?.needs_verification) {
        try { await api.post("/send-otp", { email: f.email, purpose: "verify" }); } catch {}
        return nav("/register", { state: { email: f.email, step: "otp" } });
      }
      setError(msg(err));
    } finally { setLoading(false); }
  };

  return (
    <div className="auth-bg"><form className="auth-card" onSubmit={submit}>
      <h1>Welcome back</h1><p className="muted">Log in to continue with CareerVerse.</p>
      <ErrorBox>{error}</ErrorBox>
      <label htmlFor="e">Email</label><input id="e" type="email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} autoComplete="email" />
      <label htmlFor="p">Password</label><input id="p" type="password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} autoComplete="current-password" />
      <p style={{ textAlign: "right", margin: ".4rem 0 0" }}><Link to="/forgot-password">Forgot password?</Link></p>
      <button className="btn block" disabled={loading}>{loading ? "Logging in..." : "Log in"}</button>
      <p className="muted" style={{ textAlign: "center" }}>New here? <Link to="/register">Create an account</Link></p>
    </form></div>
  );
}
