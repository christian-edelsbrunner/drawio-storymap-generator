import pytest
import yaml
import os
from src.adapters.yaml_parser import YamlParser, StoryMapParseError


def test_parse_valid_yaml(tmp_path):
    yaml_content = """
maps:
  - id: m1
    title: "E-Commerce Launch"
    releases: ["MVP", "Q3 Release", "Backlog"]
    goals:
      - id: g1
        title: "User Management"
        features:
          - id: f1
            title: "Authentication"
            status: "In Progress"
            epics:
              - id: e1
                title: "SSO Integration"
                status: "Done"
                url: "https://jira.com/ticket-1"
                release: "MVP"
              - id: e2
                title: "Password Reset Flow"
                status: "To Do"
                url: "https://jira.com/ticket-2"
                release: "Q3 Release"
"""
    file_path = tmp_path / "test_map.yaml"
    file_path.write_text(yaml_content)

    workspace = YamlParser.parse(str(file_path))

    assert len(workspace.maps) == 1
    m1 = workspace.maps[0]
    assert m1.id == "m1"
    assert m1.title == "E-Commerce Launch"
    assert m1.releases == ["MVP", "Q3 Release", "Backlog"]

    assert len(m1.goals) == 1
    g1 = m1.goals[0]
    assert g1.id == "g1"
    assert g1.title == "User Management"

    assert len(g1.features) == 1
    f1 = g1.features[0]
    assert f1.id == "f1"
    assert f1.title == "Authentication"
    assert f1.status == "In Progress"

    assert len(f1.epics) == 2
    e1 = f1.epics[0]
    assert e1.id == "e1"
    assert e1.title == "SSO Integration"
    assert e1.status == "Done"
    assert e1.url == "https://jira.com/ticket-1"
    assert e1.release == "MVP"


def test_parse_invalid_yaml_missing_id(tmp_path):
    yaml_content = """
maps:
  - title: "Missing ID Map"
"""
    file_path = tmp_path / "test_map_invalid.yaml"
    file_path.write_text(yaml_content)

    with pytest.raises(StoryMapParseError) as excinfo:
        YamlParser.parse(str(file_path))
    assert "Map must have 'id' and 'title'" in str(excinfo.value)
