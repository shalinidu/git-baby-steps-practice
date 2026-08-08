import csv
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

DEFAULT_JIRA_BASE_URL = "https://jiraeu.epam.com"
DEFAULT_JIRA_BOARD_ID = "279935"
DEFAULT_JIRA_PROJECT_KEY = "EPMCDMETST"


class DataFetchError(RuntimeError):
    pass


class BaseDataFetcher:
    def fetch(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement fetch()")


class JiraDataFetcher(BaseDataFetcher):
    def __init__(
        self,
        base_url: Optional[str] = None,
        board_id: Optional[str] = None,
        project_key: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        self.base_url = (base_url or os.environ.get("JIRA_BASE_URL") or DEFAULT_JIRA_BASE_URL).rstrip("/")
        self.board_id = self._normalize_board_id(
            board_id or os.environ.get("JIRA_BOARD_ID") or DEFAULT_JIRA_BOARD_ID
        )
        self.project_key = project_key or os.environ.get("JIRA_PROJECT_KEY") or DEFAULT_JIRA_PROJECT_KEY
        self.email = email or os.environ.get("JIRA_EMAIL")
        self.api_token = api_token or os.environ.get("JIRA_API_TOKEN")

        if not self.email or not self.api_token:
            raise DataFetchError(
                "Jira credentials are missing. Set JIRA_EMAIL and JIRA_API_TOKEN in your environment."
            )

        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.session = requests.Session()
        self.session.auth = self.auth

    @staticmethod
    def _normalize_board_id(board_id: str) -> str:
        match = re.search(r"\d+", board_id)
        if not match:
            raise DataFetchError(f"Invalid Jira board identifier: {board_id}")
        return match.group(0)

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.get(url, params=params or {}, timeout=20)
            response.raise_for_status()
        except RequestException as exc:
            raise DataFetchError(f"Jira request failed: {exc}") from exc
        return response.json()

    def fetch_active_sprint(self) -> Dict[str, Any]:
        payload = self._request(f"/rest/agile/1.0/board/{self.board_id}/sprint", params={"state": "active"})
        sprints = payload.get("values") or []
        if not sprints:
            raise DataFetchError("No active sprint found for the configured board.")
        return sprints[0]

    def fetch_sprint_issues(self, sprint_id: int) -> List[Dict[str, Any]]:
        fields = "summary,status,issuetype,assignee"
        payload = self._request(
            f"/rest/agile/1.0/sprint/{sprint_id}/issue",
            params={"fields": fields, "maxResults": 1000},
        )
        return payload.get("issues", [])

    def fetch(self) -> Dict[str, Any]:
        sprint = self.fetch_active_sprint()
        issues = self.fetch_sprint_issues(sprint_id=int(sprint["id"]))
        blocked_issues = [issue for issue in issues if self._is_blocked(issue)]
        done_issues = [issue for issue in issues if self._is_done(issue)]

        metrics = {
            "board_id": self.board_id,
            "project_key": self.project_key,
            "active_sprint": sprint.get("name"),
            "sprint_id": sprint.get("id"),
            "total_issues": len(issues),
            "done_issues": len(done_issues),
            "blocked_issues": len(blocked_issues),
            "completion_pct": round((len(done_issues) / len(issues) * 100) if issues else 0, 1),
        }

        return {
            "source": "jira",
            "jira": {
                "base_url": self.base_url,
                "board_id": self.board_id,
                "project_key": self.project_key,
                "sprint": sprint,
                "issues": issues,
                "blocked_issues": blocked_issues,
            },
            "metrics": metrics,
        }

    @staticmethod
    def _extract_status_name(issue: Dict[str, Any]) -> str:
        return str(issue.get("fields", {}).get("status", {}).get("name", "")).strip()

    @classmethod
    def _is_blocked(cls, issue: Dict[str, Any]) -> bool:
        return cls._extract_status_name(issue).lower() == "blocked"

    @classmethod
    def _is_done(cls, issue: Dict[str, Any]) -> bool:
        return cls._extract_status_name(issue).lower() == "done"


class CsvDataFetcher(BaseDataFetcher):
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise DataFetchError(f"CSV file does not exist: {csv_path}")

    def fetch(self) -> Dict[str, Any]:
        with self.csv_path.open("r", encoding="utf-8", newline="") as input_file:
            reader = csv.DictReader(input_file)
            rows = list(reader)
        return {
            "source": "csv",
            "csv_path": str(self.csv_path),
            "rows": rows,
            "row_count": len(rows),
            "headers": reader.fieldnames or [],
        }


if __name__ == "__main__":
    try:
        fetcher = JiraDataFetcher()
        payload = fetcher.fetch()
        print("Jira sprint data fetched successfully:")
        for key, value in payload["metrics"].items():
            print(f"- {key}: {value}")
    except DataFetchError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
