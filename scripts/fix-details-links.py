from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DETAILS_BLOCK = re.compile(
    r'<div align="center">\s*'
    r'(?:<table[^>]*>\s*<tr>\s*)?'
    r'((?:'
    r'(?:<td>\s*)?'
    r'<a href="[^"]*" target="_blank"(?: rel="[^"]*")? title="[^"]*">'
    r'<img src="[^"]+" alt="[^"]*" height="30"(?: border="0")?(?: style="[^"]*")? />\s*</a>'
    r'(?:\s*</td>)?(?:<!-- -->)?'
    r')+)'
    r'(?:\s*</tr>\s*</table>)?'
    r"\s*</div>",
    re.MULTILINE,
)

LINK_RE = re.compile(
    r'(?:<td>\s*)?'
    r'<a href="([^"]*)" target="_blank"(?: rel="[^"]*")? title="([^"]*)">'
    r'<img src="([^"]+)" alt="([^"]*)" height="30"(?: border="0")?(?: style="[^"]*")? />\s*</a>'
    r'(?:\s*</td>)?',
    re.MULTILINE,
)


def compact_link(href: str, title: str, src: str, alt: str) -> str:
    return (
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" title="{title}">'
        f'<img src="{src}" alt="{alt}" height="30" border="0" /></a>'
    )


def rebuild_block(match: re.Match[str]) -> str:
    links = LINK_RE.findall(match.group(1))
    parts: list[str] = []
    for index, link in enumerate(links):
        if index:
            parts.append("<!-- -->")
        parts.append(compact_link(*link))
    body = "".join(parts)
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
