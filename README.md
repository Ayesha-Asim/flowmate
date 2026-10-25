# FlowMate — AI Workflow Planner

> Two-person Nebius × NVIDIA Global AI Hackathon starter repository.

**Status:** Starter template. The UI and API run in **demo mode** by default. Demo mode does **not** call NVIDIA or Nebius and does **not** meet the hackathon model requirement. Enable and verify live mode before submission.

## What works now
- Responsive React + TypeScript dashboard, goal form, project overview, Kanban task board, progress summary.
- FastAPI API with SQLite storage, task updates, plan generation, replan proposal + approval.
- Mock plan generation and mock replanning for local development.
- Configurable OpenAI-compatible model API adapter for Nebius; real integration **not yet verified**.

## Team ownership
- **Frontend teammate:** `frontend/` — design, screens, usability, API integration.
- **Backend teammate:** `backend/` — API, Nebius NVIDIA model integration, validation, storage.
- **Both:** testing, documentation, demo video, release.

## Run locally (Windows PowerShell)

**Backend terminal:**
```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload --port 8000
```
If PowerShell blocks activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000` instead.

**Frontend terminal:**
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```
Open http://localhost:5173 and visit API docs at http://localhost:8000/docs.

## Live NVIDIA/Nebius integration
1. Confirm your Nebius Token Factory/AI Cloud access and the exact NVIDIA open-source model available to your account.
2. In `backend/.env`, set `AI_MODE=live`, `NEBIUS_API_KEY`, `NEBIUS_BASE_URL` (provider's OpenAI-compatible `/v1` base URL), and `NEBIUS_MODEL` (verified model identifier).
3. Restart FastAPI. `/health` should return `mode: live`.
4. Generate a plan and verify a **real successful model response**, not merely the health status. Test replanning too.
5. If the model does not support JSON response format, adjust `call_model()` for the actual provider capabilities, then validate the returned content before saving.
6. Capture architecture and model usage in the demo/README. **Never** commit credentials.

The model adapter is a starting point; API endpoints, model availability, authentication, and structured-output support must be verified against current Nebius documentation.

## API endpoints
| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Server status and mode |
| POST | `/api/plans/generate` | Goal → project plan |
| GET | `/api/projects` | Saved projects |
| GET | `/api/projects/{id}` | Project details |
| PATCH | `/api/tasks/{id}` | Update a task |
| POST | `/api/projects/{id}/replan` | Preview suggested changes |
| POST | `/api/projects/{id}/apply-replan` | Apply approved proposal |

## Collaboration
1. One teammate creates a GitHub repository and adds the other as a collaborator.
2. Keep `main` stable; create `feature/frontend-*` and `feature/backend-*` branches.
3. Open pull requests; review and merge only after local tests.
4. Do not edit the other teammate's folder without coordinating.
5. Use GitHub Issues to assign daily tasks. See `docs/TEAM_TASKS.md`.

## Test commands
```bash
# from backend/ with dependencies installed
pytest -q
# from frontend/
npm run build
```

## Limitations and next steps
- No authentication: do not expose the demo API publicly with real user data. Add authentication, access controls, rate limits and per-user project ownership before public launch.
- SQLite is for local demos; use managed persistent storage for deployment.
- The task editor currently changes status only; expand to edit title, priority, dates and dependencies.
- The mock replan adjusts dates using a simple rule and ignores semantic intent beyond basic day shifts.
- Add automated end-to-end tests and real deployment health checks.

## Hackathon submission checklist
- [ ] Working live NVIDIA open-source model on Nebius
- [ ] Hosted working demo URL
- [ ] Public repository + MIT license + setup instructions
- [ ] Public YouTube demo ≤3 minutes
- [ ] Project description, track, technology details and feedback
- [ ] Verify official rules, deadline and participant eligibility

**Suggested track:** Best Apps and Agents.
