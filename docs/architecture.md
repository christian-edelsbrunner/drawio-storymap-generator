# Software Architecture

## Architectural Style
The application follows a **Ports and Adapters (Hexagonal) / Pipeline** architecture. This ensures that the core domain logic (representing a Story Map) is completely decoupled from how the data is ingested (YAML, API, JSON) and how it is rendered (Draw.io, Mermaid, etc.).

## Core Flow
`Input Data -> Parser (Adapter) -> Domain Model -> Layout Engine -> Renderer (Adapter) -> Output Diagram`

## Components

### 1. Core Domain (`domain/`)
Strictly typed Python Dataclasses that represent the business concepts of a Story Map. The domain has no knowledge of YAML or Draw.io.

*   **Workspace**: Top-level container to support multiple maps in parallel.
*   **Map (Level 0)**: Root object grouping a whole map. Contains `releases` to define swimlane order.
*   **Goal (Level 1)**: Forms the primary backbone. Contains `Feature`s.
*   **Feature (Level 2)**: Grouping under Goals. Contains `Epic`s.
*   **Epic (Level 3)**: The lowest level in the hierarchy, placed into swimlanes (releases).

*Shared Properties*: All levels inherit layout properties (x, y, width, height) and can have attributes like `status` and `url`.

### 2. Ports / Interfaces
*   `ParserInterface`: Defines the contract for translating raw input into the Domain Model.
*   `RendererInterface`: Defines the contract for generating visual outputs from the layout-assigned Domain Model.

### 3. Adapters
*   `YamlParser`: Parses YAML hierarchies into strict domain objects, validating the structure.
*   `DrawioRenderer`: Uses `drawpyo` (or raw XML generation) to create the `.drawio` file, styling boxes based on type, status, and swimlanes.

### 4. Layout Engine (`layout/`)
The algorithmic heart of the application. It traverses the Domain Model and calculates `(x, y)` coordinates for every node.
*   **Grid System**: Calculates bounding boxes for Maps, Goals, and Features to form the top "backbone".
*   **Swimlane System**: Calculates horizontal row boundaries for each "Release" and places Epics in the correct column (under their Feature) and correct row (inside their Release swimlane).

### 5. CLI Application (`cli.py`)
The entry point that orchestrates the flow, parsing command-line arguments and wiring the chosen Parser to the Layout Engine and then to the chosen Renderer.
