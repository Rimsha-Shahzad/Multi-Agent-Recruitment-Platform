# AI-Powered Recruitment Marketing Platform

A working demo of an **enterprise recruitment marketing platform** powered by a
5-agent **LangGraph** pipeline, a **FastAPI + PostgreSQL/SQLite** backend, and a
**Next.js** dashboard.

> Everything is already built and copy-pasted into the right files for you.
> You just need to install some software and run two commands. Follow this
> guide top to bottom — it assumes you've never set this up before.

---

## 1. What this project does (for your presentation)

**Agent workflow (LangGraph, linear pipeline):**

1. **Persona Agent** – profiles the ideal candidate for the role (skills,
   motivations, preferred channels, keywords).
2. **Content Agent** – generates a job ad (headline, body, call-to-action)
   tailored to that persona.
3. **Distribution Agent** – "posts" the ad across LinkedIn, Indeed, Google
   Jobs, and the company careers site.
4. **Engagement Agent** – generates candidate leads from those postings and
   sends each one a personalised nurture message (via HubSpot).
5. **Analytics Agent** – aggregates impressions, clicks, applications,
   qualified leads, interviews, hires, CTR and application rate.

**Tech stack mapping:**

| Brief item | Where it lives |
|---|---|
| LangGraph | `backend/graph.py` |
| Python | entire `backend/` folder |
| PostgreSQL | `backend/database.py` (SQLite by default, Postgres optional — see step 6) |
| Next.js | `frontend/` folder |
| GPT-4o | `backend/mock_apis.py` → `call_llm()` (used by Persona & Content agents) |
| LinkedIn / Indeed / Google Jobs / HubSpot APIs | `backend/mock_apis.py` (real calls can be dropped in later — see step 7) |

**Important — about the external APIs:** LinkedIn, Indeed, Google Jobs and
HubSpot all require business/developer approval that takes days or weeks to
get. So that you can finish **today**, this project runs on realistic **mock
data** for those by default. The agent logic, LangGraph workflow, database,
and dashboard are all fully real and working — only the external API calls
are simulated. This is completely normal for a student/demo project and you
can explain it exactly like that to your evaluator.

---

## 2. Software you need to install

Install these once, in this order:

1. **Python 3.10 or newer** — https://www.python.org/downloads/
   - On Windows, during install, check ✅ "Add Python to PATH".
2. **Node.js 18 or newer** (includes npm) — https://nodejs.org/ (choose the
   LTS version)
3. **A code editor** — VS Code is recommended: https://code.visualstudio.com/
4. *(Optional, only if you want real PostgreSQL instead of the built-in
   SQLite database)* **Docker Desktop** — https://www.docker.com/products/docker-desktop/

To check everything installed correctly, open a terminal (Command Prompt /
PowerShell / Terminal) and run:

```bash
python --version
node --version
npm --version
```

Each should print a version number.

---

## 3. Project folder structure

Everything has already been created for you in this structure:

```
recruitment-platform/
├── backend/
│   ├── agents/
│   │   ├── persona_agent.py
│   │   ├── content_agent.py
│   │   ├── distribution_agent.py
│   │   ├── engagement_agent.py
│   │   └── analytics_agent.py
│   ├── graph.py          ← LangGraph pipeline definition
│   ├── main.py            ← FastAPI app (the backend server)
│   ├── models.py          ← database tables
│   ├── database.py        ← database connection
│   ├── mock_apis.py        ← GPT-4o / LinkedIn / Indeed / Google Jobs / HubSpot
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── layout.js
│   │   ├── page.js         ← the dashboard UI
│   │   └── globals.css
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml     ← optional PostgreSQL
└── README.md
```

You do **not** need to write or copy any code — it's all already in place.
You just need to install dependencies and run it.

---

## 4. Run the backend (FastAPI + LangGraph)

Open a terminal **in the `backend` folder**:

```bash
cd recruitment-platform/backend
```

### 4.1 Create a virtual environment (keeps dependencies isolated)

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (Command Prompt):** `venv\Scripts\activate.bat`
- **Mac/Linux:** `source venv/bin/activate`

