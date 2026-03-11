# Gemini Context & Memory Log

**CRITICAL MANDATE FOR GEMINI:**
Every time a change is made to this codebase (code modifications, settings adjustments, commits, debugging sessions, or significant observations), you MUST append a new entry to the "Changelog" section of this `GEMINI.md` file with the current date. This file serves as the definitive memory state for the project.

## Changelog

### [2026-03-11] Architecture Cleanup & UI Optimization
- **Backend Refactoring:** Cleaned up FastAPI backend by removing legacy Jinja2 UI templates (`src/templates`). Converted the backend into a pure JSON API. Fixed SMTP port configuration (5173 -> 465) for Gmail SSL. Added a global `ExceptionMiddleware` for standardized JSON error handling. Cleaned up unused imports and relative path hacks.
- **Alert Integration:** Integrated the alert service directly into the pipeline in `routes_inference.py` so that detecting a "Wildfire" automatically triggers an email notification.
- **Frontend Optimization:** Improved the UI responsiveness of the React/Vite app. Switched to a compact grid layout, reduced padding, capped image preview heights, and implemented an `h-screen` container to resolve persistent fit-to-screen and overlapping issues at 100% zoom.
- **Debugging:** Tracked down and resolved a Vite build failure caused by a JSX mismatched closing tag in `App.jsx`.
- **Issue Tracking:** Opened Issue #7 (and closed after resolving UI/build issues). Opened Issue #8 to track concerns regarding FastAPI backend reliability and dependency conflicts.
- **Commits:** Pushed all integration, UI fixes, and cleanup changes to the `rebuild` branch on GitHub.
