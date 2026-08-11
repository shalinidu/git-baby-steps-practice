# Module 17 Completion Report

## Specification Contents
```markdown
# Feature Specification: Automated Sprint Health Dashboard

**Feature Branch**: `001-sprint-health-dashboard`
**Created**: 2026-08-11
**Status**: Draft
**Input**: PROJECT_IDEAS.md #1 — "Automated Sprint Health Dashboard": managers
lack a quick, consistent overview of sprint progress, making it hard to spot
blocked work, scope creep, or uneven team load.
**Constitution**: [spec/constitution.md](./constitution.md)

## User Scenarios & Testing (mandatory)

### Primary User Story
As a Delivery Manager, I want a single dashboard that shows the health of
the active sprint — progress, blocked work, and how load is distributed
across the team — so I can spot risk without manually cross-referencing
Jira boards and filters before every standup or status meeting.

### Acceptance Scenarios
1. **Given** an active sprint with a mix of Done, In Progress, and Blocked
   issues, **When** the Delivery Manager opens the dashboard, **Then** they
   see the sprint's completion percentage, total/done/blocked issue counts,
   and a list of blocked issues with their blocking reason.
2. **Given** issues assigned unevenly across team members, **When** the
   dashboard loads, **Then** a per-assignee workload view shows issue count
   and story points per person, making imbalance visually obvious.
3. **Given** new issues were added to the sprint after it started, **When**
   the Delivery Manager views the dashboard, **Then** scope creep is flagged
   by comparing the current issue set against the sprint's starting
   snapshot.
4. **Given** the Delivery Manager wants historical context, **When** they
   open the trend view, **Then** they see completion % and blocked-issue
   count for the current sprint plotted alongside recent prior sprints.
5. **Given** Jira Cloud is unreachable or credentials are invalid, **When**
   the dashboard attempts to load or refresh data, **Then** the UI shows an
   explicit error state rather than a blank or stale-looking dashboard.

### Edge Cases
- Active sprint has zero issues (empty state, not an error).
- Issues missing story points (must not silently break completion-by-points
  calculations — falls back to issue-count-based progress).
- An issue is unassigned (must appear in an "Unassigned" workload bucket,
  not be dropped).
- The configured "Blocked" status doesn't exist on a given board (must
  degrade to zero blocked issues, not fail the whole fetch).
- Jira API rate limiting or transient failure during a refresh (must not
  corrupt or clear previously loaded data).
- More than one sprint is active simultaneously on a board (dashboard must
  let the user pick which one).

## Requirements (mandatory)

### Functional Requirements
- **FR-001**: System MUST fetch the active sprint's issues from Jira Cloud,
  including status, assignee, story points, issue type, and sprint
  membership.
- **FR-002**: System MUST classify each issue into a status bucket (To Do /
  In Progress / Blocked / Done) using a configurable status mapping.
- **FR-003**: System MUST identify blocked issues via a configurable
  "Blocked" status name and capture the blocking reason where available.
- **FR-004**: System MUST compute sprint completion using issue-count-based
  progress, matching the Weekly Delivery Report project's convention
  (`project_spec.md`), with story-point totals shown as supplementary
  context.
- **FR-005**: System MUST show per-assignee workload (issue count and story
  points), including an explicit "Unassigned" bucket.
- **FR-006**: System MUST capture a snapshot of the sprint's issue set at
  sprint start and use it to detect and flag scope creep (issues added after
  the snapshot).
- **FR-007**: System MUST persist periodic sprint snapshots so that
  historical trend data survives across dashboard sessions and server
  restarts.
- **FR-008**: System MUST let the user select which sprint to view (active
  sprint plus recent prior sprints).
- **FR-009**: System MUST show the current sprint alongside trend data for
  at least the prior 2 sprints, consistent with the comparison window used
  in the Weekly Delivery Report project.
- **FR-010**: System MUST authenticate to Jira Cloud using credentials
  supplied via environment variables, per the constitution's credential
  handling principle.
- **FR-011**: System MUST show an explicit error state when Jira data
  cannot be fetched or refreshed, and MUST NOT silently display stale data
  as if it were current.
- **FR-012**: System MUST support both a manual, user-triggered refresh and
  a periodic automatic refresh of dashboard data. *(Refresh interval:
  [NEEDS CLARIFICATION: exact cadence for automatic refresh not specified])*
- **FR-013**: Dashboard access control. *(Not yet defined — [NEEDS
  CLARIFICATION: does the dashboard require user login/auth, or is it
  trusted-network / single-tenant for now?])*
- **FR-014**: Scope-creep detection threshold. *(Not yet defined — [NEEDS
  CLARIFICATION: is any issue added after snapshot flagged, or only once a
  threshold count/percentage is exceeded?])*
- **FR-015**: System MUST read the target Jira board and project from
  environment variables (`JIRA_BASE_URL`, `JIRA_BOARD_ID`,
  `JIRA_PROJECT_KEY`) rather than a UI setting or hardcoded value,
  consistent with v1's single-board scope (see Out of Scope) and the
  constitution's Secure Credential Handling principle. *(Resolves
  `clarify.md` B1.)*

### Key Entities
- **Sprint** — a Jira sprint tracked by the dashboard: Jira sprint ID, name,
  board ID, start/end dates, state (active/closed).
- **Issue** — a Jira issue within a tracked sprint: Jira issue key, sprint
  reference, type, status, assignee, story points, blocked flag, blocking
  reason, last-updated timestamp.
- **SprintSnapshot** — a point-in-time capture of a sprint's health, used
  for scope-creep detection and trend history: sprint reference, captured-at
  timestamp, total/done/blocked issue counts, completion percentage, total
  and remaining story points.
- **Assignee** — a team member issues can be attributed to: Jira account ID,
  display name; used to group the workload view.

## API Endpoints (illustrative — final contract defined in plan.md)
- `GET /health` — operational health check (server liveness only, no
  business data); intentionally outside `/api` versioning, per common
  convention for infra/monitoring endpoints.
- `GET /api/sprints` — list tracked sprints (active + recent history).
- `GET /api/sprints/:sprintId/summary` — computed health summary: completion
  %, total/done/blocked counts, scope-creep flag.
- `GET /api/sprints/:sprintId/issues` — issue-level detail, filterable by
  status and assignee.
- `GET /api/sprints/:sprintId/workload` — per-assignee issue count and
  story-point breakdown.
- `GET /api/sprints/:sprintId/trend` — snapshot history for the current
  sprint plus prior 2 sprints.
- `POST /api/sprints/:sprintId/refresh` — trigger an on-demand re-fetch from
  Jira Cloud.

## UI Screens
- **Dashboard Overview** — sprint selector, summary tiles (completion %,
  blocked count, days remaining), workload-by-assignee chart, blocked-issues
  list with blocking reasons.
- **Sprint Issue List** — filterable/sortable table of all issues in the
  selected sprint (status, assignee, points, blocked reason).
- **Trend View** — chart of completion % and blocked-issue count across the
  active sprint plus prior 2 sprints.
- **Error / Empty States** — Jira unreachable, credentials invalid, no
  active sprint, sprint with zero issues.

## Out of Scope
- Confluence integration (meeting notes, risk pages) — reserved for a
  separate feature spec (see PROJECT_IDEAS.md #2 and #3).
- Budget, capacity, and QA connectors — these belong to the separate Weekly
  Delivery Report project (`project_spec.md`), not this dashboard.
- Editing or transitioning Jira issues from the dashboard — v1 is read-only.
- Multi-board / multi-project aggregation — v1 targets a single Jira board.
- Formal SLA/performance targets (dashboard load time, data-freshness
  budget, accuracy tolerance) — v1 ships without measurable targets;
  define these once real usage data exists (`clarify.md` G1).
- Automated snapshot retention/cleanup — v1 retains `SprintSnapshot` rows
  indefinitely; revisit only if storage becomes a real constraint
  (`clarify.md` G2).
- Working-day/timezone-aware "days remaining" logic — v1 computes simple
  calendar days between now and the sprint end date in the server's local
  timezone (`clarify.md` G3).
- A normalized `Issue` → `Assignee` foreign-key relationship — v1 stores
  assignee account ID/display name directly on the `Issue` row
  (denormalized); revisit only if per-assignee data needs grow
  (`clarify.md` G4).
- Dedicated Jira API mock/contract-test infrastructure — v1 satisfies
  Principle II (TDD) using static fixture JSON captured from real Jira
  responses instead of a mock server (`clarify.md` G5).
- A formal shared app-shell design (auth/navigation/schema namespace) for
  future Confluence-focused specs — deferred until a second feature spec
  actually exists; v1 is built as a standalone app (`clarify.md` G6).

## Clarifications
- **Resolved by scoping out (2026-08-11)**: `clarify.md` Gaps G1–G6 — each
  resolved by locking a simple v1 default and deferring the more rigorous
  version; see the newly added Out of Scope bullets above for the specific
  decision made per gap.
- **Resolved (2026-08-11)**: `clarify.md` Blocking item B1 (Jira
  board/project configuration) — see FR-015. Decided via
  `spec/tasks.md` T001.
- **Still open**: `[NEEDS CLARIFICATION]` markers under Functional
  Requirements (FR-012, FR-013, FR-014), and Blocking items B2–B4 from
  `clarify.md` (dashboard access control, the Jira field backing "blocking
  reason," and the sprint-start snapshot trigger). These are real
  decisions, not deferrable scope cuts, and are addressed as the remaining
  steps of Phase 0 in `spec/plan.md` before feature implementation begins.

## Review & Acceptance Checklist
- [x] No implementation details beyond what's needed to scope endpoints/
      screens (framework/library choices deferred to plan.md)
- [x] Written in terms of user value and observable behavior
- [x] All mandatory sections completed
- [ ] All `[NEEDS CLARIFICATION]` markers resolved
- [ ] Requirements are testable and unambiguous (pending clarification items)
- [ ] Success criteria are measurable
- [ ] Reviewed against `spec/constitution.md` for principle conflicts

## Execution Status
- [x] User description parsed (from PROJECT_IDEAS.md #1)
- [x] Key concepts extracted (progress, blocked work, workload, scope creep,
      trend history)
- [ ] Ambiguities marked (`[NEEDS CLARIFICATION]`) — 3 open (FR-012,
      FR-013, FR-014); Gaps G1–G6 resolved by scoping out
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed (blocked on FR-012/013/014 and Blocking
      items B1–B4, see `clarify.md`)
```

