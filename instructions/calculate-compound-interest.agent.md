# Calculate Compound Interest Instruction

- Use this instruction when asked to compute compound interest from a principal, interest rate, compounding frequency, and duration.
- Invoke the tool with the command: `python3 tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <years>`.
- Provide numeric values for:
  + `principal` as the starting amount
  + `annual_rate` as a percentage (for example `7.34`)
  + `compounds_per_year` as the number of compounding periods per year
  + `years` as the total years (decimal values allowed)
- Present the result as two lines:
  + `Final amount: $X,XXX.XX`
  + `Interest earned: $X,XXX.XX`
- Do not include extra explanation or unrelated output.
