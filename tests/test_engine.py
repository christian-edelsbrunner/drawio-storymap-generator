import pytest
from src.domain.models import Workspace, Map, Goal, Feature, Epic
from src.layout.engine import LayoutEngine


def test_layout_engine_backbone():
    epic1 = Epic(id="e1", title="SSO Integration", release="MVP")
    epic2 = Epic(id="e2", title="Password Reset", release="MVP")

    feature1 = Feature(id="f1", title="Auth", epics=[epic1, epic2])
    feature2 = Feature(id="f2", title="Profile", epics=[])

    goal = Goal(id="g1", title="User Management", features=[feature1, feature2])

    story_map = Map(
        id="m1", title="E-Commerce Launch", releases=["MVP", "Post-MVP"], goals=[goal]
    )
    workspace = Workspace(maps=[story_map])

    LayoutEngine.calculate(workspace)

    # Map title check
    assert story_map.x == LayoutEngine.PADDING_X
    assert story_map.y == 0

    # Goal check
    assert goal.x == LayoutEngine.PADDING_X
    assert goal.y == story_map.y + LayoutEngine.HEADER_HEIGHT + LayoutEngine.PADDING_Y
    assert goal.width == (LayoutEngine.CARD_WIDTH * 2) + LayoutEngine.PADDING_X

    # Feature checks (side-by-side)
    assert feature1.x == LayoutEngine.PADDING_X
    assert feature1.y == goal.y + LayoutEngine.CARD_HEIGHT + LayoutEngine.PADDING_Y

    assert feature2.x == feature1.x + LayoutEngine.CARD_WIDTH + LayoutEngine.PADDING_X
    assert feature2.y == feature1.y

    # Epic checks (stacked vertically in the MVP swimlane under feature1)
    swimlane_y = (
        feature1.y
        + LayoutEngine.CARD_HEIGHT
        + LayoutEngine.PADDING_Y
        + LayoutEngine.SWIMLANE_MARGIN
    )

    assert epic1.x == feature1.x
    assert epic1.y == swimlane_y

    assert epic2.x == feature1.x
    assert epic2.y == swimlane_y + LayoutEngine.CARD_HEIGHT + LayoutEngine.PADDING_Y

    assert story_map.width == goal.width
    assert story_map.height > 0
