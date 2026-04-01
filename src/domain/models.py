from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(kw_only=True)
class LayoutMixin:
    """Shared visual and positioning properties assigned by the Layout Engine."""

    width: int = 120  # Default pixel width
    height: int = 120  # Default pixel height
    x: int = 0  # Absolute X coordinate
    y: int = 0  # Absolute Y coordinate


@dataclass(kw_only=True)
class Epic(LayoutMixin):
    """Level 3: The lowest level in the hierarchy."""

    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None  # e.g., "To Do", "In Progress", "Done"
    url: Optional[str] = None  # Link to Jira/GitHub ticket
    release: str = "Unassigned"  # Determines which swimlane this Epic falls into


@dataclass(kw_only=True)
class Feature(LayoutMixin):
    """Level 2: A feature belonging to a goal."""

    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    epics: List[Epic] = field(default_factory=list)


@dataclass(kw_only=True)
class Goal(LayoutMixin):
    """Level 1: A goal within the map."""

    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    features: List[Feature] = field(default_factory=list)


@dataclass(kw_only=True)
class Map(LayoutMixin):
    """Level 0: Map Root object that groups a whole map."""

    id: str
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    releases: List[str] = field(
        default_factory=list
    )  # Defines swimlane order (e.g., ["MVP", "v1.0"])
    goals: List[Goal] = field(default_factory=list)


@dataclass(kw_only=True)
class Workspace:
    """Top-level container to support importing and rendering multiple maps in parallel."""

    maps: List[Map] = field(default_factory=list)
