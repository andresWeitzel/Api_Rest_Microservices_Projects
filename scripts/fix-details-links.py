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
    r'<img src="[^"]+" alt="[^"]*" height="30"(?: style="[^"]*")? />\s*</a>'
    r'(?:\s*</td>)?'
    r')+)'
    r'(?:\s*</tr>\s*</table>)?'
    r"\s*</div>",
    re.MULTILINE,
)

LINK_RE = re.compile(
    r'(?:<td>\s*)?'
    r'<a href="([^"]*)" target="_blank"(?: rel="[^"]*")? title="([^"]*)">'
    r'<img src="([^"]+)" alt="([^"]*)" height="30"(?: style="[^"]*")? />\s*</a>'
    r'(?:\s*</td>)?',
    re.MULTILINE,
)


def table_cell(href: str, title: str, src: str, alt: str) -> str:
    return (
        f'<td><a href="{href}" target="_blank" rel="noopener noreferrer" title="{title}">'
        f'<img src="{src}" alt="{alt}" height="30" /></a></td>'
    )


def rebuild_block(match: re.Match[str]) -> str:
    links = LINK_RE.findall(match.group(1))
    cells = "".join(table_cell(href, title, src, alt) for href, title, src, alt in links)
    return (
        '<div align="center">\n'
        '<table cellpadding="0" cellspacing="8" border="0">\n'
        f"<tr>{cells}</tr>\n"
        "</table>\n"
        "</div>"
    )


def main() -> None:
    for rel in ("README.md", "translations/README.en.md"):
        path = ROOT / rel
        content = path.read_text(encoding="utf-8")
        updated, count = DETAILS_BLOCK.subn(rebuild_block, content)
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"fixed {count} blocks in {rel}")


if __name__ == "__main__":
    main()
