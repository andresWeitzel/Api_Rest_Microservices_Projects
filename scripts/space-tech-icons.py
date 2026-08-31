from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TECH_ROW = re.compile(
    r'(<div align="(?:right|left)">)\s*((?:(?:<!-- -->)?<img[^>]+>)+)(</div>)',
    re.MULTILINE,
)

IMG_TAG = re.compile(r"<img[^>]+>")
IMG_STYLE = 'style="vertical-align: middle;"'


def normalize_img_tag(tag: str) -> str:
    tag = re.sub(r'\s+border="0"', "", tag)
    tag = re.sub(r'\s+style="[^"]*"', "", tag)
    tag = tag.replace("/>", f' {IMG_STYLE} border="0" />', 1)
    return tag


def space_tech_row(match: re.Match[str]) -> str:
    images = [normalize_img_tag(tag) for tag in IMG_TAG.findall(match.group(2))]
    return f'{match.group(1)}{" ".join(images)}{match.group(3)}'


def main() -> None:
    for rel in ("README.md", "translations/README.en.md"):
        path = ROOT / rel
        content = path.read_text(encoding="utf-8")
        updated, count = TECH_ROW.subn(space_tech_row, content)
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"spaced {count} tech rows in {rel}")


if __name__ == "__main__":
    main()
