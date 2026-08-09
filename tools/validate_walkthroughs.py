import re
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


def check_file(path: Path):
    text = path.read_text()
    lines = text.splitlines()
    errors = []

    # Rule 1: Filename and location
    if not re.match(r"modules/module-\d{2}/walkthrough\.md$", str(path).replace('\\', '/')):
        errors.append("Rule 1: File must be located at modules/module-XX/walkthrough.md")

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
    base_path = Path(__file__).resolve().parents[1] / "modules"
    results = []
    for path in sorted(base_path.rglob("walkthrough.md")):
        errors = check_file(path)
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
