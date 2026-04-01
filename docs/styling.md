# Story Map Generator Styling

The Story Map Generator automatically applies consistent styling and color-coding to the generated Draw.io diagrams to visually distinguish between the different hierarchical elements of the Story Map.

## Color Palette

The following hex color codes are used to visually identify the *type* of card or element:

*   **Map Background / Header**: `#f5f5f5` (Light Gray)
*   **Goals (Top Level, Backbone)**: `#dae8fc` (Light Blue)
*   **Features (Second Level)**: `#d5e8d4` (Light Green)
*   **Epics (Third Level)**: `#ffe6cc` (Light Orange/Peach)
*   **Swimlane Lines/Background**: `#fff2cc` (Light Yellow/Gold)

*(Note: Colors are purely structural and do not represent the workflow status of an item).*

## Card Content formatting

All cards in the Story Map follow a consistent content formatting standard:

### Goals and Features
These cards form the structural backbone and display their ID and Title.
*   **Format**: `[ID]` (bold) on the first line, followed by the `Title` (bold) on the second line.
*   **Example**: 
    ```
    [GOAL-1]
    User Management
    ```

### Epics
These are the executable units of work located within the swimlanes. They contain additional workflow information.
*   **Format**: `[ID]` (bold) on the first line, followed by the `Title` (normal text) on the second line, and optionally the `Status` (italicized) on the third line.
*   **Example**:
    ```
    [PROJ-1]
    SSO Integration
    Done
    ```
