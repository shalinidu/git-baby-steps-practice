# Module 15 Completion Report

## Script Metadata
- Filename: tools/validate_walkthroughs.py
- Language: Python
- Purpose: validates walkthrough files under a configurable modules directory using CLI parameters for module-folder regex, filename, glob search pattern, dry-run mode, and confirmation prompts; checks filename/location, title format, required sections, summary quality, quiz questions, and placeholder content.

## Script Contents
```python
import argparse
import re
import sys
from pathlib import Path

RULES = [
    "Filename & Location",
    "Title Format",
    "Required Sections",
    "Summary Content Quality",
    "Quiz Requirements",
    "Placeholders and TODOs",
]

PLACEHOLDERS = ["Objective 1", "Objective 2", "Step 1", "Step 2", "TBD", "TODO", "Question 1?"]

REQUIRED_SECTIONS = ["Overview", "Objectives", "Walkthrough", "Summary", "Quiz"]


def parse_args():
    parser = argparse.ArgumentParser(description="Validate module walkthrough files.")
    parser.add_argument(
        "--modules-dir",
        default="modules",
        help="Path to the modules root directory containing module-XX subdirectories.",
    )
    parser.add_argument(
        "--module-dir-pattern",
        default=r"module-\d{2}",
        help="Regex pattern for module folders under the modules directory.",
    )
    parser.add_argument(
        "--filename",
        default="walkthrough.md",
        help="Filename to validate under each module directory.",
    )
    parser.add_argument(
        "--glob-pattern",
        default="**/walkthrough.md",
        help="Glob pattern to search for files under the modules directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be validated and exit without performing validation.",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Prompt for confirmation before validating files.",
    )
    return parser.parse_args()


def check_file(path: Path, base_path: Path, module_dir_pattern: str, filename: str):
    text = path.read_text()
    lines = text.splitlines()
    errors = []

    # Rule 1: Filename and location
    try:
        relative_path = path.relative_to(base_path).as_posix()
    except ValueError:
        relative_path = path.as_posix()

    if not re.match(rf"^{module_dir_pattern}/{re.escape(filename)}$", relative_path):
        errors.append(f"Rule 1: File must be located at <modules-dir>/{module_dir_pattern}/{filename}")

    # Rule 2: Title format
    if not lines or not re.match(r"^# Module \d{2} Walkthrough$", lines[0].strip()):
        errors.append("Rule 2: Title must be '# Module XX Walkthrough' on the first line")

    # Rule 3: Required sections
    missing = [section for section in REQUIRED_SECTIONS if not re.search(rf"^##\s+{section}$", text, re.MULTILINE | re.IGNORECASE)]
    if missing:
        errors.append(f"Rule 3: Missing sections: {', '.join(missing)}")

    # Rule 4: Summary quality
    summary_match = re.search(r"^##\s+Summary$(.*?)^(## |$)", text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    if not summary_match:
        errors.append("Rule 4: Missing Summary section")
    else:
        summary_text = summary_match.group(1).strip()
        if len(summary_text.split()) < 20 or any(ph in summary_text for ph in PLACEHOLDERS):
            errors.append("Rule 4: Summary must be at least 20 words and not placeholder text")

    # Rule 5: Quiz requirements
    quiz_match = re.search(r"^##\s+Quiz$(.*?)^(## |$)", text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    if not quiz_match:
        errors.append("Rule 5: Missing Quiz section")
    else:
        quiz_text = quiz_match.group(1).strip()
        if not re.search(r"^(- |\d+\.) .+\?$", quiz_text, re.MULTILINE):
            errors.append("Rule 5: Quiz must contain at least one question ending with a question mark")

    # Rule 6: Placeholders/TODOs
    placeholders = [ph for ph in PLACEHOLDERS if ph in text]
    if placeholders:
        errors.append(f"Rule 6: Placeholder content detected: {', '.join(placeholders)}")

    return errors


def main():
    args = parse_args()
    base_path = Path(args.modules_dir).resolve()
    if not base_path.exists():
        print(f"Error: modules directory not found: {base_path}", file=sys.stderr)
        return 1

    files = sorted(base_path.rglob(args.glob_pattern))
    if args.dry_run:
        print("Dry run mode: files that would be validated:")
        for path in files:
            print(f"- {path.relative_to(base_path)}")
        print(f"\nTotal files found: {len(files)}")
        return 0

    if args.confirm:
        print(f"Ready to validate {len(files)} files under {base_path}.")
        answer = input("Continue? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Validation aborted.")
            return 0

    results = []
    for path in files:
        errors = check_file(path, base_path, args.module_dir_pattern, args.filename)
        results.append((path.relative_to(base_path.parent), errors))

    print("Validation Summary")
    print("==================")
    for path, errors in results:
        print(f"\nFile: {path}")
        if not errors:
            print("  PASS")
        else:
            print("  FAIL")
            for error in errors:
                print(f"   - {error}")

    failing = [path for path, errors in results if errors]
    print(f"\nTotal files checked: {len(results)}")
    print(f"Passing: {len(results) - len(failing)}")
    print(f"Failing: {len(failing)}")


if __name__ == "__main__":
    main()
```

## Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--modules-dir` | Path to the modules root directory containing `module-XX` directories. | `modules` |
| `--module-dir-pattern` | Regex pattern for module folder names under the modules directory. | `module-\d{2}` |
| `--filename` | Filename to validate within each module folder. | `walkthrough.md` |
| `--glob-pattern` | Glob pattern to search for files under the modules directory. | `**/walkthrough.md` |
| `--dry-run` | Print which files would be validated and exit without performing validation. | false |
| `--confirm` | Prompt for confirmation before validating files. | false |
## Test Run Output
Validation Summary
==================

File: modules/module-03/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

File: modules/module-08/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

File: modules/module-09/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

File: modules/module-10/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

File: modules/module-12/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

File: modules/module-13/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

File: modules/module-14/walkthrough.md
  FAIL
   - Rule 1: File must be located at modules/module-XX/walkthrough.md
   - Rule 4: Summary must be at least 20 words and not placeholder text
   - Rule 5: Quiz must contain at least one question ending with a question mark
   - Rule 6: Placeholder content detected: Objective 1, Objective 2, Step 1, Step 2, Question 1?

Total files checked: 7
Passing: 0
Failing: 7
