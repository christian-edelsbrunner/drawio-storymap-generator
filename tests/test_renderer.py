# @ai-generated: gemini-3.1-pro
import pytest
import os
import xml.etree.ElementTree as ET
from src.domain.models import Workspace, Map, Goal, Feature, Epic
from src.layout.engine import LayoutEngine
from src.adapters.drawio_renderer import DrawioRenderer


def test_drawio_renderer(tmp_path):
    epic1 = Epic(
        id="e1", title="SSO", url="http://jira/1", status="Done", release="MVP"
    )
    feature1 = Feature(id="f1", title="Auth", epics=[epic1])
    goal1 = Goal(id="g1", title="Users", features=[feature1])
    story_map = Map(id="m1", title="My Map", releases=["MVP"], goals=[goal1])
    workspace = Workspace(maps=[story_map])

    LayoutEngine.calculate(workspace)

    output_file = tmp_path / "output.drawio"
    DrawioRenderer.render(workspace, str(output_file))

    assert output_file.exists()

    # Parse XML and verify
    tree = ET.parse(str(output_file))
    root = tree.getroot()
    assert root.tag == "mxfile"

    # Find the Epic UserObject (due to URL)
    user_obj = root.find(".//UserObject[@id='epic_e1']")
    assert user_obj is not None
    assert user_obj.attrib["link"] == "http://jira/1"

    label = user_obj.attrib["label"]
    # Jira-card style: title text is present, plus status + ID pills.
    assert "SSO" in label
    assert "[e1]" in label
    assert "Done" in label
    # Atlassian "Done" lozenge colors
    assert "#E3FCEF" in label  # green background
    assert "#006644" in label  # green foreground
    # ID pill uses Atlassian link blue
    assert "#DEEBFF" in label
    assert "#0747A6" in label

    # Find the Goal mxCell - should also use Jira-card style
    goal_cell = root.find(".//mxCell[@id='goal_g1']")
    assert goal_cell is not None
    goal_label = goal_cell.attrib["value"]
    assert "Users" in goal_label
    assert "[g1]" in goal_label
    # Goal card style should be rounded (not shape=note anymore)
    assert "rounded=1" in goal_cell.attrib["style"]
    assert "shape=note" not in goal_cell.attrib["style"]
