# Module 18 Completion Report

## Target Application
- URL: http://localhost:4173 (React SPA, Docker Compose service `client`; API under test at http://localhost:3001/api/v1). Routes exercised: `/dashboard/54`, `/issues/54`, `/trend/54`, `/status`.

## QA Findings
| # | Category | Finding | Severity | MCP Tool Used |
|---|----------|---------|----------|---------------|
| 1 | Network / CORS | API requests from the SPA origin (`:4173`) to the API origin (`:3001`) were blocked: "Access to fetch at 'http://localhost:3001/api/v1/sprints' from origin 'http://localhost:4173' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource." | Critical | mcp__chrome-devtools__list_console_messages |
| 2 | Functional / Filtering | Filtering the Sprint Issue List by Status = "Blocked" returned zero results ("This sprint has no issues yet") even though a blocked issue (PROJ-103) existed in the unfiltered list; the backend filtered on the raw Jira `status` column instead of the computed status bucket | High | mcp__chrome-devtools__take_snapshot |
| 3 | Functional / Error handling | Clicking "Refresh now" while Jira was unreachable produced no visible feedback; console showed "Failed to load resource: the server responded with a status of 502 (Bad Gateway)" and "Uncaught (in promise)" — an unhandled promise rejection with no error state shown to the user | Medium | mcp__chrome-devtools__list_console_messages |
| 4 | Accessibility | DevTools issue reported: "A form field element should have an id or name attribute" (count: 1), on the sprint selector `<select>` | Low | mcp__chrome-devtools__list_console_messages |

## MCP Tools Used
- mcp__chrome-devtools__new_page
- mcp__chrome-devtools__list_pages
- mcp__chrome-devtools__navigate_page
- mcp__chrome-devtools__resize_page
- mcp__chrome-devtools__take_screenshot
- mcp__chrome-devtools__take_snapshot
- mcp__chrome-devtools__list_console_messages
- mcp__chrome-devtools__click
- mcp__chrome-devtools__fill
- mcp__chrome-devtools__fill_form
- mcp__chrome-devtools__press_key
