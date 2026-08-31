from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICON_STYLE = 'style="display: inline-block; vertical-align: middle;"'

FILES = {
    ROOT / "translations" / "README.en.md": {
        "github": ("Code", "Code"),
        "live": ("Watch live", "Watch live"),
        "youtube": ("YouTube", "YouTube"),
    },
    ROOT / "README.md": {
        "github": ("Código", "Código"),
        "live": ("Ver en vivo", "Ver en vivo"),
        "youtube": ("YouTube", "YouTube"),
    },
}

ICON_FILES = {
    "github": "github.gif",
    "live": "live.gif",
    "youtube": "youtubeLogo.gif",
}


def upsert_title(anchor_tag: str, title: str) -> str:
    if re.search(r'\btitle="[^"]*"', anchor_tag):
        return re.sub(r'\btitle="[^"]*"', f'title="{title}"', anchor_tag)
    return anchor_tag.replace('target="_blank"', f'target="_blank" title="{title}"', 1)


def update_icon_block(
    content: str,
    icon_key: str,
    title: str,
    alt: str,
) -> str:
    icon_name = ICON_FILES[icon_key]
    pattern = re.compile(
        rf'(<a href="[^"]*" target="_blank"(?: title="[^"]*")?>)\s*'
        rf'(<img width="60" height="60" alt="[^"]*" src="[^"]+/{re.escape(icon_name)}" '
        rf'style="[^"]*" />)',
        re.MULTILINE,
    )

    def replacer(match: re.Match[str]) -> str:
        anchor = upsert_title(match.group(1), title)
        src_match = re.search(r'src="([^"]+)"', match.group(2))
        src = src_match.group(1) if src_match else ""
        img = f'<img width="60" height="60" alt="{alt}" src="{src}" {ICON_STYLE} />'
        return f"{anchor}\n    {img}"

    return pattern.sub(replacer, content)


def main() -> None:
    for path, labels in FILES.items():
        content = path.read_text(encoding="utf-8")
        for icon_key, (title, alt) in labels.items():
            content = update_icon_block(content, icon_key, title, alt)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
