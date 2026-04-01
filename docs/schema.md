# Story Map YAML Schema

The Story Map Generator expects a strictly defined YAML structure. This document outlines the required and optional fields for each hierarchical level, their default values, and specific behavioral logic (such as swimlane assignments).

## Root Level

The root of the YAML file must contain a `maps` list.

```yaml
maps:
  - # Map Object 1
  - # Map Object 2
```

---

## 1. Map (Level 0)

The top-level container for a single story map.

| Field | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String | **Yes** | - | Unique identifier for the map. |
| `title` | String | **Yes** | - | The display title (rendered as a header note). |
| `description` | String | No | `null` | Optional description of the map. |
| `url` | String | No | `null` | Optional URL. If provided, the title note becomes a clickable link. |
| `releases` | List[String] | No | `[]` | Defines the top-to-bottom order of the swimlanes (e.g., `["MVP", "v1.0", "Backlog"]`). |
| `goals` | List[Goal] | No | `[]` | List of Goal objects belonging to this map. |

### Swimlane Logic (`releases`)
* If you define the `releases` list, the generated diagram will render the swimlanes in that exact order from top to bottom.
* If an Epic specifies a `release` that is *not* in this list, the Layout Engine will automatically append it to the bottom of the map.
* If an Epic does not specify a `release` at all, it defaults to `"Unassigned"`. The `"Unassigned"` swimlane is always forced to the very bottom of the diagram.

---

## 2. Goal (Level 1)

Goals form the top horizontal backbone of the story map.

| Field | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String | **Yes** | - | Unique identifier. Displayed in brackets `[ID]`. |
| `title` | String | **Yes** | - | Display title. |
| `description` | String | No | `null` | Optional description. |
| `status` | String | No | `null` | Workflow status. |
| `url` | String | No | `null` | Optional URL. Makes the Goal note clickable. |
| `features` | List[Feature] | No | `[]` | List of Feature objects belonging to this goal. |

---

## 3. Feature (Level 2)

Features are grouped under Goals and form the vertical columns of the map.

| Field | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String | **Yes** | - | Unique identifier. Displayed in brackets `[ID]`. |
| `title` | String | **Yes** | - | Display title. |
| `description` | String | No | `null` | Optional description. |
| `status` | String | No | `null` | Workflow status. |
| `url` | String | No | `null` | Optional URL. Makes the Feature note clickable. |
| `epics` | List[Epic] | No | `[]` | List of Epic objects belonging to this feature. |

---

## 4. Epic (Level 3)

Epics are the executable units of work that drop down into the horizontal release swimlanes.

| Field | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String | **Yes** | - | Unique identifier. Displayed in brackets `[ID]`. |
| `title` | String | **Yes** | - | Display title. |
| `description` | String | No | `null` | Optional description. |
| `status` | String | No | `null` | Workflow status (e.g., "To Do", "Done"). Displayed as italic text on the card. |
| `url` | String | No | `null` | Optional URL. Makes the Epic note clickable. |
| `release` | String | No | `"Unassigned"` | The swimlane this Epic belongs to. Determines its horizontal row. |
