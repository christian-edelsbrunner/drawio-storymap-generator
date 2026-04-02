import yaml
from src.cli import main
import sys

# just run the cli with a sample
sys.argv = ["src/cli.py", "--input", "sample.yaml"]
try:
    main()
except Exception as e:
    print(f"Error: {e}")
