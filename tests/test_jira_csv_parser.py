import pytest

from src.adapters.jira_csv_parser import JiraCsvParser
from src.adapters.yaml_parser import StoryMapParseError


def test_parse_jira_csv_builds_multiple_maps_and_hierarchy(tmp_path):
    csv_content = """Issue Key|Summary|Status|Issue Type|Outward issue link (relates)|Outward issue link (relates)
INIT-1|Checkout Revamp|In Progress|Initiative|EPIC-1|EPIC-2
INIT-2|Account Area|To Do|Initiative|EPIC-3|
EPIC-1|Authentication|To Do|Epic|STORY-1|
EPIC-2|Cart|In Progress|Epic|STORY-2|
EPIC-3|Profile|Done|Epic|STORY-3|
STORY-1|SSO Login|In Progress|Story|TASK-1|
STORY-2|Save Basket|To Do|Story|TASK-2|
STORY-3|Edit Profile|Done|Story|TASK-3|
TASK-1|Implement OAuth|To Do|Task||
TASK-2|Persist Cart|In Progress|Task||
TASK-3|Update Avatar|Done|Task||
"""
    file_path = tmp_path / "jira.csv"
    file_path.write_text(csv_content)

    workspace = JiraCsvParser.parse(
        str(file_path), hierarchy_issue_types=["Initiative", "Epic", "Story", "Task"]
    )

    assert len(workspace.maps) == 2
    assert workspace.maps[0].id == "INIT-1"
    assert workspace.maps[1].id == "INIT-2"

    map_1 = workspace.maps[0]
    assert [g.id for g in map_1.goals] == ["EPIC-1", "EPIC-2"]
    assert map_1.goals[0].features[0].id == "STORY-1"
    assert map_1.goals[0].features[0].epics[0].id == "TASK-1"
    assert map_1.goals[0].features[0].epics[0].status == "To Do"
    assert len(map_1.goals) == 2

    map_2 = workspace.maps[1]
    assert [g.id for g in map_2.goals] == ["EPIC-3"]
    assert map_2.goals[0].features[0].epics[0].id == "TASK-3"


def test_parse_jira_csv_missing_required_column_raises(tmp_path):
    csv_content = """Issue Key|Summary|Status|Outward issue link (relates)
INIT-1|Checkout Revamp|In Progress|EPIC-1
"""
    file_path = tmp_path / "jira_missing_column.csv"
    file_path.write_text(csv_content)

    with pytest.raises(StoryMapParseError) as excinfo:
        JiraCsvParser.parse(str(file_path))

    assert "Missing required Jira CSV column: 'Issue Type'" in str(excinfo.value)


def test_parse_jira_csv_supports_shorter_hierarchy(tmp_path):
    csv_content = """Issue Key|Summary|Status|Issue Type|Outward issue link (relates)
EPIC-1|Authentication|To Do|Epic|STORY-1
STORY-1|SSO Login|In Progress|Story|TASK-1
TASK-1|Implement OAuth|To Do|Task|
"""
    file_path = tmp_path / "jira_short.csv"
    file_path.write_text(csv_content)

    workspace = JiraCsvParser.parse(str(file_path), hierarchy_issue_types=["Epic", "Story"])

    assert len(workspace.maps) == 1
    assert workspace.maps[0].id == "EPIC-1"
    assert [goal.id for goal in workspace.maps[0].goals] == ["STORY-1"]


def test_parse_jira_csv_supports_multiple_types_per_level(tmp_path):
    csv_content = """Issue Key|Summary|Status|Issue Type|Outward issue link (relates)|Outward issue link (relates)
INIT-1|Commerce Platform|In Progress|Initiative|EPIC-1|CAP-1
EPIC-1|Authentication|To Do|Epic|STORY-1|
CAP-1|Catalog Backbone|To Do|Capability|STORY-2|
STORY-1|Login Story|To Do|Story|TASK-1|
STORY-2|Browse Story|To Do|User Story|TASK-2|
TASK-1|Build login|To Do|Task||
TASK-2|Build browse|To Do|Sub-task||
"""
    file_path = tmp_path / "jira_multitype.csv"
    file_path.write_text(csv_content)

    hierarchy = "Initiative,Epic/Capability,Story/User Story,Task/Sub-task"
    workspace = JiraCsvParser.parse(str(file_path), hierarchy_issue_types=hierarchy)

    assert len(workspace.maps) == 1
    goals = workspace.maps[0].goals
    assert [g.id for g in goals] == ["EPIC-1", "CAP-1"]
    assert goals[0].features[0].epics[0].id == "TASK-1"
    assert goals[1].features[0].epics[0].id == "TASK-2"


def test_load_hierarchy_issue_types_from_config(tmp_path):
    config_content = """
hierarchy_issue_types:
  - ["Initiative"]
  - ["Epic", "Capability"]
  - ["Story", "User Story"]
  - ["Task", "Sub-task"]
"""
    config_path = tmp_path / "hierarchy.yaml"
    config_path.write_text(config_content)

    parsed = JiraCsvParser.load_hierarchy_issue_types_from_config(str(config_path))
    assert parsed == [
        ["Initiative"],
        ["Epic", "Capability"],
        ["Story", "User Story"],
        ["Task", "Sub-task"],
    ]
