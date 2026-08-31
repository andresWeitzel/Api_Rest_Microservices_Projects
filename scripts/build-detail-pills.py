from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("doc/assets/icons/detail-actions")

FONT_CANDIDATES = (
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
)

HEIGHT = 30
PADDING_X = 12
ICON_BOX = 14
ICON_GAP = 6
RADIUS = 8
FONT_SIZE = 12
SIDE_GAP = 6

ICONS = {
    "live": (
        '<path d="M11 3h6v6"/>'
        '<path d="M6 14 17 3"/>'
        '<path d="M14 13v6a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
    ),
    "code": (
        '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.55-5.36-.55-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65S8.5 17.5 9 18v4"/>'
        '<path d="M9 18c-4.51 2-5-2-7-2"/>'
    ),
    "video": (
        '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/>'
        '<path d="m10 15 5-3-5-3z"/>'
    ),
}

# Approximate Segoe UI semibold widths at 12px (fallback).
CHAR_WIDTH = 6.55


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = load_font(FONT_SIZE)


def text_width(label: str) -> int:
    probe = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(probe)
    bbox = draw.textbbox((0, 0), label, font=FONT, anchor="lt")
    return bbox[2] - bbox[0]


def pill_width_for(label: str) -> int:
    return PADDING_X * 2 + ICON_BOX + ICON_GAP + text_width(label) + 2


def build_svg(label: str, variant: str, filename: str, *, accent: bool) -> None:
    pill_width = pill_width_for(label)
    canvas_width = pill_width + (SIDE_GAP * 2)
    text_x = SIDE_GAP + PADDING_X + ICON_BOX + ICON_GAP
    text_y = HEIGHT / 2 + 4.5
    icon_x = SIDE_GAP + PADDING_X
    icon_y = (HEIGHT - ICON_BOX) / 2
    scale = ICON_BOX / 24

    if accent:
        fill = "#122820"
        stroke = "#2A8F6A"
        foreground = "#2EE9A8"
    else:
        fill = "#1C2128"
        stroke = "#3D4450"
        foreground = "#9AA4B2"

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{HEIGHT}" '
        f'viewBox="0 0 {canvas_width} {HEIGHT}" fill="none" role="img" '
        f'aria-label="{label}">\n'
        f'  <g transform="translate({SIDE_GAP} 0)">\n'
        f'    <rect x="0.5" y="0.5" width="{pill_width - 1}" height="{HEIGHT - 1}" rx="{RADIUS}" '
        f'fill="{fill}" stroke="{stroke}"/>\n'
        f'    <g transform="translate({icon_x - SIDE_GAP:.2f} {icon_y:.2f}) scale({scale:.4f})" '
        f'fill="none" stroke="{foreground}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{ICONS[variant]}</g>\n'
        f'    <text x="{text_x - SIDE_GAP}" y="{text_y}" fill="{foreground}" '
        f'font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" '
        f'font-size="{FONT_SIZE}" font-weight="600">{label}</text>\n'
        f"  </g>\n"
        f"</svg>\n"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / filename
    path.write_text(svg, encoding="utf-8", newline="\n")
    print(f"saved {path} ({canvas_width}x{HEIGHT})")


def main() -> None:
    build_svg("Live", "live", "live-pill.svg", accent=True)
    build_svg("Código", "code", "codigo-pill.svg", accent=False)
    build_svg("Code", "code", "code-pill.svg", accent=False)
    build_svg("Video", "video", "video-pill.svg", accent=False)


if __name__ == "__main__":
    main()
