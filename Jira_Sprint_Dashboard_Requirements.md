# Jira Sprint Progress Dashboard Requirements

## Overview
Build a weekly Jira Cloud PDF report for SteerCo that highlights sprint health and blocked work, with charts and prior sprint context.

## Jira Access
- Jira Cloud base URL: `https://jiraeu.epam.com`
- Active board: `rapidView=279935`
- Project key: `EPMCDMETST`
- Authentication:
  - Atlassian email: `shalini_dulloor@epam.com`
  - API token: provided for implementation

## Frequency
- Weekly report generation

## Output Format
- PDF report
- Stakeholder-ready quality
- Includes charts, summary table, and appendix details

## Scope
- Current active sprint snapshot
- Comparison with prior 2 sprints
- Issue-count-based progress tracking

## Key Metrics
- Total issues
- Done issues
- Blocked issues
- Sprint completion %
- Remaining story/effort points
- Prior sprint trend/context

## Blocked Work
- Identify blocked items using a board status named `Blocked`
- Include aggregate blocked counts in the summary
- Include blocked issue details in an appendix

## Charts
- Burndown chart
- Blocked-work trend chart
- Completion pie chart

## Report Structure
1. Executive summary
2. Aggregate summary table
3. Chart section
4. Current sprint snapshot
5. Prior 2 sprint comparison
6. Blocked issue appendix

## User Experience
- Manual weekly execution
- Clear, concise visuals for SteerCo
- PDF output for distribution and review
