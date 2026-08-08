# Module 08 Completion Report

## Tracked Files
.gitignore
Jira_Sprint_Dashboard_Requirements.md
PROJECT_IDEAS.md
README.md
bubble_sort.py
calculator.py
calculator/__init__.py
calculator/main.py
calculator/operations.py
csv_to_json.py
hello.txt
main.py
project_spec.md
test_report.md
weekly_status_report.py

## Spec Commit History
e0b3dde (HEAD -> main, origin/main, origin/HEAD) Add Jira dashboard requirements and project spec, update report automation

## project_spec.md Contents
# Project Specification: Weekly Delivery Report

## Overview
This project will deliver a clean, automated weekly PDF report for a Delivery Manager overseeing a 40-person T&M project.
The report is intended for SteerCo and all peers, with a focus on delivery health, blocked work, financial forecast, resource capacity, and quality risk.

## Objectives
- Provide a concise, stakeholder-ready weekly report in PDF format
- Surface sprint delivery progress and blocked work clearly
- Include prior sprint context for comparison
- Automate data collection where possible
- Maintain a secure credentials/configuration approach

## Primary Audience
- Delivery Manager
- Delivery leadership peers
- SteerCo
- Project team stakeholders

## Data Sources
### Primary
- Jira Cloud
  - Base URL: `https://jiraeu.epam.com`
  - Active board ID: `rapidView=279935`
  - Project key: `EPMCDMETST`
  - Authentication:
    - Atlassian email: `shalini_dulloor@epam.com`
    - API token: stored securely via environment variables

### Extensible Connectors
- Budget/forecast data: generic connector for finance or T&M system API, with CSV fallback if needed
- Capacity data: generic connector for timesheet or HR tool API, with CSV fallback
- QA data: generic connector for defect/test management tool API, with CSV fallback

## Report Frequency
- Weekly generation

## Output Format
- PDF report
- Stakeholder-ready formatting and structure
- Includes charts, tables, and appendix details

## Key Report Sections
1. Executive summary
2. Delivery progress/status
3. Risks and issues
4. Budget and forecast
5. Resource utilization
6. Quality and QA status
7. Prior sprint comparison
8. Blocked issue appendix

## Delivery Metrics
- Issue-count-based progress
- Total issues in sprint
- Done issues
- Blocked issues
- Sprint completion percentage
- Remaining story/effort points
- Current active sprint snapshot
- Prior 2 sprint comparison

## Blocked Work
- Blocked items identified by a status named `Blocked`
- Aggregate blocked count shown in summary table
- Blocked issue detail included as appendix
- Top blocked risks surfaced in summary

## Budget Metrics
- Actual vs planned T&M spend
- Burn rate
- Remaining budget
- Forecasted financial risk

## Resource Utilization Metrics
- Capacity percentage by role
- Billable vs non-billable hours
- Headcount and staffing mix

## Quality / QA Metrics
- Open defects by severity
- Regression or release risk indicators
- Test pass rate
- Quality incidents

## Charts and Visuals
- Burndown chart for the active sprint
- Blocked-work trend chart
- Completion pie chart
- Optional additional charts for budget burn, capacity by role, and QA severity

## Comparison Context
- Include the current active sprint plus prior 2 sprints
- Show trend lines for delivery and blocked work
- Provide comparative summary data for all three sprints

## Technical Design
### Architecture
- Data ingestion layer for Jira Cloud and generic connectors
- Processing layer to compute metrics, summaries, and chart data
- Presentation layer to render markdown and convert to PDF

### Security
- Store all credentials and connector settings via environment variables
- Avoid hard-coding secrets in source code
- If local configuration is needed, use a secured config file with restricted permissions

### Extensibility
- Design connectors for budget, capacity, and QA data as pluggable modules
- Default to Jira Cloud for delivery data, with fallback connectors for other domains
- Support CSV import as a fallback for non-API sources

## Functional Requirements
- FR1: Generate a weekly PDF report automatically from Jira Cloud delivery data
- FR2: Compute and display issue-count-based sprint progress
- FR3: Surface blocked issues and include a detailed appendix
- FR4: Compare the active sprint with the prior 2 sprints
- FR5: Include budget, capacity, and QA metrics via extensible connectors
- FR6: Render charts and tables in the final PDF
- FR7: Use secure environment variables for credentials

## Non-Functional Requirements
- NFR1: The report should be clean, concise, and appropriate for executive review
- NFR2: PDF generation must be reliable and repeatable
- NFR3: The system must keep credentials out of source control
- NFR4: The architecture must support future extension to additional data sources

## Implementation Notes
- Start with Jira Cloud delivery integration first
- Build a generic connector interface for finance/capacity/QA data
- Use environment variables for all secure settings
- Generate a Markdown intermediate if needed, then convert to PDF

## File to Save
- `project_spec.md` in project root
