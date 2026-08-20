# @ai-generated: gemini-3.1-pro
import html
import xml.etree.ElementTree as ET
from typing import Optional

from src.domain.models import Workspace


# Atlassian native "lozenge" palette used for Jira status pills.
# Keys are lowercase substrings matched against the status text.
_STATUS_PALETTE = {
    "done":       {"bg": "#E3FCEF", "fg": "#006644"},
    "closed":     {"bg": "#E3FCEF", "fg": "#006644"},
    "resolved":   {"bg": "#E3FCEF", "fg": "#006644"},
    "progress":   {"bg": "#DEEBFF", "fg": "#0747A6"},
    "doing":      {"bg": "#DEEBFF", "fg": "#0747A6"},
    "active":     {"bg": "#DEEBFF", "fg": "#0747A6"},
    "implementation": {"bg": "#DEEBFF", "fg": "#0747A6"},
    "development": {"bg": "#DEEBFF", "fg": "#0747A6"},
    "review":     {"bg": "#EAE6FF", "fg": "#403294"},
    "testing":    {"bg": "#EAE6FF", "fg": "#403294"},
    "blocked":    {"bg": "#FFEBE6", "fg": "#BF2600"},
    "impediment": {"bg": "#FFEBE6", "fg": "#BF2600"},
    "to do":      {"bg": "#DFE1E6", "fg": "#42526E"},
    "todo":       {"bg": "#DFE1E6", "fg": "#42526E"},
    "open":       {"bg": "#DFE1E6", "fg": "#42526E"},
    "new":        {"bg": "#DFE1E6", "fg": "#42526E"},
    "backlog":    {"bg": "#DFE1E6", "fg": "#42526E"},
}
# Fallback pill used when the status text matches nothing above.
_STATUS_FALLBACK = {"bg": "#EAE6FF", "fg": "#403294"}

