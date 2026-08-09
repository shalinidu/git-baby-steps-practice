# Validate Walkthrough Files

- Task: validate all `modules/module-XX/walkthrough.md` files against the walkthrough validation rules in `validation-rules.md`.
- Files: all files matching `modules/module-*/walkthrough.md`.
- Check: verify filename/location, title format, required headings, summary length, quiz questions, and placeholder content.
- Output: per-file validation report that lists pass/fail results for each rule, plus details for any failures.
- Recommended approach: Approach 3 — Script-Based Automation.
- Script: `tools/validate_walkthroughs.py` processes each file individually and prints a summary for each walkthrough.

Keywords:
- validation
- walkthrough
- modules
- script
