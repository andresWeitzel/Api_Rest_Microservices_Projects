from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DETAILS_BLOCK = re.compile(
    r'<div align="center">\s*'
    r'((?:<a href="[^"]*" target="_blank"(?: rel="[^"]*")? title="[^"]*">\s*'
    r'<img src="[^"]+" alt="[^"]*" height="30" />\s*</a>\s*)+)'
    r"</div>",
    re.MULTILINE,
)

LINK_RE = re.compile(
    r'<a href="([^"]*)" target="_blank"(?: rel="[^"]*")? title="([^"]*)">\s*'
    r'<img src="([^"]+)" alt="([^"]*)" height="30" />\s*</a>',
    re.MULTILINE,
)


def compact_link(href: str, title: str, src: str, alt: str) -> str:
    return (
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" title="{title}">'
        f'<img src="{src}" alt="{alt}" height="30" /></a>'
    )


def rebuild_block(match: re.Match[str]) -> str:
    links = LINK_RE.findall(match.group(1))
    body = "".join(compact_link(href, title, src, alt) for href, title, src, alt in links)
    return f'<div align="center">\n{body}\n</div>'


def main() -> None:
    for rel in ("README.md", "translations/README.en.md"):
        path = ROOT / rel
        content = path.read_text(encoding="utf-8")
        updated, count = DETAILS_BLOCK.subn(rebuild_block, content)
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"fixed {count} blocks in {rel}")


if __name__ == "__main__":
    main()
