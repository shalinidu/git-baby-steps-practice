# Module 12 Completion Report

## Instruction File
- Filename: instructions/use-test-coverage.agent.md

# Use Test Coverage Instruction

- Use this instruction when asked to calculate total test coverage from generated test cases and written unit tests.
- Invoke the actual tool with: `python3 tools/test_coverage.py <generated> <written>`.
- Provide numeric values for:
  + `generated` as the number of test cases generated
  + `written` as the number of unit test cases written
- Present output as a single line: `Test coverage: X.XX`.
- If `written` is zero, return an error or request a valid positive number.
- Do not include extra explanation or unrelated output.

## Script File
- Filename: tools/test_coverage.py
- Language: Python

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate total test coverage.")
    parser.add_argument("generated", type=float, help="Number of test cases generated")
    parser.add_argument("written", type=float, help="Number of unit test cases written")
    return parser.parse_args()


def main():
    args = parse_args()
    generated = args.generated
    written = args.written

    if written == 0:
        print("Error: written unit test cases must be greater than zero.")
        return

    coverage = generated / written
    print(f"Test coverage: {coverage:.2f}")


if __name__ == "__main__":
    main()

## Script Execution Output
usage: test_coverage.py [-h] generated written

Calculate total test coverage.

positional arguments:
  generated   Number of test cases generated
  written     Number of unit test cases written

options:
  -h, --help  show this help message and exit
