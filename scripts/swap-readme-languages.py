from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EN_SOURCE = ROOT / "README.md"
ES_SOURCE = ROOT / "translations" / "README.es.md"
EN_TARGET = ROOT / "translations" / "README.en.md"
ES_TARGET = ROOT / "README.md"

SPANISH_LANG_BLOCK = """<div align="right">
    <a href="./README.md" target="_blank">
      <img src="./doc/assets/icons/translation/arg-flag.jpg" width="65" height="40" />
    </a>
    <a href="./translations/README.en.md" target="_blank">
      <img src="./doc/assets/icons/translation/eeuu-flag.jpg" width="65" height="40" />
    </a>
</div>"""

ENGLISH_LANG_BLOCK = """<div align="right">
    <a href="../README.md" target="_blank">
      <img src="../doc/assets/icons/translation/arg-flag.jpg" width="65" height="40" />
    </a>
    <a href="./README.en.md" target="_blank">
      <img src="../doc/assets/icons/translation/eeuu-flag.jpg" width="65" height="40" />
    </a>
</div>"""


def replace_lang_block(content: str, new_block: str) -> str:
    start = content.index('<div align="right">')
    end = content.index("</div>", start) + len("</div>")
    return content[:start] + new_block + content[end:]


def main() -> None:
    english = EN_SOURCE.read_text(encoding="utf-8")
    spanish = ES_SOURCE.read_text(encoding="utf-8")

    english = english.replace("./doc/", "../doc/")
    english = replace_lang_block(english, ENGLISH_LANG_BLOCK)

    spanish = spanish.replace("../doc/", "./doc/")
    spanish = spanish.replace(
        "../doc/assets/img/arg-flag.jpg",
        "./doc/assets/icons/translation/arg-flag.jpg",
    )
    spanish = spanish.replace(
        "../doc/assets/img/eeuu-flag.jpg",
        "./doc/assets/icons/translation/eeuu-flag.jpg",
    )
    spanish = replace_lang_block(spanish, SPANISH_LANG_BLOCK)

    EN_TARGET.parent.mkdir(parents=True, exist_ok=True)
    EN_TARGET.write_text(english, encoding="utf-8", newline="\n")
    ES_TARGET.write_text(spanish, encoding="utf-8", newline="\n")
    ES_SOURCE.unlink()

    print(f"created {EN_TARGET.relative_to(ROOT)}")
    print(f"updated {ES_TARGET.relative_to(ROOT)}")
    print(f"removed {ES_SOURCE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
