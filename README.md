# CareerVerse: AI-Powered Career Guidance & Development Portal

React (Vite) + Flask + SQLite + JWT. Includes OTP email verification, career roadmaps, resume analysis, job matching,
voice mock interviews, a coding arena, learning tracking, community, and a **Job Readiness Report with PDF download**.

## Folder structure
```
careerverse/
├── backend/
│   ├── app.py                  # app factory, JWT/error handlers, seeding
│   ├── extensions.py           # db, jwt
│   ├── models.py               # all tables
│   ├── data.py, seed.py        # domains, modules, jobs, challenges, interview bank, mentors, events
│   ├── routes/                 # auth, profile, career (+learning/progress), chat, resume, jobs,
│   │                           # interview, coding, report (+PDF), dashboard, community (+notifications)
│   ├── utils/                  # helpers, otp, chatbot, resume_analyzer, interview_eval, sandbox, readiness
│   ├── requirements.txt, .env, .env.example
└── frontend/
    ├── package.json, vite.config.js, index.html, .env
    └── src/ main.jsx, App.jsx, styles.css
            components/ Layout, ChatWidget, ui
            context/    AuthContext, ThemeContext, ToastContext
            pages/      Login, Register (OTP), Forgot, Dashboard, Profile, Career, Learning, Resume,
                        Jobs, Interview, Coding, Report, Community, Notifications
            utils/      api.js
```

## Run in VS Code (two terminals)
**Backend** (needs Python 3.10+):
```
cd backend
python -m venv venv
venv\Scripts\activate            (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
**Frontend** (needs Node.js 18+):
```
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. The database and seed data (jobs, challenges, learning modules) are created on first start.

## OTP in demo mode
Registration and password reset print the 6-digit code in the **backend terminal**. With `SHOW_OTP_IN_RESPONSE=true`
(default in `.env`) the code is also shown on screen. For production set it to `false`, fill the `MAIL_*` values in `.env`,
and Flask-Mail sends real emails (see `utils/otp.py`).

## Suggested test flow
Register → verify OTP → Profile (add 3+ skills) → Career path → Resume upload → Jobs (match %) → Mock interview →
Coding (solve a problem) → Learning (tick modules) → Dashboard → Readiness Report → Download PDF.

## Job Readiness Score (utils/readiness.py)
Profile 15% + Resume 20% + Interview 20% + Coding 15% + Learning 15% + Skill match 15%.
Levels: Beginner 0-40, Developing 41-60, Job-Ready 61-80, Interview-Ready 81-100.
Every action calls `log_activity`, which refreshes today's snapshot, so the trend chart and dashboard stay current.

## API summary (all under /api, JWT required except auth)
- Auth: register, send-otp, verify-otp, login, forgot-password, reset-password
- Profile: GET/POST/PUT /profile
- Career: /career/domains, /career/select, /career/my-path, /career/roadmap
- Chat: POST /chat, GET/DELETE /chat/history
- Resume: POST /resume/upload, GET /resume/history
- Jobs: GET /jobs (filters), POST /jobs/save, POST /jobs/apply, GET /jobs/applications
- Interview: GET /interview/questions, POST /interview/start, POST /interview/submit, GET /interview/history
- Coding: GET /coding/challenges, GET /coding/challenges/<id>/hint, GET /coding/challenges/<id>/solution, POST /coding/submit, GET /coding/leaderboard
- Learning: GET /learning/roadmap, GET /progress, POST /progress/update
- Report: GET /report/readiness, GET /report/readiness/pdf
- Dashboard: GET /dashboard/stats
- Community: /forum/posts, /forum/posts/<id>/upvote, /forum/comments, /mentors, /mentors/connect, /events, /events/register
- Notifications: GET /notifications, POST /notifications/read

## Notes and limits
- Chatbot, resume scoring and interview feedback are rule-based by design. Swap `utils/chatbot.py`, `utils/resume_analyzer.py` and `utils/interview_eval.py` for LLM calls later.
- Code runs in a subprocess with a blocklist, time and memory limits (limits apply on Mac/Linux). This is a basic sandbox: for public hosting use Docker or Judge0.
- Resume files are analyzed and then deleted; only the analysis is stored.
- Before deploying: set strong secrets in `backend/.env`, set `SHOW_OTP_IN_RESPONSE=false`, set `CORS_ORIGIN`, run with gunicorn, and `npm run build` the frontend.
- Voice interview needs Chrome or Edge and microphone permission; typing works everywhere.
