import argparse
import os
import shutil
import subprocess
from typing import Any, Dict

from data_fetcher import CsvDataFetcher, DataFetchError, JiraDataFetcher
from report_builder import build_report


def parse_metrics(metrics):
    items: Dict[str, str] = {}
    for metric in metrics:
        if ":" in metric:
            name, value = metric.split(":", 1)
            items[name.strip()] = value.strip()
        else:
            items[metric.strip()] = ""
    return items


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
    parser.add_argument("--source", choices=["manual", "jira", "csv"], default="manual", help="Data source used to enrich the report")
    parser.add_argument("--csv-path", help="Path to CSV file when using --source csv")
    parser.add_argument("--output", help="Output file path (markdown or pdf)")
    parser.add_argument("--pdf", action="store_true", help="Generate a PDF report")
    args = parser.parse_args()

    context: Dict[str, Any] = {
        "summary": args.summary,
        "accomplishments": args.accomplishments,
        "blockers": args.blockers,
        "next_plan": args.next,
        "metrics": parse_metrics(args.metric),
    }

    if args.source == "jira":
        try:
            fetcher = JiraDataFetcher()
            payload = fetcher.fetch()
            context["jira_data"] = payload["jira"]
            context["metrics"].update(payload.get("metrics", {}))
        except DataFetchError as exc:
            raise SystemExit(f"Failed to fetch Jira data: {exc}")
    elif args.source == "csv":
        if not args.csv_path:
            raise SystemExit("--csv-path is required when --source csv is specified.")
        try:
            fetcher = CsvDataFetcher(args.csv_path)
            payload = fetcher.fetch()
            context["csv_data"] = payload
            context["metrics"].update({"csv_rows": payload.get("row_count", 0)})
        except DataFetchError as exc:
            raise SystemExit(f"Failed to load CSV data: {exc}")

    content = build_report(context)
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
