from src.domain.models import Workspace, Map, Theme


class LayoutEngine:
    @staticmethod
    def calculate(workspace: Workspace):
        theme = workspace.theme
        current_y = 0
        for story_map in workspace.maps:
            LayoutEngine._calculate_map(story_map, start_y=current_y, theme=theme)
            current_y = story_map.y + story_map.height + theme.padding_y * 2

    @staticmethod
    def _calculate_map(story_map: Map, start_y: int, theme: Theme):
        story_map.x = theme.padding_x
        story_map.y = start_y

        # We start laying out goals underneath the map title header
        current_x = theme.padding_x
        goal_start_y = start_y + theme.header_height + theme.padding_y

        # Backbone Layout (Goals and Features)
        for goal in story_map.goals:
            goal.x = current_x
            goal.y = goal_start_y

            feature_start_x = current_x
            feature_start_y = goal.y + theme.card_height + theme.padding_y

            goal_width = 0

            for feature in goal.features:
                feature.x = feature_start_x
                feature.y = feature_start_y
                feature_start_x += theme.card_width + theme.padding_x
                goal_width += theme.card_width + theme.padding_x

            if goal.features:
                goal.width = goal_width - theme.padding_x
                current_x = feature_start_x
            else:
                goal.width = theme.card_width
                current_x += theme.card_width + theme.padding_x

        # Swimlane Layout (Releases and Epics)
        # Determine unique releases across all epics in this map if not explicitly defined
        releases = story_map.releases.copy()
        for goal in story_map.goals:
            for feature in goal.features:
                for epic in feature.epics:
                    if epic.release not in releases:
                        releases.append(epic.release)

        # Ensure "Unassigned" is at the bottom if it appeared and wasn't specified
        if "Unassigned" in releases and releases[-1] != "Unassigned":
            releases.remove("Unassigned")
            releases.append("Unassigned")

        story_map.releases = releases

        swimlane_y = (
            goal_start_y
            + (theme.card_height + theme.padding_y) * 2
            + theme.swimlane_margin
        )
        swimlane_heights = {
            release: theme.card_height + theme.padding_y for release in releases
        }

        # First pass to find max height needed for each swimlane based on number of epics in a single feature column
        swimlane_feature_counts = {release: {} for release in releases}

        for goal in story_map.goals:
            for feature in goal.features:
                for epic in feature.epics:
                    if epic.release in swimlane_feature_counts:
                        swimlane_feature_counts[epic.release][feature.id] = (
                            swimlane_feature_counts[epic.release].get(feature.id, 0) + 1
                        )

        for release in releases:
            max_epics = 0
            if swimlane_feature_counts[release]:
                max_epics = max(swimlane_feature_counts[release].values())
            if max_epics > 0:
                swimlane_heights[release] = (
                    max_epics * (theme.card_height + theme.padding_y) + theme.padding_y
                )

        # Assign Epics to coordinates
        current_swimlane_y = swimlane_y
        swimlane_y_positions = {}
        for release in releases:
            swimlane_y_positions[release] = current_swimlane_y
            current_swimlane_y += swimlane_heights[release]

        for goal in story_map.goals:
            for feature in goal.features:
                epic_counts = {}
                for epic in feature.epics:
                    release = epic.release
                    epic_index = epic_counts.get(release, 0)
                    epic.x = feature.x
                    epic.y = swimlane_y_positions[release] + epic_index * (
                        theme.card_height + theme.padding_y
                    )
                    epic_counts[release] = epic_index + 1

        story_map.width = current_x - theme.padding_x - story_map.x
        story_map.height = current_swimlane_y - start_y
