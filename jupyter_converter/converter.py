#!/usr/bin/env python3
import subprocess
from pathlib import Path
import argparse

def convert_all_notebooks(input_dir, output_dir):
    input_dir  = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()

    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for nb in input_dir.rglob("*.ipynb"):
        # skip checkpoints
        if ".ipynb_checkpoints" in nb.parts:
            continue

        # preserve folder structure
        rel = nb.relative_to(input_dir).with_suffix(".html")
        target_dir = output_dir / rel.parent
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Converting: {nb} → {target_dir / rel.name}")
        try:
            subprocess.run([
                "jupyter", "nbconvert",
                "--to", "html",
                "--output-dir", str(target_dir),
                str(nb)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {nb}: {e}")

def main():
    p = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to HTML recursively."
    )
    p.add_argument("input_dir",  help="Directory to search for notebooks")
    p.add_argument("output_dir", help="Directory to write HTML files")
    args = p.parse_args()
    convert_all_notebooks(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
