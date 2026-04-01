# Agents Concept

To enhance the Story Map Generator, we can introduce AI Agents to assist in the creation, refinement, and management of story maps. These agents will operate on the strictly typed Domain Model or the raw YAML input to automate planning tasks.

## 🤖 Agent Roles

### 1. The "Ideation" Agent (Generator)
**Purpose:** Bootstrap a new project by generating a complete, draft Story Map from a simple text prompt.
*   **Input:** A high-level description (e.g., "An e-commerce mobile app for selling shoes").
*   **Output:** A structured YAML string adhering to our Domain Model schema (Maps, Goals, Features, Epics, and placeholder Releases like "MVP" and "v2.0").
*   **Benefit:** Overcomes the "blank page" problem and provides a solid starting point for the user to tweak.

### 2. The "Refinement" Agent (Reviewer)
**Purpose:** Analyze an existing Story Map and suggest improvements, missing pieces, or structural changes.
*   **Input:** The current Domain Model (parsed from the user's YAML).
*   **Output:** Suggestions for new Features/Epics that might have been forgotten (e.g., "I noticed you have User Registration, but no Password Reset feature. Would you like me to add it?").
*   **Benefit:** Ensures completeness and acts as a "second pair of eyes" for the product owner.

### 3. The "Slicer" Agent (Release Planner)
**Purpose:** Help categorize Epics into sensible Releases (Swimlanes) based on dependencies and MVP requirements.
*   **Input:** A Story Map where Epics have an "Unassigned" release.
*   **Output:** An updated Story Map where Epics are distributed across "MVP", "Phase 2", etc., based on logical product evolution.
*   **Benefit:** Automates the tedious task of prioritization and MVP scoping.

## 🏗️ Architecture Integration

To support Agents, we will introduce an **Agent Layer** that acts as an optional pre-processor or post-processor around the Core Flow:

`Prompt -> [Ideation Agent] -> YAML -> Parser -> Domain Model -> [Refinement Agent] -> Layout Engine -> Output`

*   The agents will interact with LLM APIs (e.g., OpenAI, Anthropic).
*   We will provide the agents with strict JSON Schemas matching our Python Dataclasses to ensure they generate valid structures that our `YamlParser` can easily digest.
