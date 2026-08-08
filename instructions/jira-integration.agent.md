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