# ID pill uses Atlassian "link" blue so it visually hints clickability
# even though the Draw.io HTML label subset does not support inline <a>
# hyperlinks - the whole card is still wrapped in a clickable UserObject.
_ID_PILL = {"bg": "#DEEBFF", "fg": "#0747A6"}


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
            # Map header - Jira-card style, wider layout since it spans the map
            DrawioRenderer._create_cell(
                root=root,
                id=f"map_{story_map.id}",
                value=DrawioRenderer._jira_card_label(
                    node_id=story_map.id,
                    title=story_map.title,
                    status=None,           # Maps have no status
                    title_font_size=13,
                    title_bold=True,
                ),
                x=story_map.x,
                y=story_map.y,
                width=story_map.width,
                height=theme.header_height,
                style=DrawioRenderer._card_style(fill=theme.color_map),
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
            )

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
                    y = current_swimlane_y
                    height = 80

                # Swimlane label
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"swimlane_label_{story_map.id}_{idx}",
                    value=f"<b>{html.escape(release)}</b>",
                    x=story_map.x,
                    y=y - 30,
                    width=200,
                    height=30,
                    style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=12;fontColor=#42526E;",
                )

                # Swimlane separator line
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"swimlane_line_{story_map.id}_{idx}",
                    value="",
                    x=story_map.x,
                    y=y - 10,
                    width=story_map.width,
                    height=10,
                    style="shape=line;html=1;strokeWidth=1;strokeColor=#DFE1E6;dashed=1;",
                )
                current_swimlane_y = y + height

            # Draw Goals
            for goal in story_map.goals:
                DrawioRenderer._create_cell(
                    root=root,
                    id=f"goal_{goal.id}",
                    value=DrawioRenderer._jira_card_label(
                        node_id=goal.id,
                        title=goal.title,
                        status=goal.status,
                    ),
                    x=goal.x,
                    y=goal.y,
                    width=goal.width,
                    height=goal.height,
                    style=DrawioRenderer._card_style(fill=theme.color_goal),
                    url=goal.url,
                )

                # Draw Features
                for feature in goal.features:
                    DrawioRenderer._create_cell(
                        root=root,
                        id=f"feature_{feature.id}",
                        value=DrawioRenderer._jira_card_label(
                            node_id=feature.id,
                            title=feature.title,
                            status=feature.status,
                        ),
                        x=feature.x,
                        y=feature.y,
                        width=feature.width,
                        height=feature.height,
                        style=DrawioRenderer._card_style(fill=theme.color_feature),
                        url=feature.url,
                    )

                    # Draw Epics
                    for epic in feature.epics:
                        DrawioRenderer._create_cell(
                            root=root,
                            id=f"epic_{epic.id}",
                            value=DrawioRenderer._jira_card_label(
                                node_id=epic.id,
                                title=epic.title,
                                status=epic.status,
                            ),
                            x=epic.x,
                            y=epic.y,
                            width=epic.width,
                            height=epic.height,
                            style=DrawioRenderer._card_style(fill=theme.color_epic),
                            url=epic.url,
                        )

        tree = ET.ElementTree(mxfile)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    # ------------------------------------------------------------------
    # Label / style helpers (Jira-card look)
    # ------------------------------------------------------------------
    @staticmethod
    def _jira_card_label(
        node_id: str,
        title: str,
        status: Optional[str] = None,
        title_font_size: int = 10,
        title_bold: bool = True,
    ) -> str:
        """Render a Jira/Miro-style card label as a Draw.io HTML fragment.

        Structure (all inside a <table> because Draw.io's label HTML subset
        does not honour block-level layout otherwise):

          - Row 1: card title, left-aligned, dark text.
          - Row 2: status pill (if present).
          - Row 3: Jira-ID pill (if present).

        Draw.io labels only support ONE URL per node (the enclosing
        UserObject), so the ID pill is a visual affordance - the entire
        card is what actually navigates on click.
        """
        safe_title = html.escape(title or "")
        safe_id = html.escape(node_id or "")

        title_style = (
            f"font-size:{title_font_size}px;"
            f"color:#172B4D;"
            f"line-height:1.25;"
            + ("font-weight:600;" if title_bold else "")
        )
        title_html = f'<div style="{title_style}">{safe_title}</div>'

        # Each pill lives on its own line. We use separate divs (not a
        # flexbox / not comma-separated) because Draw.io's label HTML subset
        # honours block-level <div> line breaks reliably.
        rows_html = [title_html]
        if status:
            rows_html.append(
                '<div style="margin-top:4px;line-height:1.4;">'
                + DrawioRenderer._pill_html(status, _status_pill(status))
                + "</div>"
            )
        if safe_id:
            rows_html.append(
                '<div style="margin-top:2px;line-height:1.4;">'
                + DrawioRenderer._pill_html(f"[{safe_id}]", _ID_PILL)
                + "</div>"
            )

        # Table wrapper keeps vertical spacing predictable across Draw.io
        # versions (some ignore margins on top-level divs inside a label).
        return (
            '<table style="width:100%;height:100%;" border="0" cellpadding="2" cellspacing="0">'
            f'<tr><td align="left" valign="top">{"".join(rows_html)}</td></tr>'
            "</table>"
        )

    @staticmethod
    def _pill_html(text: str, palette: dict) -> str:
        return (
            f'<span style="'
            f'background:{palette["bg"]};'
            f'color:{palette["fg"]};'
            f'padding:1px 6px;'
            f'border-radius:3px;'
            f'font-size:9px;'
            f'font-weight:600;'
            f'letter-spacing:0.3px;'
            f'text-transform:uppercase;'
            f'">'
            f"{html.escape(text)}</span>"
        )

    @staticmethod
    def _card_style(fill: str) -> str:
        """Common Jira-card mxCell style: white-ish fill, subtle border, rounded."""
        return (
            "rounded=1;"
            "whiteSpace=wrap;"
            "html=1;"
            f"fillColor={fill};"
            "strokeColor=#DFE1E6;"
            "strokeWidth=1;"
            "shadow=0;"
            "align=left;"
            "verticalAlign=top;"
            "spacing=4;"
            "arcSize=8;"
        )

    # ------------------------------------------------------------------
    # Legacy helper kept for backwards compatibility (was public-ish).
    # ------------------------------------------------------------------
    @staticmethod
    def _get_status_color(status: str) -> str:
        palette = _status_pill(status)
        return palette["fg"]

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
        url: Optional[str] = None,
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


def _status_pill(status: str) -> dict:
    if not status:
        return _STATUS_FALLBACK
    s = status.lower()
    for keyword, palette in _STATUS_PALETTE.items():
        if keyword in s:
            return palette
    return _STATUS_FALLBACK
