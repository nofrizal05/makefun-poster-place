#!/usr/bin/env python3
"""Write the Aurelia travel poster to the make.fun output directory.

Stdlib only: the shipped entry.png is copied verbatim to
$MAKEFUN_OUTPUT_DIR/entry.png (defaults to ./output when the variable
is unset, so `python3 main.py` works locally too).
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
