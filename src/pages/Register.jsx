import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import api, { msg } from "../utils/api";
import { useAuth } from "../context/AuthContext.jsx";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox } from "../components/ui.jsx";

const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/, MOBILE = /^[6-9]\d{9}$/;
export function pwProblem(p) {
  if (p.length < 8) return "Password must be at least 8 characters";
  if (!/[A-Z]/.test(p)) return "Password needs an uppercase letter";
  if (!/[a-z]/.test(p)) return "Password needs a lowercase letter";
  if (!/\d/.test(p)) return "Password needs a number";
  if (!/[^A-Za-z0-9]/.test(p)) return "Password needs a special character";
  return "";
}

export default function Register() {
  const nav = useNavigate(); const { state } = useLocation(); const { login } = useAuth(); const toast = useToast();
  const [step, setStep] = useState(state?.step || "form");
  const [f, setF] = useState({ name: "", email: state?.email || "", mobile: "", password: "" });
  const [otp, setOtp] = useState(""); const [demo, setDemo] = useState("");
  const [error, setError] = useState(""); const [loading, setLoading] = useState(false);
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault(); setError("");
    if (f.name.trim().length < 2) return setError("Enter your full name");
    if (!EMAIL.test(f.email)) return setError("Enter a valid email address");
    if (!MOBILE.test(f.mobile)) return setError("Mobile must be 10 digits starting with 6, 7, 8 or 9");
    const p = pwProblem(f.password); if (p) return setError(p);
    setLoading(true);
    try { const { data } = await api.post("/register", f); setDemo(data.dev_otp || ""); setStep("otp"); }
    catch (err) { setError(msg(err)); } finally { setLoading(false); }
  };

  const verify = async (e) => {
    e.preventDefault(); setError("");
    if (!/^\d{6}$/.test(otp)) return setError("Enter the 6-digit code");
    setLoading(true);
    try { const { data } = await api.post("/verify-otp", { email: f.email, otp }); login(data); toast("Email verified. Welcome!"); nav("/profile"); }
    catch (err) { setError(msg(err)); } finally { setLoading(false); }
  };

  const resend = async () => {
    setError("");
    try { const { data } = await api.post("/send-otp", { email: f.email, purpose: "verify" }); setDemo(data.dev_otp || ""); toast("A new code was sent"); }
    catch (err) { setError(msg(err)); }
  };

  if (step === "otp") return (
    <div className="auth-bg"><form className="auth-card" onSubmit={verify}>
      <h1>Verify your email</h1><p className="muted">We sent a 6-digit code to <b>{f.email}</b>. It expires in 10 minutes.</p>
      {demo && <div className="demo">Demo mode: your code is <b>{demo}</b>. It is also printed in the backend terminal.</div>}
      <ErrorBox>{error}</ErrorBox>
      <label htmlFor="o">Verification code</label>
      <input id="o" inputMode="numeric" maxLength={6} value={otp} onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))} autoFocus />
      <button className="btn block" disabled={loading}>{loading ? "Verifying..." : "Verify and continue"}</button>
      <p className="muted" style={{ textAlign: "center" }}>Didn't get it? <a href="#" onClick={(e) => { e.preventDefault(); resend(); }}>Resend code</a></p>
    </form></div>
  );

  return (
    <div className="auth-bg"><form className="auth-card" onSubmit={submit}>
      <h1>Create your account</h1><p className="muted">Takes under a minute.</p>
      <ErrorBox>{error}</ErrorBox>
      <label htmlFor="n">Full name</label><input id="n" value={f.name} onChange={set("name")} />
      <label htmlFor="e">Email</label><input id="e" type="email" value={f.email} onChange={set("email")} />
      <label htmlFor="m">Mobile number</label><input id="m" inputMode="numeric" maxLength={10} value={f.mobile} onChange={set("mobile")} />
      <label htmlFor="p">Password</label><input id="p" type="password" value={f.password} onChange={set("password")} autoComplete="new-password" />
      <small className="muted">8+ characters with upper, lower, number and special character.</small>
      <button className="btn block" disabled={loading}>{loading ? "Creating..." : "Create account"}</button>
      <p className="muted" style={{ textAlign: "center" }}>Have an account? <Link to="/login">Log in</Link></p>
    </form></div>
  );
}
