from PIL import Image, ImageDraw, ImageFont
import math

OUT = "doc/assets/icons/social-networks/live.gif"

CANVAS_SIZE = 640
FRAMES = 20
DURATION = 85

RING_COLOR = (24, 96, 48, 255)
FILL_COLOR = (34, 128, 58, 255)
FILL_LIGHT = (48, 156, 72, 255)
DOT_CORE = (235, 255, 235, 255)
TEXT_COLOR = (255, 255, 255, 255)

CIRCLE_RADIUS = 248
DOT_CENTER_X = 220
TEXT_CENTER_X = 362
CENTER_Y = CANVAS_SIZE // 2


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = load_font(116)


def add_dot_glow(
    draw: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    pulse: float,
) -> None:
    glow_r = int(30 + 16 * pulse)
    glow_layers = [
        (glow_r + 26, (18, 72, 30, 255)),
        (glow_r + 14, (30, 110, 42, 255)),
        (glow_r, (58, 188, 72, 255)),
        (int(18 + 4 * pulse), (120, 255, 96, 255)),
    ]
    for radius, color in glow_layers:
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            fill=color,
        )

    core_r = int(14 + 3 * pulse)
    draw.ellipse(
        (center_x - core_r, center_y - core_r, center_x + core_r, center_y + core_r),
        fill=DOT_CORE,
    )


def draw_live_badge(draw: ImageDraw.ImageDraw, pulse: float, ring_pulse: float) -> None:
    cx = CANVAS_SIZE // 2
    cy = CENTER_Y
    radius = int(CIRCLE_RADIUS * (1 + 0.015 * ring_pulse))

    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill=RING_COLOR,
    )

    inner_radius = radius - 18
    draw.ellipse(
        (cx - inner_radius, cy - inner_radius, cx + inner_radius, cy + inner_radius),
        fill=FILL_COLOR,
    )

    highlight_radius = inner_radius - 24
    draw.ellipse(
        (
            cx - highlight_radius,
            cy - highlight_radius - 16,
            cx + highlight_radius,
            cy + highlight_radius - 48,
        ),
        fill=FILL_LIGHT,
    )

    add_dot_glow(draw, DOT_CENTER_X, cy, pulse)
    draw.text((TEXT_CENTER_X, cy), "LIVE", fill=TEXT_COLOR, font=FONT, anchor="mm")


def rgba_to_palette_frame(image: Image.Image, transparent_index: int = 255) -> Image.Image:
    alpha = image.getchannel("A")
    rgb = image.convert("RGB")
    palette_image = rgb.quantize(colors=254, method=Image.Quantize.MEDIANCUT)
    mask = Image.eval(alpha, lambda value: 255 if value < 16 else 0)
    palette_image.paste(transparent_index, mask)
    return palette_image


def save_transparent_gif(frames: list[Image.Image], path: str) -> None:
    transparent_index = 255
    palette_frames = [rgba_to_palette_frame(frame, transparent_index) for frame in frames]

    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=DURATION,
        loop=0,
        disposal=2,
        transparency=transparent_index,
        optimize=False,
    )


def build_gif() -> None:
    frames = []

    for i in range(FRAMES):
        phase = 2 * math.pi * i / FRAMES
        dot_pulse = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(phase * 1.35))
        ring_pulse = math.sin(phase + math.pi / 4)

        frame = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
        draw_live_badge(ImageDraw.Draw(frame), dot_pulse, ring_pulse)
        frames.append(frame)

    save_transparent_gif(frames, OUT)
    print(f"saved {OUT} ({CANVAS_SIZE}x{CANVAS_SIZE}, {FRAMES} frames, round LIVE badge)")


if __name__ == "__main__":
    build_gif()
