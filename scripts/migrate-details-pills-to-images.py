from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    ROOT / "README.md": {
        "asset_prefix": "./doc/assets/icons/detail-actions/",
        "live_img": "live-pill.svg",
        "code_img": "codigo-pill.svg",
        "live_title": "Ver en vivo",
        "code_title": "Código",
        "video_title": "Video en YouTube",
        "live_alt": "Live",
        "code_alt": "Código",
        "video_alt": "Video",
    },
    ROOT / "translations" / "README.en.md": {
        "asset_prefix": "../doc/assets/icons/detail-actions/",
        "live_img": "live-pill.svg",
        "code_img": "code-pill.svg",
        "live_title": "Watch live",
        "code_title": "Code",
        "video_title": "YouTube video",
        "live_alt": "Live",
        "code_alt": "Code",
        "video_alt": "Video",
    },
}

DETAILS_BLOCK = re.compile(
    r'<div align="center" style="margin-top: 4px;">\s*'
    r'((?:<a href="[^"]*" target="_blank" rel="noopener noreferrer" title="[^"]*" style="[^"]*">\s*'
    r'<img src="[^"]+" width="14" height="14" alt="" style="display: block;" />\s*'
    r"(?:Live|Código|Code|Video)\s*"
    r"</a>\s*)+)"
    r"</div>",
    re.MULTILINE,
)

ANCHOR_RE = re.compile(
    r'<a href="([^"]*)" target="_blank" rel="noopener noreferrer" title="([^"]*)"[^>]*>\s*'
    r'<img src="[^"]+" width="14" height="14" alt="" style="display: block;" />\s*'
    r"(Live|Código|Code|Video)\s*</a>",
    re.MULTILINE,
)

PILL_HEIGHT = 28


def render_img_link(href: str, title: str, alt: str, image: str, asset_prefix: str) -> str:
    return (
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" title="{title}">'
        f'<img src="{asset_prefix}{image}" alt="{alt}" height="{PILL_HEIGHT}" /></a>'
    )


def classify(label: str) -> str:
    if label == "Live":
        return "live"
    if label in {"Código", "Code"}:
        return "code"
    return "video"


def build_block(anchors: list[tuple[str, str, str]], config: dict[str, str]) -> str:
    asset_prefix = config["asset_prefix"]
    buttons: list[str] = []

    for href, _title, label in anchors:
        kind = classify(label)
        if kind == "live":
            buttons.append(
                render_img_link(
                    href,
                    config["live_title"],
                    config["live_alt"],
                    config["live_img"],
                    asset_prefix,
                )
            )
        elif kind == "code":
            buttons.append(
                render_img_link(
                    href,
                    config["code_title"],
                    config["code_alt"],
                    config["code_img"],
                    asset_prefix,
                )
            )
        else:
            buttons.append(
                render_img_link(
                    href,
                    config["video_title"],
                    config["video_alt"],
                    "video-pill.svg",
                    asset_prefix,
                )
            )

    return '<div align="center">\n' + "".join(buttons) + "\n</div>"


def replace_block(match: re.Match[str], config: dict[str, str]) -> str:
    anchors = ANCHOR_RE.findall(match.group(1))
    return build_block(anchors, config)


def migrate_file(path: Path, config: dict[str, str]) -> int:
    content = path.read_text(encoding="utf-8")
    updated, count = DETAILS_BLOCK.subn(lambda match: replace_block(match, config), content)
    path.write_text(updated, encoding="utf-8", newline="\n")
    return count


def main() -> None:
    for path, config in FILES.items():
        count = migrate_file(path, config)
        print(f"updated {path.relative_to(ROOT)} ({count} blocks)")


if __name__ == "__main__":
    main()
