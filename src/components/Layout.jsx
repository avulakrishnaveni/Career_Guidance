import { useEffect, useState } from "react";
import { NavLink, Outlet, Navigate, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { LayoutDashboard, UserRound, Compass, GraduationCap, FileText, Briefcase, Mic, Code2, Gauge, Users, Bell, Sun, Moon, LogOut, Menu, X } from "lucide-react";
import api from "../utils/api";
import { useAuth } from "../context/AuthContext.jsx";
import { useTheme } from "../context/ThemeContext.jsx";
import ChatWidget from "./ChatWidget.jsx";

const NAV = [
  ["/dashboard", "Dashboard", LayoutDashboard], ["/report", "Readiness report", Gauge], ["/profile", "Profile", UserRound],
  ["/career", "Career path", Compass], ["/learning", "Learning path", GraduationCap], ["/resume", "Resume analyzer", FileText],
  ["/jobs", "Jobs", Briefcase], ["/interview", "Mock interview", Mic], ["/coding", "Coding arena", Code2], ["/community", "Community", Users],
];

export default function Layout() {
  const { user, logout } = useAuth();
  const { theme, toggle } = useTheme();
  const loc = useLocation(); const nav = useNavigate();
  const [open, setOpen] = useState(false);
  const [unread, setUnread] = useState(0);

  useEffect(() => { setOpen(false); }, [loc.pathname]);
  useEffect(() => { if (user) api.get("/notifications").then(({ data }) => setUnread(data.unread)).catch(() => {}); }, [loc.pathname, user]);

  if (!localStorage.getItem("token")) return <Navigate to="/login" replace />;
  const out = () => { logout(); nav("/login"); };

  return (
    <div className="app">
      <aside className={"side" + (open ? " open" : "")}>
        <div className="side-head"><span className="brand">CareerVerse</span><button className="icon-btn only-mobile" onClick={() => setOpen(false)} aria-label="Close menu"><X size={20} /></button></div>
        <nav>{NAV.map(([to, label, Icon]) => <NavLink key={to} to={to} className={({ isActive }) => "nav" + (isActive ? " active" : "")}><Icon size={18} />{label}</NavLink>)}</nav>
      </aside>
      {open && <div className="scrim" onClick={() => setOpen(false)} />}
      <div className="main">
        <header className="top">
          <button className="icon-btn only-mobile" onClick={() => setOpen(true)} aria-label="Open menu"><Menu size={22} /></button>
          <div style={{ flex: 1 }} />
          <button className="icon-btn" onClick={toggle} aria-label="Toggle dark mode">{theme === "dark" ? <Sun size={19} /> : <Moon size={19} />}</button>
          <NavLink to="/notifications" className="icon-btn bell" aria-label={`Notifications, ${unread} unread`}><Bell size={19} />{unread > 0 && <span className="dot">{unread > 9 ? "9+" : unread}</span>}</NavLink>
          <span className="who">{user?.name?.split(" ")[0]}</span>
          <button className="icon-btn" onClick={out} aria-label="Log out"><LogOut size={19} /></button>
        </header>
        <motion.main key={loc.pathname} className="page" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.22 }}>
          <Outlet />
        </motion.main>
      </div>
      <ChatWidget />
    </div>
  );
}
