from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TECH_ROW = re.compile(
    r'(<div align="(?:right|left)">)\s*((?:<img[^>]+>\s*)+)(</div>)',
    re.MULTILINE,
)

IMG_TAG = re.compile(r"<img[^>]+>")


def compact_tech_row(match: re.Match[str]) -> str:
    images = IMG_TAG.findall(match.group(2))
    compact_images: list[str] = []
    for index, tag in enumerate(images):
        if index:
            compact_images.append("<!-- -->")
        if 'border="0"' not in tag:
            tag = tag.replace("/>", ' border="0" />', 1)
        compact_images.append(tag)
    return f'{match.group(1)}{"".join(compact_images)}{match.group(3)}'


def main() -> None:
    for rel in ("README.md", "translations/README.en.md"):
        path = ROOT / rel
        content = path.read_text(encoding="utf-8")
        content = content.replace("-pill.svg", "-pill.png")
        updated, count = TECH_ROW.subn(compact_tech_row, content)
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"updated {rel}: {count} tech rows, pills -> png")


if __name__ == "__main__":
    main()
