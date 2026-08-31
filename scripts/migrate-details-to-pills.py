from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    ROOT / "README.md": {
        "asset_prefix": "./doc/assets/icons/detail-actions/",
        "code_label": "Código",
        "code_title": "Código",
        "live_label": "Live",
        "live_title": "Ver en vivo",
        "video_label": "Video",
        "video_title": "Video en YouTube",
    },
    ROOT / "translations" / "README.en.md": {
        "asset_prefix": "../doc/assets/icons/detail-actions/",
        "code_label": "Code",
        "code_title": "Code",
        "live_label": "Live",
        "live_title": "Watch live",
        "video_label": "Video",
        "video_title": "YouTube video",
    },
}

DETAILS_BLOCK = re.compile(
    r'<div style="display: inline-block; vertical-align: middle; text-align: center;">\s*'
    r'((?:<a href="[^"]*" target="_blank"(?: title="[^"]*")?>\s*'
    r'<img width="60" height="60" alt="[^"]*" src="[^"]+/(?:github|live|youtubeLogo)\.gif" '
    r'style="[^"]*" />\s*</a>\s*)+)'
    r'</div>',
    re.MULTILINE,
)

LINK_RE = re.compile(
    r'<a href="([^"]*)" target="_blank"(?: title="([^"]*)")?>\s*'
    r'<img[^>]+src="[^"]+/(github|live|youtubeLogo)\.gif"',
    re.MULTILINE,
)

BTN_BASE = (
    "display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; "
    "border-radius: 8px; font-family: -apple-system, BlinkMacSystemFont, "
    "'Segoe UI', Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 600; "
    "text-decoration: none; vertical-align: middle; margin: 0 4px;"
)
LIVE_STYLE = (
    f"{BTN_BASE} border: 1px solid rgba(46, 233, 168, 0.35); "
    "background: rgba(46, 233, 168, 0.12); color: #2ee9a8;"
)
SECONDARY_STYLE = (
    f"{BTN_BASE} border: 1px solid rgba(148, 163, 184, 0.35); "
    "background: rgba(148, 163, 184, 0.08); color: #9aa4b2;"
)


def render_button(
    href: str,
    title: str,
    label: str,
    icon: str,
    style: str,
    asset_prefix: str,
) -> str:
    return (
        f'  <a href="{href}" target="_blank" rel="noopener noreferrer" title="{title}" '
        f'style="{style}">\n'
        f'    <img src="{asset_prefix}{icon}" width="14" height="14" alt="" '
        f'style="display: block;" />\n'
        f"    {label}\n"
        f"  </a>"
    )


def build_block(links: dict[str, str], config: dict[str, str]) -> str:
    asset_prefix = config["asset_prefix"]
    buttons: list[str] = []

    live_url = links.get("live", "").strip()
    if live_url:
        buttons.append(
            render_button(
                live_url,
                config["live_title"],
                config["live_label"],
                "external-link.svg",
                LIVE_STYLE,
                asset_prefix,
            )
        )

    code_url = links.get("github", "").strip()
    if code_url:
        buttons.append(
            render_button(
                code_url,
                config["code_title"],
                config["code_label"],
                "github.svg",
                SECONDARY_STYLE,
                asset_prefix,
            )
        )

    video_url = links.get("youtubeLogo", "").strip()
    if video_url:
        buttons.append(
            render_button(
                video_url,
                config["video_title"],
                config["video_label"],
                "youtube.svg",
                SECONDARY_STYLE,
                asset_prefix,
            )
        )

    return '<div align="center" style="margin-top: 4px;">\n' + "\n".join(buttons) + "\n</div>"


def replace_block(match: re.Match[str], config: dict[str, str]) -> str:
    links: dict[str, str] = {}
    for href, _title, icon_name in LINK_RE.findall(match.group(1)):
        links[icon_name] = href
    return build_block(links, config)


def migrate_file(path: Path, config: dict[str, str]) -> int:
    content = path.read_text(encoding="utf-8")
    updated, count = DETAILS_BLOCK.subn(lambda match: replace_block(match, config), content)
    path.write_text(updated, encoding="utf-8", newline="\n")
    return count


def main() -> None:
    for path, config in FILES.items():
        count = migrate_file(path, config)
        print(f"updated {path.relative_to(ROOT)} ({count} detail blocks)")


if __name__ == "__main__":
    main()
