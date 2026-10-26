import axios from "axios";

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api" });

api.interceptors.request.use((cfg) => {
  const t = localStorage.getItem("token");
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

api.interceptors.response.use((r) => r, (e) => {
  if (e.response?.status === 401 && localStorage.getItem("token")) {
    localStorage.removeItem("token"); localStorage.removeItem("user");
    window.location.href = "/login";
  }
  return Promise.reject(e);
});

export const msg = (e) => e.response?.data?.error || "Could not reach the server. Check that the backend is running.";
export const fmtDate = (s) => new Date(s).toLocaleDateString(undefined, { day: "numeric", month: "short" });
export const ago = (s) => {
  const m = Math.round((Date.now() - new Date(s).getTime()) / 60000);
  if (m < 1) return "just now"; if (m < 60) return `${m}m ago`;
  if (m < 1440) return `${Math.round(m / 60)}h ago`; return `${Math.round(m / 1440)}d ago`;
};
export default api;
