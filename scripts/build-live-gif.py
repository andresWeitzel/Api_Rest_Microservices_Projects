from PIL import Image, ImageDraw, ImageFont
import math

OUT = "doc/assets/icons/social-networks/live.gif"

CANVAS_SIZE = 640
FRAMES = 20
DURATION = 85

# Red palette — live broadcast badge, strong contrast on dark README backgrounds.
RING_COLOR = (120, 18, 18, 255)
FILL_COLOR = (196, 30, 30, 255)
FILL_LIGHT = (232, 58, 58, 255)
DOT_CORE = (255, 245, 245, 255)
TEXT_COLOR = (255, 255, 255, 255)

CIRCLE_RADIUS = 248
CENTER_Y = CANVAS_SIZE // 2
TEXT_STROKE = (96, 12, 12, 255)
FONT_SIZE = 152
DOT_LAYOUT_RADIUS = 36
DOT_TEXT_GAP = 48
BADGE_MARGIN_RATIO = 0.17


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


FONT = load_font(FONT_SIZE)


def measure_live_text() -> tuple[int, int]:
    probe = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(probe)
    bbox = draw.textbbox(
        (0, 0),
        "LIVE",
        font=FONT,
        stroke_width=4,
        anchor="lt",
    )
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


TEXT_WIDTH, _TEXT_HEIGHT = measure_live_text()


def live_content_layout(center_x: int) -> tuple[int, int]:
    group_width = (DOT_LAYOUT_RADIUS * 2) + DOT_TEXT_GAP + TEXT_WIDTH
    group_left = center_x - group_width // 2
    dot_x = group_left + DOT_LAYOUT_RADIUS
    text_x = group_left + (DOT_LAYOUT_RADIUS * 2) + DOT_TEXT_GAP
    return dot_x, text_x


def add_dot_glow(
    draw: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    pulse: float,
) -> None:
    glow_r = int(24 + 12 * pulse)
    glow_layers = [
        (glow_r + 20, (72, 10, 10, 255)),
        (glow_r + 10, (120, 18, 18, 255)),
        (glow_r, (220, 48, 48, 255)),
        (int(14 + 3 * pulse), (255, 120, 120, 255)),
    ]
    for radius, color in glow_layers:
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            fill=color,
        )

    core_r = int(11 + 2 * pulse)
    draw.ellipse(
        (center_x - core_r, center_y - core_r, center_x + core_r, center_y + core_r),
        fill=DOT_CORE,
    )


def draw_live_badge(draw: ImageDraw.ImageDraw, pulse: float, ring_pulse: float) -> None:
    cx = CANVAS_SIZE // 2
    cy = CENTER_Y
    radius = CIRCLE_RADIUS

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

    dot_x, text_x = live_content_layout(cx)
    add_dot_glow(draw, dot_x, cy, pulse)
    draw.text(
        (text_x, cy),
        "LIVE",
        fill=TEXT_COLOR,
        font=FONT,
        anchor="lm",
        stroke_width=4,
        stroke_fill=TEXT_STROKE,
    )


def tighten_alpha(image: Image.Image, threshold: int = 40) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a < threshold:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (r, g, b, 255)

    return rgba


def compute_crop_box(frames: list[Image.Image], padding: int = 6) -> tuple[int, int, int, int]:
    left = top = CANVAS_SIZE
    right = bottom = 0

    for frame in frames:
        alpha = frame.getchannel("A")
        bbox = alpha.getbbox()
        if not bbox:
            continue
        left = min(left, bbox[0])
        top = min(top, bbox[1])
        right = max(right, bbox[2])
        bottom = max(bottom, bbox[3])

    if right <= left or bottom <= top:
        return (0, 0, CANVAS_SIZE, CANVAS_SIZE)

    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(CANVAS_SIZE, right + padding)
    bottom = min(CANVAS_SIZE, bottom + padding)
    return (left, top, right, bottom)


def rgba_to_palette_frame(image: Image.Image, transparent_index: int = 255) -> Image.Image:
    cleaned = tighten_alpha(image)
    alpha = cleaned.getchannel("A")
    rgb = cleaned.convert("RGB")
    palette_image = rgb.quantize(colors=254, method=Image.Quantize.MEDIANCUT)
    mask = Image.eval(alpha, lambda value: 255 if value < 128 else 0)
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


def pad_frames(frames: list[Image.Image], margin_ratio: float) -> list[Image.Image]:
    width, height = frames[0].size
    pad = int(max(width, height) * margin_ratio)
    padded_size = (width + (pad * 2), height + (pad * 2))
    padded_frames = []

    for frame in frames:
        canvas = Image.new("RGBA", padded_size, (0, 0, 0, 0))
        canvas.paste(frame, (pad, pad), frame)
        padded_frames.append(canvas)

    return padded_frames


def build_gif() -> None:
    frames = []

    for i in range(FRAMES):
        phase = 2 * math.pi * i / FRAMES
        dot_pulse = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(phase * 1.35))
        ring_pulse = math.sin(phase + math.pi / 4)

        frame = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
        draw_live_badge(ImageDraw.Draw(frame), dot_pulse, ring_pulse)
        frames.append(frame)

    crop_box = compute_crop_box(frames)
    frames = [frame.crop(crop_box) for frame in frames]
    frames = pad_frames(frames, BADGE_MARGIN_RATIO)

    save_transparent_gif(frames, OUT)
    print(
        f"saved {OUT} ({frames[0].size[0]}x{frames[0].size[1]}, "
        f"{FRAMES} frames, round LIVE badge)"
    )


if __name__ == "__main__":
    build_gif()
