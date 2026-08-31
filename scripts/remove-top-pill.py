from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOP_PILL = re.compile(
    r' ?<a href="#(?:índice|index)-" title="[^"]*" style="[^"]*">'
    r'<img src="[^"]*arrow-up\.svg" width="12" height="12" alt="" style="display: block;" /> '
    r"(?:Índice|Index)</a>"
)


def main() -> None:
    for rel in ("README.md", "translations/README.en.md"):
        path = ROOT / rel
        content = path.read_text(encoding="utf-8")
        updated, count = TOP_PILL.subn("", content)
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"removed {count} from {rel}")


if __name__ == "__main__":
    main()