You should now see `(venv)` at the start of your terminal line.

### 4.2 Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI, LangGraph, SQLAlchemy, etc. It may take a minute or two.

### 4.3 (Optional) Add your OpenAI API key

Copy `.env.example` to a new file named `.env` in the same `backend` folder:

```bash
copy .env.example .env        # Windows
cp .env.example .env           # Mac/Linux
```

Open `.env` and, if you have a GPT-4o / OpenAI API key, paste it like this:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

If you don't have one, leave it blank — the app automatically uses a built-in
mock generator instead, and everything still works.

### 4.4 Start the backend server

```bash
uvicorn main:app --reload --port 8000
```

Leave this terminal running. You should see something like
`Application startup complete.` and a database file `recruitment.db` will be
created automatically (no extra setup needed).

Test it: open http://localhost:8000 in your browser — you should see a JSON
message confirming the API is running. You can also open
http://localhost:8000/docs for the interactive API documentation.

---

## 5. Run the frontend (Next.js dashboard)

Open a **second, new terminal** (keep the backend terminal running) **in the
`frontend` folder**:

```bash
cd recruitment-platform/frontend
```

### 5.1 Install dependencies

```bash
npm install
```

### 5.2 Start the dashboard

```bash
npm run dev
```

Open your browser to **http://localhost:3000**

You'll see the dashboard. Fill in a job title, company, location and
seniority, then click **"Run campaign"**. The frontend sends the request to
your FastAPI backend, which runs the full 5-agent LangGraph pipeline and
returns the persona, job ad, distribution postings, candidate leads, and
analytics — all displayed live on the dashboard.

---

## 6. (Optional) Switch to PostgreSQL

By default the app uses SQLite (a single file, zero setup) which is fine for
a demo/final project. If your brief specifically requires showing
PostgreSQL:

1. Install Docker Desktop and make sure it's running.
2. From the project root folder, run:
   ```bash
   docker compose up -d
   ```
   This starts a PostgreSQL database on `localhost:5432`.
3. In `backend/.env`, uncomment and set:
   ```
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/recruitment
   ```
4. Restart the backend (`Ctrl+C` then run `uvicorn main:app --reload --port 8000`
   again). It will create all tables in Postgres automatically.

No code changes are needed — `backend/database.py` already supports both.

---

## 7. (Optional) Connecting real APIs later

Everything in `backend/mock_apis.py` has a clearly marked spot
(`# TODO: real call to ... API would go here`) where you'd add the actual
API call once you have approved developer access to LinkedIn, Indeed, Google
Jobs, or HubSpot. Until then, the mock responses keep the whole pipeline
working so you can demo it today.

---

## 8. Troubleshooting

- **"command not found: python"** → try `python3` instead of `python`.
- **Backend errors on startup** → make sure you activated the virtual
  environment (you should see `(venv)`) before running `pip install` and
  `uvicorn`.
- **Frontend shows "Could not reach the backend"** → make sure the backend
  terminal is still running and shows no errors, and that it's on port 8000.
- **Port already in use** → close other programs using ports 8000 or 3000,
  or change the port number in the run commands (and in
  `frontend/next.config.js` if you change the backend port).
- **CORS errors in browser console** → the backend already allows all
  origins; make sure you're visiting `http://localhost:3000`, not
  `127.0.0.1:3000`.

---

## 9. What to say in your presentation

- "I built a multi-agent recruitment marketing pipeline using LangGraph,
  where each agent (Persona, Content, Distribution, Engagement, Analytics)
  is a node in the graph and passes a shared state to the next."
- "The backend is FastAPI with SQLAlchemy, supporting both SQLite (for local
  development) and PostgreSQL (for production), matching the enterprise
  tech stack."
- "The frontend is a Next.js dashboard that triggers the pipeline and
  visualizes each agent's output in real time."
- "External integrations (LinkedIn, Indeed, Google Jobs, HubSpot, GPT-4o)
  are implemented behind an adapter layer (`mock_apis.py`) — they use mock
  data today because real API access requires business approval, but the
  integration points are fully scaffolded and ready for real credentials."
