# Drawpyo Agent Skill

## Overview
`drawpyo` is a Python library for programmatically generating Draw.io charts. It allows you to create files, pages, objects (nodes), and edges (connections), apply styles, and save them as `.drawio` files that can be opened in the Draw.io application.

## Core Concepts

### 1. Files and Pages
Every diagram starts with a File and a Page. A file can contain multiple pages.

```python
import drawpyo

# Create a File
file = drawpyo.File()
file.file_path = "./diagrams"
file.file_name = "my_diagram.drawio"

# Create a Page attached to the file
page = drawpyo.Page(file=file)
```

### 2. Objects (Nodes)
Objects represent the shapes in your diagram.

**Basic Object:**
```python
# Create a basic object (rounded rectangle by default)
my_obj = drawpyo.diagram.Object(page=page)
my_obj.value = "Hello World" # Text displayed inside the object

# Sizing
my_obj.width = 120
my_obj.height = 80

# Positioning (Top Left or Center)
my_obj.position = (0, 0) # Top Left
# OR
my_obj.center_position = (100, 100) # Center
```

**Objects from Libraries:**
Draw.io has built-in libraries (like "general" or "flowchart"). You can instantiate pre-styled objects from these libraries.
```python
process_obj = drawpyo.diagram.object_from_library(
    library="general",
    obj_name="process",
    page=page
)
process_obj.value = "Process Step"
```

### 3. Edges (Connections)
Edges connect objects together.

```python
# Connect two objects
link = drawpyo.diagram.Edge(
    page=page,
    source=obj_1,
    target=obj_2
)

# Set a label for the edge
link.label = "connects to"
```

### 4. Programmatic Styling
Since we want to generate diagrams purely programmatically without relying on manual Draw.io GUI steps, you should set all styling properties directly as attributes on the Object and Edge instances.

**Object Styling Attributes:**
```python
my_obj.fillColor = "#dae8fc"
my_obj.strokeColor = "#6c8ebf"
my_obj.strokeWidth = 2
my_obj.opacity = 80       # 0 to 100
my_obj.rounded = 1        # Boolean toggle (0 or 1)
my_obj.shadow = 1         # Boolean toggle
my_obj.glass = 1          # Boolean toggle
my_obj.whiteSpace = "wrap"
```

**Edge Styling Attributes:**
```python
link.strokeColor = "#FF0000"
link.strokeWidth = 2
link.waypoint = "orthogonal"     # Routing: straight, orthogonal, curved, etc.
link.connection = "line"         # Type: line, link, arrow, simple_arrow
link.pattern = "dashed_medium"   # solid, dashed_small, dotted_large, etc.
link.line_end_target = "classic" # block, open, oval, diamond, etc.
link.jumpStyle = "arc"           # Line jump intersections (arc, gap, sharp, line)
```

## Workflow for Generating a Diagram

1. Initialize `drawpyo.File()` and `drawpyo.Page()`.
2. Instantiate `drawpyo.diagram.Object`s (or use `object_from_library`).
3. Set their `.value`, sizes (`.width`, `.height`), and positions (`.position` or `.center_position`).
4. Instantiate `drawpyo.diagram.Edge`s linking `source` and `target` objects.
5. Apply styling purely programmatically via direct attribute assignments on objects and edges.
6. Call `file.write()` to generate the `.drawio` output file.

```python
# Example Complete Workflow
import drawpyo

file = drawpyo.File()
file.file_name = "example.drawio"
page = drawpyo.Page(file=file)

node_a = drawpyo.diagram.Object(page=page)
node_a.value = "Node A"
node_a.position = (10, 10)
node_a.fillColor = "#d5e8d4"
node_a.strokeColor = "#82b366"

node_b = drawpyo.diagram.Object(page=page)
node_b.value = "Node B"
node_b.position = (200, 10)
node_b.fillColor = "#f8cecc"
node_b.strokeColor = "#b85450"

edge = drawpyo.diagram.Edge(page=page, source=node_a, target=node_b)
edge.label = "Flows to"
edge.waypoint = "orthogonal"
edge.strokeWidth = 2
edge.pattern = "dashed_medium"

file.write()
```

## Best Practices
- **Auto-Routing:** When defining an edge without explicitly setting entry/exit coordinates (`entryX`, `exitY`, etc.), drawpyo relies on the Draw.io engine's auto-routing when you open the file, ensuring lines look clean automatically.
- **Purely Programmatic:** Define a set of standard styling dictionaries in your script and apply them programmatically to maintain consistency across shapes instead of copying raw style strings. For example:
  ```python
  success_style = {"fillColor": "#d5e8d4", "strokeColor": "#82b366", "rounded": 1}
  for k, v in success_style.items():
      setattr(node_a, k, v)
  ```