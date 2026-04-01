import xml.etree.ElementTree as ET
import os
from src.domain.models import Workspace


class DrawioRenderer:
    COLORS = {
        "map": "#f5f5f5",
        "goal": "#dae8fc",
        "feature": "#d5e8d4",
        "epic": "#ffe6cc",
        "swimlane": "#fff2cc",
    }

    @staticmethod
    def render(workspace: Workspace, output_path: str):
        mxfile = ET.Element(
            "mxfile", host="StoryMapGenerator", version="21.6.5", type="device"
        )
        diagram = ET.SubElement(mxfile, "diagram", name="Story Map", id="story_map_1")
        mxGraphModel = ET.SubElement(
            diagram,
            "mxGraphModel",
            dx="1000",
            dy="1000",
            grid="1",
            gridSize="10",
            guides="1",
            toolTips="1",
            connect="1",
            arrows="1",
            fold="1",
            page="1",
            pageScale="1",
            pageWidth="1100",
            pageHeight="850",
            math="0",
            shadow="0",
        )
        root = ET.SubElement(mxGraphModel, "root")

        # Root cells
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        for story_map in workspace.maps:
            # Map Title
            DrawioRenderer._create_cell(
                root=root,
                id=f"map_{story_map.id}",
                value=f"<b>{story_map.title}</b>",
                x=story_map.x,
                y=story_map.y,
                width=story_map.width,
                height=60,
                style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={DrawioRenderer.COLORS['map']};strokeColor=#b3b3b3;size=15;align=center;verticalAlign=middle;fontSize=16;",
                url=story_map.url,
            )

            # Draw Swimlanes
            current_swimlane_y = (
                story_map.y + 60 + 20 + 120 + 20 + 120 + 20 + 40
            )  # Based on Layout Engine (HEADER_HEIGHT + padding + goal + padding + feature + padding + SWIMLANE_MARGIN)
            # We don't have swimlane heights exactly stored, but we can draw a separator line or bounding box based on the epics in it.
            # To be accurate with heights, we'll iterate through the epics and find max Y in each swimlane.

            swimlane_bounds = {}
            for goal in story_map.goals:
                for feature in goal.features:
                    for epic in feature.epics:
                        rel = epic.release
                        if rel not in swimlane_bounds:
                            swimlane_bounds[rel] = {
                                "min_y": epic.y - 10,
                                "max_y": epic.y + epic.height + 10,
                            }
                        else:
                            swimlane_bounds[rel]["min_y"] = min(
                                swimlane_bounds[rel]["min_y"], epic.y - 10
                            )
                            swimlane_bounds[rel]["max_y"] = max(
                                swimlane_bounds[rel]["max_y"], epic.y + epic.height + 10
                            )

            for idx, release in enumerate(story_map.releases):
                if release in swimlane_bounds:
                    y = swimlane_bounds[release]["min_y"]
                    height = (
                        swimlane_bounds[release]["max_y"]
                        - swimlane_bounds[release]["min_y"]
                    )
                else:
                    # Fallback if empty swimlane
                    y = current_swimlane_y
                    height = 80

                # Draw Swimlane Line
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"swimlane_{story_map.id}_{idx}",
                    value=release,
                    x=story_map.x,
                    y=y,
                    width=story_map.width,
                    height=height,
                    style="swimlane;html=1;horizontal=0;startSize=20;fillColor=none;strokeColor=#666666;",
                )
                current_swimlane_y = y + height

            # Draw Goals
            for goal in story_map.goals:
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"goal_{goal.id}",
                    value=f"<b>[{goal.id}]</b><br/><b>{goal.title}</b>",
                    x=goal.x,
                    y=goal.y,
                    width=goal.width,
                    height=goal.height,
                    style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={DrawioRenderer.COLORS['goal']};strokeColor=#6c8ebf;size=15;",
                    url=goal.url,
                )

                # Draw Features
                for feature in goal.features:
                    DrawioRenderer._create_cell(
                        root=root,
                        id=f"feature_{feature.id}",
                        value=f"<b>[{feature.id}]</b><br/><b>{feature.title}</b>",
                        x=feature.x,
                        y=feature.y,
                        width=feature.width,
                        height=feature.height,
                        style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={DrawioRenderer.COLORS['feature']};strokeColor=#82b366;size=15;",
                        url=feature.url,
                    )

                    # Draw Epics
                    for epic in feature.epics:
                        epic_value = f"<b>[{epic.id}]</b><br/>{epic.title}"
                        if epic.status:
                            epic_value += f"<br/><i>{epic.status}</i>"

                        DrawioRenderer._create_cell(
                            root=root,
                            id=f"epic_{epic.id}",
                            value=epic_value,
                            x=epic.x,
                            y=epic.y,
                            width=epic.width,
                            height=epic.height,
                            style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={DrawioRenderer.COLORS['epic']};strokeColor=#d6b656;size=15;",
                            url=epic.url,
                        )

        tree = ET.ElementTree(mxfile)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _create_cell(
        root,
        id: str,
        value: str,
        x: int,
        y: int,
        width: int,
        height: int,
        style: str,
        url: str = None,
    ):
        if url:
            # Wrap with UserObject for clickable links
            user_obj = ET.SubElement(root, "UserObject", label=value, link=url, id=id)
            cell = ET.SubElement(
                user_obj, "mxCell", style=style, vertex="1", parent="1"
            )
        else:
            cell = ET.SubElement(
                root, "mxCell", id=id, value=value, style=style, vertex="1", parent="1"
            )

        geometry = ET.SubElement(
            cell, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height)
        )
        geometry.set("as", "geometry")