## Commit History
```
02fc8ac Add implementation checklist; document /health in the spec
b412a27 Implement T008 (backend scaffold), T009 (Postgres compose), T011 (schema/migrations), and T016 (frontend scaffold)
559a221 Add cross-artifact analysis; resolve T001 (Jira board/project config)
7638b8c Add clarify, plan, and tasks; resolve spec gaps by scoping out
eea3e73 commit the specs
37368fc Initial scaffold for jira-confluence-automation
```

## Commit Count
6

## Project Files
```
.gitignore
LICENSE
README.md
client/.gitignore
client/.oxlintrc.json
client/README.md
client/index.html
client/package-lock.json
client/package.json
client/public/favicon.svg
client/public/icons.svg
client/src/App.css
client/src/App.jsx
client/src/assets/hero.png
client/src/assets/react.svg
client/src/assets/vite.svg
client/src/index.css
client/src/main.jsx
client/vite.config.js
docker-compose.yml
requirements.txt
server/package-lock.json
server/package.json
server/src/app.js
server/src/db/migrate.js
server/src/db/migrations/0001_init.sql
server/src/db/pool.js
server/src/server.js
server/test/health.test.js
spec/analyze.md
spec/checklist.md
spec/clarify.md
spec/constitution.md
spec/plan.md
spec/specification.md
spec/tasks.md
src/jira_confluence_automation/__init__.py
```
