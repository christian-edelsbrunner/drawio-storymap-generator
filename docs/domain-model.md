# Domain Model

The Story Map Generator uses a strict hierarchical domain model represented by Python Dataclasses. This ensures that the data structure is well-defined and validated before any layout calculations or rendering occur.

## Hierarchy Overview

1.  **Workspace**: The top-level container holding multiple Maps.
2.  **Map (Level 0)**: The root object for a single story map.
3.  **Goal (Level 1)**: High-level objectives that form the backbone.
4.  **Feature (Level 2)**: Groupings of specific functionalities under a Goal.
5.  **Epic (Level 3)**: The lowest level representing deliverable units of work.

## Class Definitions

### LayoutMixin
All visual elements inherit from `LayoutMixin` to store coordinates calculated by the Layout Engine.

```python
@dataclass
class LayoutMixin:
    width: int = 120   # Default pixel width
    height: int = 60   # Default pixel height
    x: int = 0         # Absolute X coordinate
    y: int = 0         # Absolute Y coordinate
```

### Epic (Level 3)
The lowest level item. Placed into swimlanes (releases).

```python
@dataclass
class Epic(LayoutMixin):
    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None   # e.g., "To Do", "In Progress", "Done"
    url: Optional[str] = None      # Link to Jira/GitHub ticket
    release: str = "Unassigned"    # Determines the horizontal swimlane
```

### Feature (Level 2)
A feature belonging to a goal. Placed horizontally under its parent goal.

```python
@dataclass
class Feature(LayoutMixin):
    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    epics: List[Epic] = field(default_factory=list)
```

### Goal (Level 1)
A high-level goal forming the top "backbone" of the story map.

```python
@dataclass
class Goal(LayoutMixin):
    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    features: List[Feature] = field(default_factory=list)
```

### Map (Level 0)
The root object for a story map.

```python
@dataclass
class Map(LayoutMixin):
    id: str
    title: str
    description: Optional[str] = None
    releases: List[str] = field(default_factory=list) # Defines swimlane vertical order (e.g., ["MVP", "v1.0"])
    goals: List[Goal] = field(default_factory=list)
```

### Workspace
The top-level container supporting multiple maps in parallel.

```python
@dataclass
class Workspace:
    maps: List[Map] = field(default_factory=list)
```
