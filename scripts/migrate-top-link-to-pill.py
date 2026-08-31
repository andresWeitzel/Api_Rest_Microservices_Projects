from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    ROOT / "README.md": {
        "anchor": "#índice-",
        "label": "Índice",
        "title": "Volver al índice",
        "asset_prefix": "./doc/assets/icons/detail-actions/",
    },
    ROOT / "translations" / "README.en.md": {
        "anchor": "#index-",
        "label": "Index",
        "title": "Back to index",
        "asset_prefix": "../doc/assets/icons/detail-actions/",
    },
}

TOP_LINK = re.compile(r"\[🔝\]\(#(?:índice|index)-\)")

TOP_BTN_STYLE = (
    "display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; "
    "border-radius: 8px; font-family: -apple-system, BlinkMacSystemFont, "
    "'Segoe UI', Helvetica, Arial, sans-serif; font-size: 11px; font-weight: 600; "
    "text-decoration: none; vertical-align: middle; margin-left: 6px; "
    "border: 1px solid rgba(148, 163, 184, 0.35); "
    "background: rgba(148, 163, 184, 0.08); color: #9aa4b2;"
)


def build_top_pill(config: dict[str, str]) -> str:
    return (
        f'<a href="{config["anchor"]}" title="{config["title"]}" '
        f'style="{TOP_BTN_STYLE}">'
        f'<img src="{config["asset_prefix"]}arrow-up.svg" width="12" height="12" alt="" '
        f'style="display: block;" /> {config["label"]}</a>'
    )


def migrate_file(path: Path, config: dict[str, str]) -> int:
    pill = build_top_pill(config)
    content = path.read_text(encoding="utf-8")
    updated, count = TOP_LINK.subn(pill, content)
    path.write_text(updated, encoding="utf-8", newline="\n")
    return count


def main() -> None:
    for path, config in FILES.items():
        count = migrate_file(path, config)
        print(f"updated {path.relative_to(ROOT)} ({count} top links)")


if __name__ == "__main__":
    main()
