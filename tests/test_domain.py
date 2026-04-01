import pytest
from src.domain.models import Workspace, Map, Goal, Feature, Epic


def test_domain_model_instantiation():
    epic1 = Epic(id="e1", title="SSO Integration", release="MVP")
    epic2 = Epic(id="e2", title="Password Reset", status="To Do")

    feature = Feature(id="f1", title="Auth", epics=[epic1, epic2])
    goal = Goal(id="g1", title="User Management", features=[feature])

    story_map = Map(
        id="m1", title="E-Commerce Launch", releases=["MVP", "Post-MVP"], goals=[goal]
    )

    workspace = Workspace(maps=[story_map])

    assert len(workspace.maps) == 1
    assert workspace.maps[0].title == "E-Commerce Launch"
    assert len(workspace.maps[0].goals) == 1
    assert workspace.maps[0].goals[0].title == "User Management"
    assert len(workspace.maps[0].goals[0].features) == 1
    assert len(workspace.maps[0].goals[0].features[0].epics) == 2
    assert workspace.maps[0].goals[0].features[0].epics[0].release == "MVP"


def test_layout_mixin_defaults():
    epic = Epic(id="e1", title="Test")
    assert epic.width == 120
    assert epic.height == 120
    assert epic.x == 0
    assert epic.y == 0
