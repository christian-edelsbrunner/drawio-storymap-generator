import yaml
from src.domain.models import Workspace, Map, Goal, Feature, Epic, Theme


class StoryMapParseError(Exception):
    pass


class YamlParser:
    @staticmethod
    def parse(file_path: str) -> Workspace:
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise StoryMapParseError(f"Failed to read or parse YAML file: {e}")

        if not isinstance(data, dict):
            raise StoryMapParseError("Root of YAML must be a dictionary.")

        maps_data = data.get("maps", [])
        if not isinstance(maps_data, list):
            raise StoryMapParseError("'maps' must be a list.")

        workspace_maps = []
        for map_data in maps_data:
            workspace_maps.append(YamlParser._parse_map(map_data))

        theme_data = data.get("theme", {})
        theme = Theme()
        if theme_data:
            # We explicitly update the theme dataclass attributes if provided
            for key, value in theme_data.items():
                if hasattr(theme, key):
                    setattr(theme, key, value)

        return Workspace(maps=workspace_maps, theme=theme)

    @staticmethod
    def _parse_map(data: dict) -> Map:
        if "id" not in data or "title" not in data:
            raise StoryMapParseError("Map must have 'id' and 'title'.")

        goals_data = data.get("goals", [])
        goals = [YamlParser._parse_goal(g) for g in goals_data]

        return Map(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            url=data.get("url"),
            releases=data.get("releases", []),
            goals=goals,
        )

    @staticmethod
    def _parse_goal(data: dict) -> Goal:
        if "id" not in data or "title" not in data:
            raise StoryMapParseError("Goal must have 'id' and 'title'.")

        features_data = data.get("features", [])
        features = [YamlParser._parse_feature(f) for f in features_data]

        return Goal(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=data.get("status"),
            url=data.get("url"),
            features=features,
        )

    @staticmethod
    def _parse_feature(data: dict) -> Feature:
        if "id" not in data or "title" not in data:
            raise StoryMapParseError("Feature must have 'id' and 'title'.")

        epics_data = data.get("epics", [])
        epics = [YamlParser._parse_epic(e) for e in epics_data]

        return Feature(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=data.get("status"),
            url=data.get("url"),
            epics=epics,
        )

    @staticmethod
    def _parse_epic(data: dict) -> Epic:
        if "id" not in data or "title" not in data:
            raise StoryMapParseError("Epic must have 'id' and 'title'.")

        return Epic(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=data.get("status"),
            url=data.get("url"),
            release=data.get("release", "Unassigned"),
        )
