# Feature Documentation

## MVP Features (Phase 1)

*   **F1. CLI Orchestration**: Command-line interface accepting `--input` (path to YAML) and `--output` (path to generated output).
*   **F2. Strict YAML Parsing**: Ingests nested YAML and validates it against the strict Domain Model (Workspace -> Map -> Goal -> Feature -> Epic).
*   **F3. Advanced Layout Algorithm**: 
    *   Renders the Map Title as a header at the top of the diagram.
    *   Renders Goals and Features horizontally to form the application backbone.
    *   Draws horizontal Swimlanes based on the Map's defined `releases` list.
    *   Places Epics in the intersection of their parent Feature's column and their assigned Release's row.
*   **F4. Draw.io Generation**: Renders the diagram visually into a Draw.io compatible format.
    *   Adds clickable links to shapes if a `url` is provided.
    *   Visually indicates `status` (e.g., displaying the status text directly on the card).

## Future Features (Phase 2+)

*   **F5. Additional Input Adapters**: Support for importing via JSON, Markdown lists, or direct API Integrations (e.g., Jira, GitHub Issues).
*   **F6. Additional Output Adapters**: Render to Mermaid.js, PlantUML, or standard image formats (PNG/SVG).
*   **F7. Web Interface / API (OCI Image)**: Wrap the core logic in a lightweight REST API (e.g., using FastAPI) bundled in a Docker container, allowing users to POST a payload and receive a diagram file download.
