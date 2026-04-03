import csv
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from src.adapters.yaml_parser import StoryMapParseError
from src.domain.models import Epic, Feature, Goal, Map, Workspace


_ISSUE_KEY_PATTERN = re.compile(r"[A-Z][A-Z0-9]+-\d+")


@dataclass
class _Issue:
    key: str
    summary: str
    status: Optional[str]
    issue_type: str
    outward_links: List[str]
    order: int


class JiraCsvParser:
    @staticmethod
    def parse(
        file_path: str, hierarchy_issue_types: Optional[List[str]] = None
    ) -> Workspace:
        issue_types = hierarchy_issue_types or [
            "Initiative",
            "Epic",
            "Story",
            "Task",
        ]
        issue_types = [t.strip() for t in issue_types if t and t.strip()]

        if not issue_types:
            raise StoryMapParseError("At least one hierarchy issue type must be provided.")
        if len(issue_types) > 4:
            raise StoryMapParseError(
                "Jira import supports up to 4 hierarchy levels (Map -> Goal -> Feature -> Epic)."
            )

        issues = JiraCsvParser._parse_issues(file_path)
        maps = JiraCsvParser._build_maps(issues, issue_types)
        return Workspace(maps=maps)

    @staticmethod
    def _parse_issues(file_path: str) -> Dict[str, _Issue]:
        try:
            with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.reader(f, delimiter="|")
                rows = list(reader)
        except Exception as e:
            raise StoryMapParseError(f"Failed to read or parse Jira CSV file: {e}")

        if not rows:
            raise StoryMapParseError("Jira CSV file is empty.")

        headers = [h.strip() for h in rows[0]]
        header_lower = [h.lower() for h in headers]

        def _find_required_column(name: str) -> int:
            try:
                return header_lower.index(name.lower())
            except ValueError:
                raise StoryMapParseError(f"Missing required Jira CSV column: '{name}'.")

        key_idx = _find_required_column("Issue Key")
        summary_idx = _find_required_column("Summary")
        status_idx = _find_required_column("Status")
        issue_type_idx = _find_required_column("Issue Type")

        outward_link_indexes = [
            i
            for i, header in enumerate(header_lower)
            if header == "outward issue link (relates)"
        ]

        issues: Dict[str, _Issue] = {}
        for order, row in enumerate(rows[1:], start=1):
            if not row:
                continue

            key = JiraCsvParser._cell(row, key_idx)
            if not key:
                continue

            summary = JiraCsvParser._cell(row, summary_idx)
            status = JiraCsvParser._cell(row, status_idx) or None
            issue_type = JiraCsvParser._cell(row, issue_type_idx)
            if not issue_type:
                continue

            outward_links: List[str] = []
            seen = set()
            for link_idx in outward_link_indexes:
                link_cell = JiraCsvParser._cell(row, link_idx)
                for linked_key in JiraCsvParser._extract_issue_keys(link_cell):
                    if linked_key not in seen:
                        seen.add(linked_key)
                        outward_links.append(linked_key)

            issues[key] = _Issue(
                key=key,
                summary=summary,
                status=status,
                issue_type=issue_type,
                outward_links=outward_links,
                order=order,
            )

        return issues

    @staticmethod
    def _build_maps(issues: Dict[str, _Issue], issue_types: List[str]) -> List[Map]:
        roots = sorted(
            [issue for issue in issues.values() if issue.issue_type == issue_types[0]],
            key=lambda issue: issue.order,
        )

        maps: List[Map] = []
        for root in roots:
            goals = []
            if len(issue_types) >= 2:
                level_1_issues = JiraCsvParser._linked_by_type(issues, root, issue_types[1])
                goals = [
                    JiraCsvParser._build_goal(issues, level_1_issue, issue_types)
                    for level_1_issue in level_1_issues
                ]

            maps.append(
                Map(
                    id=root.key,
                    title=root.summary or root.key,
                    description=None,
                    goals=goals,
                    releases=[],
                )
            )

        return maps

    @staticmethod
    def _build_goal(issues: Dict[str, _Issue], issue: _Issue, issue_types: List[str]) -> Goal:
        features = []
        if len(issue_types) >= 3:
            level_2_issues = JiraCsvParser._linked_by_type(issues, issue, issue_types[2])
            features = [
                JiraCsvParser._build_feature(issues, level_2_issue, issue_types)
                for level_2_issue in level_2_issues
            ]

        return Goal(
            id=issue.key,
            title=issue.summary or issue.key,
            status=issue.status,
            features=features,
        )

    @staticmethod
    def _build_feature(
        issues: Dict[str, _Issue], issue: _Issue, issue_types: List[str]
    ) -> Feature:
        epics = []
        if len(issue_types) >= 4:
            level_3_issues = JiraCsvParser._linked_by_type(issues, issue, issue_types[3])
            epics = [
                Epic(
                    id=level_3_issue.key,
                    title=level_3_issue.summary or level_3_issue.key,
                    status=level_3_issue.status,
                    release="Unassigned",
                )
                for level_3_issue in level_3_issues
            ]

        return Feature(
            id=issue.key,
            title=issue.summary or issue.key,
            status=issue.status,
            epics=epics,
        )

    @staticmethod
    def _linked_by_type(
        issues: Dict[str, _Issue], source_issue: _Issue, expected_type: str
    ) -> List[_Issue]:
        linked: List[_Issue] = []
        seen = set()
        for linked_key in source_issue.outward_links:
            linked_issue = issues.get(linked_key)
            if (
                linked_issue
                and linked_issue.issue_type == expected_type
                and linked_issue.key not in seen
            ):
                seen.add(linked_issue.key)
                linked.append(linked_issue)
        return linked

    @staticmethod
    def _extract_issue_keys(value: str) -> List[str]:
        if not value:
            return []
        keys = _ISSUE_KEY_PATTERN.findall(value.upper())
        if keys:
            return keys
        raw_value = value.strip()
        return [raw_value] if raw_value else []

    @staticmethod
    def _cell(row: List[str], index: int) -> str:
        if index < 0 or index >= len(row):
            return ""
        return row[index].strip()
