# Module 10 Completion Report

## Instruction Files
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/generate-jira-query.agent.md
instructions/jira-integration.agent.md
instructions/main.agent.md
instructions/write-meeting-notes.agent.md

## main.agent.md Contents
# Instruction File Catalog

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — instruction infrastructure bootstrap and authoring guide.
  + Keywords: setup instructions, create instruction, instruction infrastructure
- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — weekly status report with fixed sections and format.
  + Keywords: status report, weekly report, progress summary
- [`./instructions/write-meeting-notes.agent.md`](./write-meeting-notes.agent.md) — meeting summary with action items and owners.
  + Keywords: meeting notes, action items, meeting summary
- [`./instructions/generate-jira-query.agent.md`](./generate-jira-query.agent.md) — JQL queries for common reporting scenarios.
  + Keywords: jira query, JQL, reporting query
- [`./instructions/jira-integration.agent.md`](./jira-integration.agent.md) — Jira issue integration payloads and automation support.
  + Keywords: Jira integration, issue payload, Jira API

## Sample Instruction
- File: instructions/jira-integration.agent.md
- Contents:
# Jira Integration Instruction

- Input format:
  + Receive a Jira issue definition with fields such as `project`, `issueType`, `summary`, `description`, `priority`, `labels`, and optional `components` or `assignee`.
  + Accept issue details as structured text or a simple YAML/JSON-like block.
  + Accept Jira API endpoint and authentication context when integration output is required.
- Processing steps:
  + Parse the provided issue fields and verify required values are present.
  + Normalize field values to Jira-compatible names and data types.
  + Validate `project`, `issueType`, `priority`, and any optional fields against common Jira constraints.
  + Convert the input into the target Jira payload or integration template.
- Output format:
  + Provide output as a concise Markdown code block containing either:
    - Jira API request JSON payload, or
    - Jira automation/query payload, or
    - structured Jira issue creation instruction.
  + If API metadata is included, include `endpoint`, `method`, and `headers` in the output.
- Constraints:
  + Do not add unrelated text or extra explanation.
  + Keep output strictly to valid Jira field mappings and supported payload structure.
  + If required input is missing or invalid, request only the missing fields.
  + Do not include real credentials; use placeholders for secrets.
