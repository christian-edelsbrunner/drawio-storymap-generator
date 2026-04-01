import argparse
import sys
import os

# Add project root to python path if run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.adapters.yaml_parser import YamlParser, StoryMapParseError
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
        "--output",
        "-o",
        required=False,
        help="Path to the output .drawio file (defaults to input filename with .drawio extension).",
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if not output_path:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{base_name}.drawio"

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Parsing YAML file: {input_path}")
        workspace = YamlParser.parse(input_path)

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
