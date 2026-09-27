"""Export a deterministic wireframe-style PNG and register it in a small manifest.

This is a technical pipeline fixture only; it is never product approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(output: Path, manifest: Path):
    if output.parent.resolve() != manifest.parent.resolve():
        raise ValueError("Keep fixture image and manifest in the same versioned directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (960, 540), "#f4f6f8")
    draw = ImageDraw.Draw(image)
    ink, line, panel = "#17212b", "#81909d", "#ffffff"
    draw.rectangle((0, 0, 959, 72), fill=ink)
    draw.text((32, 24), "FOUNDATION / WIREFRAME FIXTURE", fill="white")
    draw.rectangle((32, 104, 280, 488), outline=line, width=2, fill=panel)
    draw.rectangle((312, 104, 928, 184), outline=line, width=2, fill=panel)
    draw.rectangle((312, 208, 928, 488), outline=line, width=2, fill=panel)
    draw.rectangle((56, 136, 256, 160), fill="#dbe2e8")
    for y in (196, 244, 292, 340, 388):
        draw.rectangle((56, y, 256, y + 18), fill="#dbe2e8")
    draw.rectangle((344, 132, 620, 156), fill="#b9c5cf")
    draw.rectangle((344, 232, 896, 256), fill="#b9c5cf")
    for y in (286, 334, 382, 430):
        draw.rectangle((344, y, 840, y + 16), fill="#dbe2e8")
    draw.rectangle((760, 128, 896, 164), outline="#476b86", width=2)
    draw.text((790, 139), "ACTION", fill="#476b86")
    image.save(output, "PNG", optimize=False)
    record = {
        "format": "1.0", "role": "technical-wireframe-pipeline-fixture",
        "approved": False, "screen": "synthetic-foundation-dashboard", "states": ["ready"],
        "renderer": "Pillow", "source": "tools/render_fixture.py", "source_sha256": sha256(Path(__file__)),
        "path_base": "manifest directory", "dimensions": [960, 540],
        "files": {output.name: {"path": output.name, "sha256": sha256(output), "kind": "image"}},
        "review": "Technical export/display smoke test only; no product or user design approval."
    }
    manifest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.output, args.manifest), indent=2))
