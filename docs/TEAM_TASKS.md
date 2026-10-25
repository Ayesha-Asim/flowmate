# FlowMate Team Workboard

## Frontend teammate — You
- [ ] F1: Clone repo, run frontend and backend locally.
- [ ] F2: Confirm brand colors, typography, layout and mobile navigation.
- [ ] F3: Goal creator: validation, loading, errors, sample prompts.
- [ ] F4: Plan overview: task priority, due date, task dependencies.
- [ ] F5: Task board: edit title, description, priority, due date and status.
- [ ] F6: AI replan: diff preview, approval/rejection, empty/error states.
- [ ] F7: Progress page: completion, overdue and upcoming tasks.
- [ ] F8: Responsive testing on mobile and laptop.
- [ ] F9: Integrate with live backend; confirm all API states.
- [ ] F10: Screenshots, demo recording, usability polish.

## Backend teammate — Friend
- [ ] B1: Run FastAPI and test /health and /docs.
- [ ] B2: Get verified Nebius account access and a supported NVIDIA model ID.
- [ ] B3: Verify live inference; store key only in backend .env.
- [ ] B4: Validate model plan JSON; sensible tasks, priorities and dates.
- [ ] B5: Improve project and task storage and task editing.
- [ ] B6: Implement dependency checking and milestone logic.
- [ ] B7: Generate meaningful AI replanning proposals.
- [ ] B8: Validate proposal diffs and ensure approval is required.
- [ ] B9: Add authentication and per-user access before public use.
- [ ] B10: Deploy API, configure CORS, test error handling and rate limits.

## Shared integration and submission
- [ ] S1: Agree on JSON response schema and API routes.
- [ ] S2: Test generate → board update → refresh → replan → approve.
- [ ] S3: Confirm a real NVIDIA model request is visible in logs (no keys shown).
- [ ] S4: Test live demo URL from a different device.
- [ ] S5: Add setup steps, screenshots, model details and limitations to README.
- [ ] S6: Record ≤3-minute public YouTube demo.
- [ ] S7: Submit correct track, repo, demo, video and feedback.

## Suggested daily milestones (adapt to your actual deadline)
| Day | Frontend | Backend | Joint acceptance test |
|---|---|---|---|
| 1 | Run starter; brand and navigation | Run starter; confirm Nebius access | UI + API launch locally |
| 2 | Goal input and plan view | Live generate endpoint | Real model plan renders |
| 3 | Task board edits | Persistence and validation | Changes survive refresh |
| 4 | Replan comparison screen | Live replan + approval endpoint | Preview then approve |
| 5 | Progress and mobile polish | Security, errors, deployment | End-to-end deployed flow |
| 6 | Demo video and screenshots | README and API documentation | Final test and submission |

## Definition of done for every task
- Works locally; no obvious console errors.
- Handles loading, empty and failure states.
- Does not leak API keys or private data.
- Code reviewed by the other teammate.
- Includes a screenshot or test steps in pull request.
