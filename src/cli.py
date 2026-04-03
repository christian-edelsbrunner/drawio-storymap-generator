# @ai-generated: gemini-3.1-pro
import argparse
import sys
import os
import yaml

# Add project root to python path if run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.adapters.yaml_parser import YamlParser, StoryMapParseError
from src.adapters.jira_csv_parser import JiraCsvParser
from src.layout.engine import LayoutEngine
from src.adapters.drawio_renderer import DrawioRenderer


def main():
    parser = argparse.ArgumentParser(
        description="Generate a draw.io Story Map from a YAML file."
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Path to the input YAML file."
    )
    parser.add_argument(
        "--input-format",
        required=False,
        choices=["yaml", "jira-csv"],
        default="yaml",
        help="Input format: 'yaml' (default) or 'jira-csv'.",
    )
    parser.add_argument(
        "--hierarchy-issue-types",
        required=False,
        default="Initiative,Epic,Story,Task",
        help="Comma-separated hierarchy levels; use '/' for multiple issue types per level.",
    )
    parser.add_argument(
        "--hierarchy-config",
        required=False,
        help="Path to YAML hierarchy config with 'hierarchy_issue_types'.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=False,
        help="Path to the output .drawio file (defaults to input filename with .drawio extension).",
    )
    parser.add_argument(
        "--theme",
        "-t",
        required=False,
        help="Path to an optional theme YAML file.",
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    theme_path = args.theme
    input_format = args.input_format

    if not output_path:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{base_name}.drawio"

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if theme_path and not os.path.exists(theme_path):
        print(f"Error: Theme file '{theme_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if args.hierarchy_config and not os.path.exists(args.hierarchy_config):
        print(
            f"Error: Hierarchy config file '{args.hierarchy_config}' does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        if input_format == "jira-csv":
            print(f"Parsing Jira CSV file: {input_path}")
            if args.hierarchy_config:
                hierarchy_issue_types = (
                    JiraCsvParser.load_hierarchy_issue_types_from_config(
                        args.hierarchy_config
                    )
                )
            else:
                hierarchy_issue_types = JiraCsvParser.normalize_hierarchy_issue_types(
                    args.hierarchy_issue_types
                )
            workspace = JiraCsvParser.parse(input_path, hierarchy_issue_types)
        else:
            print(f"Parsing YAML file: {input_path}")
            workspace = YamlParser.parse(input_path)

        if theme_path:
            print(f"Loading theme from: {theme_path}")
            with open(theme_path, "r") as tf:
                theme_data = yaml.safe_load(tf)
                if theme_data and isinstance(theme_data, dict):
                    # Override the theme loaded from the main YAML
                    for key, value in theme_data.items():
                        if hasattr(workspace.theme, key):
                            setattr(workspace.theme, key, value)

        print("Calculating spatial layout...")
        LayoutEngine.calculate(workspace)

        print(f"Rendering to Draw.io file: {output_path}")
        DrawioRenderer.render(workspace, output_path)

        print(f"Success! Diagram saved to {output_path}")

    except StoryMapParseError as e:
        print(f"Parse Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
