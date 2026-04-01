# Implementation Plan: Story Map Generator

### Task 1: Project Initialization & Domain Model
*   **Description:** Set up the Python project structure, manage dependencies, and implement the strictly typed Domain Model dataclasses.
*   **Implementation Hints:**
    *   Create a virtual environment and a `requirements.txt` (or use `poetry`/`pipenv`).
    *   Add foundational dependencies: `pytest` for testing.
    *   Create `src/domain/models.py`.
    *   Implement `LayoutMixin`, `Workspace`, `Map`, `Goal`, `Feature`, and `Epic` as Python `@dataclass` objects with strict type hinting.
*   **Acceptance Criteria:**
    *   Project folder structure is created (e.g., `src/`, `tests/`).
    *   `src/domain/models.py` contains all classes matching the documented domain model.
    *   A simple unit test file (`tests/test_domain.py`) successfully instantiates the models.

### Task 2: YAML Parser Adapter
*   **Description:** Implement the ingest adapter that reads a YAML file and converts it into the internal Domain Model.
*   **Implementation Hints:**
    *   Add `PyYAML` to dependencies.
    *   Create `src/adapters/yaml_parser.py` with a `YamlParser` class.
    *   Implement recursive parsing logic: iterate through Maps -> Goals -> Features -> Epics.
    *   Include validation logic to ensure required fields (like `id` and `title`) are present and hierarchy rules are respected.
*   **Acceptance Criteria:**
    *   `YamlParser.parse(file_path)` returns a fully populated `Workspace` object.
    *   Unit tests verify that a valid YAML string correctly maps to the expected Python objects.
    *   Clear exceptions (e.g., `StoryMapParseError`) are raised if the YAML structure is invalid.

### Task 3: Spatial Layout Engine Algorithm
*   **Description:** Build the core algorithmic engine that traverses the Domain Model and assigns `(x, y)` coordinates to every node.
*   **Implementation Hints:**
    *   Create `src/layout/engine.py`.
    *   Define constants for spacing (e.g., `PADDING_X = 20`, `PADDING_Y = 20`, `CARD_WIDTH = 120`).
    *   **Phase A (Backbone):** Calculate horizontal positions for Goals and Features. A Goal's width should encompass all its child Features.
    *   **Phase B (Swimlanes):** Calculate vertical row bounds based on the Map's `releases` array.
    *   **Phase C (Epics):** Place Epics at the intersection of their parent Feature's `X` coordinate and their assigned Release's `Y` coordinate.
*   **Acceptance Criteria:**
    *   The `LayoutEngine.calculate(workspace)` method mutates the objects, populating their `x`, `y`, `width`, and `height` properties.
    *   Unit tests assert that sibling Features do not overlap horizontally.
    *   Unit tests assert that Epics in the same swimlane align horizontally, and Epics under the same Feature align vertically.

### Task 4: Draw.io Renderer Adapter
*   **Description:** Implement the output adapter that takes the fully laid-out Domain Model and generates a `.drawio` diagram file.
*   **Implementation Hints:**
    *   Add `drawpyo` to dependencies (or use an XML builder library if generating raw draw.io XML is preferred for granular control).
    *   Create `src/adapters/drawio_renderer.py`.
    *   Map domain concepts to visual styles:
        *   Maps = Large container or header text.
        *   Goals/Features = Distinctly colored rectangles.
        *   Releases = Background horizontal swimlane rectangles or separator lines.
        *   Status = Dictates the fill color of the Epic cards.
    *   Apply the `url` property to make shapes clickable.
*   **Acceptance Criteria:**
    *   `DrawioRenderer.render(workspace, output_path)` creates a valid `.drawio` file.
    *   The generated file opens cleanly in draw.io/diagrams.net.
    *   All cards appear at their designated `(x, y)` coordinates without manual adjustment needed.

### Task 5: CLI Orchestration & E2E Integration
*   **Description:** Build the Command Line Interface to tie the Parser, Layout Engine, and Renderer together into a seamless user experience.
*   **Implementation Hints:**
    *   Use the standard library `argparse` or add `click` for a richer CLI experience.
    *   Create `src/cli.py` at the project root.
    *   Implement command arguments: `--input` (required) and `--output` (defaulting to the input filename with a `.drawio` extension).
    *   Wire the flow: `Parser -> Engine -> Renderer`.
*   **Acceptance Criteria:**
    *   User can run `python src/cli.py --input map.yaml --output my_map.drawio`.
    *   The command executes end-to-end and successfully generates the diagram.
    *   The CLI provides helpful error messages if the input file is missing or invalid.
