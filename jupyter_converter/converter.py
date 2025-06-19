import subprocess
from pathlib import Path
import argparse

def convert_all_notebooks(input_dir, output_dir):
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for notebook_path in input_dir.rglob("*.ipynb"):
        relative_path = notebook_path.relative_to(input_dir).with_suffix(".html")
        output_path = output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Converting: {notebook_path} → {output_path}")
        try:
            subprocess.run([
                "jupyter", "nbconvert",
                "--to", "html",
                "--output", output_path.name,
                str(notebook_path)
            ], check=True, cwd=str(output_path.parent))
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {notebook_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to HTML."
    )
    parser.add_argument("input_dir",  help="Directory to search for notebooks")
    parser.add_argument("output_dir", help="Directory to write HTML files")
    args = parser.parse_args()
    convert_all_notebooks(args.input_dir, args.output_dir)
