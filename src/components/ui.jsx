export function ScoreRing({ value = 0, color = "#4F46E5", size = 120, label }) {
  const r = 46, c = 2 * Math.PI * r, off = c * (1 - Math.min(100, Math.max(0, value)) / 100);
  return (
    <svg width={size} height={size} viewBox="0 0 120 120" role="img" aria-label={`${label || "Score"} ${value} out of 100`}>
      <circle cx="60" cy="60" r={r} fill="none" stroke="var(--line)" strokeWidth="11" />
      <circle cx="60" cy="60" r={r} fill="none" stroke={color} strokeWidth="11" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={off} transform="rotate(-90 60 60)" style={{ transition: "stroke-dashoffset .8s" }} />
      <text x="60" y="64" textAnchor="middle" fontSize="28" fontWeight="800" fill="var(--ink)">{value}</text>
      {label && <text x="60" y="82" textAnchor="middle" fontSize="10" fill="var(--muted)">{label}</text>}
    </svg>
  );
}

export const Skeleton = ({ h = 90, n = 1 }) => (
  <>{Array.from({ length: n }).map((_, i) => <div key={i} className="skeleton" style={{ height: h }} />)}</>
);

export const Bar = ({ value, color }) => <div className="bar"><div style={{ width: Math.min(100, value) + "%", background: color }} /></div>;
export const Empty = ({ children }) => <p className="muted empty">{children}</p>;
export const ErrorBox = ({ children }) => children ? <div className="error" role="alert">{children}</div> : null;
