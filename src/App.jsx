import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Forgot from "./pages/Forgot.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Profile from "./pages/Profile.jsx";
import Career from "./pages/Career.jsx";
import Learning from "./pages/Learning.jsx";
import Resume from "./pages/Resume.jsx";
import Jobs from "./pages/Jobs.jsx";
import Interview from "./pages/Interview.jsx";
import Coding from "./pages/Coding.jsx";
import Report from "./pages/Report.jsx";
import Community from "./pages/Community.jsx";
import Notifications from "./pages/Notifications.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<Forgot />} />
      <Route element={<Layout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/career" element={<Career />} />
        <Route path="/learning" element={<Learning />} />
        <Route path="/resume" element={<Resume />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/coding" element={<Coding />} />
        <Route path="/report" element={<Report />} />
        <Route path="/community" element={<Community />} />
        <Route path="/notifications" element={<Notifications />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
