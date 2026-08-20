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


def test_parse_jira_csv_sets_urls_when_base_url_provided(tmp_path):
    csv_content = """Issue Key|Summary|Status|Issue Type|Outward issue link (relates)
INIT-1|Root|In Progress|Initiative|EPIC-1
EPIC-1|Auth|To Do|Epic|STORY-1
STORY-1|Login|To Do|Story|
"""
    file_path = tmp_path / "jira_urls.csv"
    file_path.write_text(csv_content)

    # Trailing slash should be normalized so both forms produce the same URL.
    workspace = JiraCsvParser.parse(
        str(file_path),
        hierarchy_issue_types=["Initiative", "Epic", "Story"],
        jira_base_url="https://jira.example.com/browse",
    )

    root_map = workspace.maps[0]
    assert root_map.url == "https://jira.example.com/browse/INIT-1"
    assert root_map.goals[0].url == "https://jira.example.com/browse/EPIC-1"
    assert root_map.goals[0].features[0].url == "https://jira.example.com/browse/STORY-1"


def test_parse_jira_csv_leaves_urls_none_without_base_url(tmp_path):
    csv_content = """Issue Key|Summary|Status|Issue Type|Outward issue link (relates)
INIT-1|Root|In Progress|Initiative|EPIC-1
EPIC-1|Auth|To Do|Epic|
"""
    file_path = tmp_path / "jira_no_urls.csv"
    file_path.write_text(csv_content)

    workspace = JiraCsvParser.parse(
        str(file_path),
        hierarchy_issue_types=["Initiative", "Epic"],
    )

    assert workspace.maps[0].url is None
    assert workspace.maps[0].goals[0].url is None


def test_parse_jira_csv_treats_relates_as_undirected(tmp_path):
    # The Jira "relates" link is symmetric; the CSV export splits it into
    # inward/outward columns depending on which side created the link.
    # Traversal must follow both directions so that a child linking "up" to
    # its parent (only inward on the parent's row) is still reachable when
    # descending from the parent.
    csv_content = """Issue Key|Summary|Status|Issue Type|Inward issue link (Relates)|Outward issue link (Relates)
INIT-1|Root|In Progress|Initiative|EPIC-1|EPIC-2
EPIC-1|Goal via inward|To Do|Epic||STORY-1
EPIC-2|Goal via outward|To Do|Epic||STORY-2
STORY-1|Feature A|To Do|Story||
STORY-2|Feature B|To Do|Story||
"""
    file_path = tmp_path / "jira_inward.csv"
    file_path.write_text(csv_content)

    workspace = JiraCsvParser.parse(
        str(file_path),
        hierarchy_issue_types=["Initiative", "Epic", "Story"],
    )

    assert len(workspace.maps) == 1
    goals = workspace.maps[0].goals
    # Both EPIC-1 (reached via inward link on INIT-1) and EPIC-2 (via outward)
    # must appear as goals under the initiative.
    assert [g.id for g in goals] == ["EPIC-1", "EPIC-2"]
    assert goals[0].features[0].id == "STORY-1"
    assert goals[1].features[0].id == "STORY-2"


def test_parse_jira_csv_fails_on_epic_linked_from_multiple_parents(tmp_path):
    csv_content = """Issue Key|Summary|Status|Issue Type|Outward issue link (relates)|Outward issue link (relates)
INIT-1|Root|In Progress|Initiative|EPIC-1|EPIC-2
EPIC-1|Goal A|To Do|Epic|STORY-1|
EPIC-2|Goal B|To Do|Epic|STORY-2|
STORY-1|Feature A|To Do|Story|TASK-1|
STORY-2|Feature B|To Do|Story|TASK-1|
TASK-1|Shared Epic|To Do|Task||
"""
    file_path = tmp_path / "jira_dup.csv"
    file_path.write_text(csv_content)

    with pytest.raises(StoryMapParseError) as excinfo:
        JiraCsvParser.parse(
            str(file_path),
            hierarchy_issue_types=["Initiative", "Epic", "Story", "Task"],
        )

    message = str(excinfo.value)
    assert "duplicate Draw.io node IDs" in message
    assert "Epic 'TASK-1'" in message
    assert "INIT-1 > EPIC-1 > STORY-1" in message
    assert "INIT-1 > EPIC-2 > STORY-2" in message


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
