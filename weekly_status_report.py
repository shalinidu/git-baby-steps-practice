import argparse
import os
import shutil
import subprocess


def format_section(title, items):
    lines = [f"## {title}", *[f"- {item}" for item in items], ""]
    return "\n".join(lines)


def parse_metrics(metrics):
    items = []
    for metric in metrics:
        if ":" in metric:
            name, value = metric.split(":", 1)
            items.append((name.strip(), value.strip()))
        else:
            items.append((metric.strip(), ""))
    return items


def build_report(args):
    report = ["# Weekly Status Report", ""]
    if args.summary:
        report.append(format_section("Executive Summary", [args.summary]))
    report.append(format_section("Accomplishments", args.accomplishments or ["No accomplishments reported."]))
    report.append(format_section("Blockers", args.blockers or ["No blockers reported."]))
    report.append(format_section("Next Week's Plan", args.next or ["No plan reported."]))

    metrics = parse_metrics(args.metric)
    if metrics:
        lines = [f"- {name}: {value}" if value else f"- {name}" for name, value in metrics]
        report.append("## Metrics")
        report.append("\n".join(lines) + "\n")
    return "\n".join(report).strip() + "\n"


def markdown_to_pdf(markdown_text, output_path):
    try:
        from markdown import markdown
    except ImportError:
        raise RuntimeError("Markdown package is required for PDF generation. Install with `pip install markdown`.")

    html = markdown(markdown_text)
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(output_path)
        return
    except ImportError:
        pass

    if shutil.which("pandoc"):
        process = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "pdf", "-o", output_path],
            input=markdown_text.encode("utf-8"),
            check=False,
        )
        if process.returncode == 0:
            return
        raise RuntimeError("Pandoc failed to convert Markdown to PDF.")

    raise RuntimeError(
        "PDF generation requires either the Python package weasyprint or pandoc installed."
    )


def main():
    parser = argparse.ArgumentParser(description="Generate a weekly status report for stakeholders.")
    parser.add_argument("--summary", help="Short executive summary")
    parser.add_argument("--accomplishments", nargs="*", default=[], help="List accomplishments")
    parser.add_argument("--blockers", nargs="*", default=[], help="List blockers")
    parser.add_argument("--next", nargs="*", default=[], help="Next week's plan")
    parser.add_argument("--metric", action="append", default=[], help="Metric in 'Name:Value' form; repeat for multiple metrics")
    parser.add_argument("--output", help="Output file path (markdown or pdf)")
    parser.add_argument("--pdf", action="store_true", help="Generate a PDF report")
    args = parser.parse_args()

    content = build_report(args)
    if args.output:
        output_path = args.output
        if args.pdf and not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"
    else:
        output_path = "weekly_status_report.pdf" if args.pdf else "weekly_status_report.md"

    if args.pdf:
        markdown_to_pdf(content, output_path)
        print(f"Generated PDF report: {output_path}")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated Markdown report: {output_path}")


if __name__ == "__main__":
    main()
