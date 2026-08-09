# Walkthrough Validation Rules

This file defines validation checks for `walkthrough.md` files under `modules/`. Use these rules to automatically verify completeness and quality before publishing.

1) Filename & Location
- Rule: File must be located at `modules/module-XX/walkthrough.md` (where `XX` is the two-digit module number).
- Failure: Wrong path or different filename.
- Fix: Move or rename the file to the prescribed path.

2) Title Format
- Rule: The file must start with a top-level heading matching `# Module XX Walkthrough` where `XX` matches the module folder name.
- Failure: Missing or mismatched title.
- Fix: Update the heading to include the correct module number and the exact phrase `Module` and `Walkthrough`.

3) Required Sections
- Rule: The file must include the following section headings (case-insensitive): `Overview`, `Objectives`, `Walkthrough`, `Summary`, and `Quiz`.
- Failure: Any of these headings missing.
- Fix: Add the missing sections as level-2 headings (e.g., `## Summary`).

4) Summary Content Quality
- Rule: The `Summary` section must contain at least 20 words and should concisely describe the main takeaways.
- Failure: Summary missing or under-length (less than 20 words) or contains only placeholders like `TBD`.
- Fix: Replace placeholder text with a clear 2–4 sentence summary of key learnings.

5) Quiz Requirements
- Rule: The `Quiz` section must contain at least one question. Each question should be a numbered item or a bulleted item ending with a question mark.
- Failure: No quiz entries present or entries are placeholders (e.g., `Question 1?`).
- Fix: Add meaningful quiz questions that test core module concepts; prefer 3–5 short questions.

6) Placeholders and TODOs
- Rule: The file must not contain visible placeholders such as `Objective 1`, `Step 1`, `TBD`, `TODO`, or similar filler text.
- Failure: Any placeholder strings detected.
- Fix: Replace placeholders with real content or mark the file draft and exclude it from final validation until filled.

Optional checks (recommended):
- Ensure code snippets, commands, or examples are correctly formatted with fenced code blocks.
- If the module references a `work/module-XX-report.md`, include a link under `Overview` or `Documentation`.

Automated tools can implement these checks with simple regex and token counts. When a rule fails, return a clear error that points to the rule number and the remediation suggestion above.
