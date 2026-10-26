import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { msg } from "../utils/api";
import { useToast } from "../context/ToastContext.jsx";
import { ErrorBox } from "./../components/ui.jsx";
import { pwProblem } from "./Register.jsx";

export default function Forgot() {
  const nav = useNavigate(); const toast = useToast();
  const [step, setStep] = useState(1); const [email, setEmail] = useState("");
  const [otp, setOtp] = useState(""); const [pw, setPw] = useState(""); const [demo, setDemo] = useState("");
  const [error, setError] = useState(""); const [loading, setLoading] = useState(false);

  const sendCode = async (e) => {
    e.preventDefault(); setError("");
    if (!email) return setError("Enter your email");
    setLoading(true);
    try { const { data } = await api.post("/forgot-password", { email }); setDemo(data.dev_otp || ""); setStep(2); }
    catch (err) { setError(msg(err)); } finally { setLoading(false); }
  };
  const reset = async (e) => {
    e.preventDefault(); setError("");
    if (!/^\d{6}$/.test(otp)) return setError("Enter the 6-digit code");
    const p = pwProblem(pw); if (p) return setError(p);
    setLoading(true);
    try { await api.post("/reset-password", { email, otp, password: pw }); toast("Password updated. Log in now."); nav("/login"); }
    catch (err) { setError(msg(err)); } finally { setLoading(false); }
  };

  return (
    <div className="auth-bg"><form className="auth-card" onSubmit={step === 1 ? sendCode : reset}>
      <h1>Reset password</h1>
      <p className="muted">{step === 1 ? "Enter your email and we'll send a code." : `Enter the code sent to ${email} and choose a new password.`}</p>
      {step === 2 && demo && <div className="demo">Demo mode: your code is <b>{demo}</b>.</div>}
      <ErrorBox>{error}</ErrorBox>
      {step === 1 ? (<><label htmlFor="e">Email</label><input id="e" type="email" value={email} onChange={(e) => setEmail(e.target.value)} /></>) : (<>
        <label htmlFor="o">Code</label><input id="o" inputMode="numeric" maxLength={6} value={otp} onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))} />
        <label htmlFor="p">New password</label><input id="p" type="password" value={pw} onChange={(e) => setPw(e.target.value)} autoComplete="new-password" /></>)}
      <button className="btn block" disabled={loading}>{loading ? "Please wait..." : step === 1 ? "Send code" : "Update password"}</button>
      <p className="muted" style={{ textAlign: "center" }}><Link to="/login">Back to log in</Link></p>
    </form></div>
  );
}
