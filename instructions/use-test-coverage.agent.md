# Use Test Coverage Instruction

- Use this instruction when asked to calculate total test coverage from generated test cases and written unit tests.
- Invoke the actual tool with: `python3 tools/test_coverage.py <generated> <written>`.
- Provide numeric values for:
  + `generated` as the number of test cases generated
  + `written` as the number of unit test cases written
- Present output as a single line: `Test coverage: X.XX`.
- If `written` is zero, return an error or request a valid positive number.
- Do not include extra explanation or unrelated output.
