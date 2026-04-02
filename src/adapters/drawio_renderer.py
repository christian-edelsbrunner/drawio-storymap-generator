# @ai-generated: gemini-3.1-pro
import xml.etree.ElementTree as ET
import os
from src.domain.models import Workspace


class DrawioRenderer:
    @staticmethod
    def render(workspace: Workspace, output_path: str):
        theme = workspace.theme
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
                height=theme.header_height,
                style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={theme.color_map};strokeColor=#b3b3b3;size=15;align=center;verticalAlign=middle;fontSize=16;",
                url=story_map.url,
            )

            # Draw Swimlanes
            current_swimlane_y = (
                story_map.y
                + theme.header_height
                + theme.padding_y
                + theme.card_height
                + theme.padding_y
                + theme.card_height
                + theme.padding_y
                + theme.swimlane_margin
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

                # Draw Swimlane Name
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"swimlane_label_{story_map.id}_{idx}",
                    value=f"<b>{release}</b>",
                    x=story_map.x,
                    y=y - 30,
                    width=200,
                    height=30,
                    style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=14;fontColor=#666666;",
                )

                # Draw Swimlane Line
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"swimlane_line_{story_map.id}_{idx}",
                    value="",
                    x=story_map.x,
                    y=y - 10,
                    width=story_map.width,
                    height=10,
                    style="shape=line;html=1;strokeWidth=2;strokeColor=#cccccc;dashed=1;",
                )
                current_swimlane_y = y + height

            # Draw Goals
            for goal in story_map.goals:
                goal_value = (
                    '<table style="width:100%;height:100%;" border="0" cellpadding="0" cellspacing="0">'
                    f'<tr><td align="center" valign="top" height="15"><b><font style="font-size: 16px;">[{goal.id}]</font></b></td></tr>'
                    f'<tr><td align="center" valign="middle"><b>{goal.title}</b></td></tr>'
                    "</table>"
                )
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"goal_{goal.id}",
                    value=goal_value,
                    x=goal.x,
                    y=goal.y,
                    width=goal.width,
                    height=goal.height,
                    style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={theme.color_goal};strokeColor=#6c8ebf;size=15;spacingTop=2;",
                    url=goal.url,
                )

                # Draw Features
                for feature in goal.features:
                    feature_value = (
                        '<table style="width:100%;height:100%;" border="0" cellpadding="0" cellspacing="0">'
                        f'<tr><td align="center" valign="top" height="15"><b><font style="font-size: 14px;">[{feature.id}]</font></b></td></tr>'
                        f'<tr><td align="center" valign="middle"><b>{feature.title}</b></td></tr>'
                        "</table>"
                    )
                    DrawioRenderer._create_cell(
                        root=root,
                        id=f"feature_{feature.id}",
                        value=feature_value,
                        x=feature.x,
                        y=feature.y,
                        width=feature.width,
                        height=feature.height,
                        style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={theme.color_feature};strokeColor=#82b366;size=15;spacingTop=2;",
                        url=feature.url,
                    )

                    # Draw Epics
                    for epic in feature.epics:
                        status_html = ""
                        if epic.status:
                            status_color = DrawioRenderer._get_status_color(epic.status)
                            status_html = f'<tr><td align="right" valign="bottom" height="15"><font color="{status_color}"><i>{epic.status}</i></font></td></tr>'

                        epic_value = (
                            '<table style="width:100%;height:100%;" border="0" cellpadding="0" cellspacing="0">'
                            f'<tr><td align="center" valign="top" height="15"><b><font style="font-size: 14px;">[{epic.id}]</font></b></td></tr>'
                            f'<tr><td align="center" valign="middle">{epic.title}</td></tr>'
                            f"{status_html}"
                            "</table>"
                        )

                        DrawioRenderer._create_cell(
                            root=root,
                            id=f"epic_{epic.id}",
                            value=epic_value,
                            x=epic.x,
                            y=epic.y,
                            width=epic.width,
                            height=epic.height,
                            style=f"shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor={theme.color_epic};strokeColor=#d6b656;size=15;spacingTop=2;",
                            url=epic.url,
                        )

        tree = ET.ElementTree(mxfile)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _get_status_color(status: str) -> str:
        s = status.lower()
        if "done" in s or "closed" in s or "resolved" in s:
            return "#008000"  # Green
        elif "progress" in s or "doing" in s or "active" in s:
            return "#0000FF"  # Blue
        elif "to do" in s or "open" in s or "todo" in s or "new" in s:
            return "#666666"  # Gray
        elif "blocked" in s or "impediment" in s:
            return "#FF0000"  # Red
        return "#333333"

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
