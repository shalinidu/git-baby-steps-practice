from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


def format_section(title: str, items: Sequence[str]) -> str:
    lines = [f"## {title}", *[f"- {item}" for item in items], ""]
    return "\n".join(lines)


def format_key_values(title: str, values: Dict[str, Any]) -> str:
    lines = [f"## {title}"]
    for name, value in values.items():
        lines.append(f"- {name}: {value}")
    lines.append("")
    return "\n".join(lines)


def load_template(template_path: str = "reports/template.md") -> str:
    path = Path(template_path)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return (
        "# Weekly Status Report\n\n"
        "## 1. Executive Summary\n"
        "Provide a concise summary of the week’s progress, key decisions, and any critical issues.\n\n"
        "## 2. Delivery Progress\n"
        "- Sprint/Project:\n"
        "- Current status:\n"
        "- Completed this week:\n"
        "- In progress:\n"
        "- Planned next week:\n\n"
        "## 3. Risks and Issues\n"
        "- Top risk:\n"
        "- Status/impact:\n"
        "- Mitigation actions:\n\n"
        "## 4. Budget and Forecast\n"
        "- Planned spend:\n"
        "- Actual spend:\n"
        "- Burn rate:\n"
        "- Remaining budget:\n"
        "- Forecasted variance:\n\n"
        "## 5. Resource Utilization\n"
        "- Total team capacity:\n"
        "- Utilization by role:\n"
        "  - Role 1:\n"
        "  - Role 2:\n"
        "  - Role 3:\n"
        "- Capacity concerns:\n\n"
        "## 6. Quality / QA Status\n"
        "- Open defects by severity:\n"
        "- Test execution summary:\n"
        "- Quality incidents:\n"
        "- Release risk:\n\n"
        "## 7. Blocked Work Summary\n"
        "- Total blocked issues:\n"
        "- Key blocked items:\n"
        "  - Issue 1:\n"
        "  - Issue 2:\n"
        "- Next steps to unblock:\n\n"
        "## 8. Prior Sprint Comparison\n"
        "- Sprint 1 status summary:\n"
        "- Sprint 2 status summary:\n"
        "- Trend observations:\n"
    )


def build_report(context: Dict[str, Any]) -> str:
    report: List[str] = ["# Weekly Status Report", ""]

    if summary := context.get("summary"):
        report.append(format_section("Executive Summary", [summary]))

    report.append(format_section("Accomplishments", context.get("accomplishments") or ["No accomplishments reported."]))
    report.append(format_section("Blockers", context.get("blockers") or ["No blockers reported."]))
    report.append(format_section("Next Week's Plan", context.get("next_plan") or ["No plan reported."]))

    metrics = context.get("metrics") or {}
    if metrics:
        report.append(format_key_values("Metrics", metrics))

    if jira_data := context.get("jira_data"):
        sprint = jira_data.get("sprint", {})
        report.append(format_key_values("Current Sprint Snapshot", {
            "Sprint name": sprint.get("name", "N/A"),
            "Sprint id": sprint.get("id", "N/A"),
            "Board id": jira_data.get("board_id", "N/A"),
            "Project key": jira_data.get("project_key", "N/A"),
            "Total issues": len(jira_data.get("issues", [])),
            "Blocked issues": len(jira_data.get("blocked_issues", [])),
        }))

        blocked_issues = jira_data.get("blocked_issues") or []
        if blocked_issues:
            lines = [
                f"{issue.get('key', 'UNKNOWN')}: {issue.get('fields', {}).get('summary', 'No summary')}"
                for issue in blocked_issues
            ]
            report.append(format_section("Blocked Issue Appendix", lines))

    return "\n".join(report).strip() + "\n"
