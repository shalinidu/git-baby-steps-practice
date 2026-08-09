# Implementation Backlog

## Setup
- [x] Review existing repo files and current report generator implementation
- [ ] Confirm environment and dependency requirements for PDF generation (`markdown`, `weasyprint`, `pandoc`)
- [ ] Add `README` usage examples for report generation and environment setup
- [ ] Define environment variables for Jira credentials and board settings

## Core Features
- [ ] Implement Jira data ingestion for active sprint and issue status details
- [ ] Create report generation engine that renders stakeholder-ready markdown
- [ ] Add support for a weekly PDF report output
- [ ] Build the report structure with sections for executive summary, delivery progress, risks, budget, capacity, QA, blocked work, and sprint comparison
- [ ] Implement blocked issue aggregation and appendix details
- [ ] Add prior sprint comparison support for active sprint plus prior 2 sprints
- [ ] Add summary metrics for total issues, done issues, blocked issues, completion percentage, and remaining effort

## Integration
- [ ] Add a generic connector interface for finance, capacity, and QA data
- [ ] Implement CSV import fallback for non-API data sources
- [ ] Wire Jira and CSV data sources into the report generation workflow
- [ ] Wire CSV data sources into the report generation workflow
- [ ] Wire Jira data sources into the report generation workflow
- [ ] Ensure secure handling of environment variables and avoid hard-coded credentials
- [ ] Add a configuration module or pattern for extensible connector registration

## Testing
- [ ] Add unit tests for Jira data fetching and blocked issue identification
- [ ] Add unit tests for report builder output formatting
- [ ] Validate PDF generation under both Python package and Pandoc fallback paths
- [ ] Add test coverage for CSV fallback data ingestion
- [ ] Calculate the number of test cases generated and the total coverage
- [ ] Add error-handling tests for missing credentials and invalid CSV paths

## Documentation
- [ ] Document usage instructions in `README.md`
- [ ] Document environment variables and setup steps for Jira integration
- [ ] Document report sections and generated output expectations
- [ ] Add a developer notes section for extending connectors and adding new data sources
- [ ] Create a `backlog.md` file for phased implementation tracking
