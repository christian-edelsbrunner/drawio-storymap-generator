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
    assert "<b>[e1]</b><br/>SSO<br/><i>Done</i>" in user_obj.attrib["label"]

    # Find the Goal mxCell
    goal_cell = root.find(".//mxCell[@id='goal_g1']")
    assert goal_cell is not None
    assert "Users" in goal_cell.attrib["value"]
