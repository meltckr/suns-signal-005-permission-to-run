from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
HERO_OUT = ASSETS / "permission-to-run-cover.png"
OG_OUT = ASSETS / "og-suns-signal-004-permission-to-run.png"

FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(path, size):
    return ImageFont.truetype(str(path), size)


def gradient(size, top, bottom):
    width, height = size
    image = Image.new("RGB", size)
    pixels = image.load()
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(width):
            pixels[x, y] = color
    return image


def add_court_system(image):
    width, height = image.size
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Court geometry on the right half.
    court_left = int(width * 0.48)
    line = (255, 255, 255, 48)
    draw.rectangle((court_left, int(height * 0.12), width + 4, int(height * 0.9)), outline=line, width=3)
    draw.line((court_left, int(height * 0.51), width, int(height * 0.51)), fill=line, width=3)
    center = (int(width * 0.75), int(height * 0.51))
    radius = int(height * 0.105)
    draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=line, width=3)
    draw.arc((int(width * 0.65), int(height * 0.2), int(width * 1.03), int(height * 0.82)), 105, 255, fill=(241, 152, 67, 95), width=5)

    # Five nodes connect into one bright identity line.
    nodes = [
        (0.56, 0.28, "IDEA"),
        (0.70, 0.39, "DECISIONS"),
        (0.84, 0.25, "FORCE"),
        (0.79, 0.68, "VERSATILITY"),
        (0.61, 0.72, "SHOOTING"),
    ]
    node_font = font(FONT_BOLD, max(16, int(width * 0.013)))
    hub = (int(width * 0.75), int(height * 0.52))
    for nx, ny, label in nodes:
        point = (int(width * nx), int(height * ny))
        draw.line((point[0], point[1], hub[0], hub[1]), fill=(241, 152, 67, 105), width=3)
        draw.ellipse((point[0] - 10, point[1] - 10, point[0] + 10, point[1] + 10), fill=(39, 200, 194, 235))
        text_box = draw.textbbox((0, 0), label, font=node_font)
        text_w = text_box[2] - text_box[0]
        draw.text((point[0] - text_w // 2, point[1] + 17), label, font=node_font, fill=(255, 255, 255, 185))
    draw.ellipse((hub[0] - 18, hub[1] - 18, hub[0] + 18, hub[1] + 18), fill=(241, 152, 67, 255))
    draw.ellipse((hub[0] - 37, hub[1] - 37, hub[0] + 37, hub[1] + 37), outline=(241, 152, 67, 105), width=4)

    # Win line in the background.
    path = []
    for step in range(34):
        x = int(width * (0.49 + step * 0.0135))
        y = int(height * (0.83 - (step / 33) * 0.22))
        path.append((x, y))
    draw.line(path, fill=(39, 200, 194, 125), width=5)
    for point in path[::5]:
        draw.ellipse((point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4), fill=(39, 200, 194, 200))

    layer = layer.filter(ImageFilter.GaussianBlur(0.2))
    return Image.alpha_composite(image.convert("RGBA"), layer)


def build_hero():
    width, height = 1600, 900
    image = gradient((width, height), (36, 24, 54), (10, 14, 21)).convert("RGBA")
    image = add_court_system(image)
    draw = ImageDraw.Draw(image)

    # Texture and timeline, kept clear of the HTML headline area.
    for x in range(0, width, 34):
        draw.line((x, 0, x - 280, height), fill=(255, 255, 255, 8), width=1)
    label = font(FONT_BOLD, 24)
    big = font(FONT_BOLD, 105)
    small = font(FONT_REG, 28)
    draw.text((930, 680), "29–53", font=big, fill=(255, 255, 255, 110))
    draw.text((1270, 680), "62–20", font=big, fill=(241, 152, 67, 210))
    draw.text((936, 800), "ONE IDEA  •  ONE IDENTITY  •  +33 WINS", font=label, fill=(255, 255, 255, 160))
    draw.text((935, 838), "PHOENIX  |  2004–05", font=small, fill=(39, 200, 194, 180))
    image.convert("RGB").save(HERO_OUT, quality=95)


def build_og():
    width, height = 1200, 630
    image = gradient((width, height), (34, 24, 51), (10, 14, 21)).convert("RGBA")
    image = add_court_system(image)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 735, height), fill=(10, 13, 18, 178))
    od.line((70, 512, 1130, 512), fill=(241, 152, 67, 195), width=3)
    image = Image.alpha_composite(image, overlay)
    draw = ImageDraw.Draw(image)

    label = font(FONT_BOLD, 25)
    tiny = font(FONT_BOLD, 18)
    display = font(FONT_BOLD, 72)
    regular = font(FONT_REG, 27)
    stat = font(FONT_BOLD, 42)

    draw.text((68, 46), "SUNS SIGNAL WEEKLY 004", font=label, fill=(255, 255, 255, 248))
    draw.text((70, 84), "SUNDAY EDITION  |  AUGUST 9, 2026", font=tiny, fill=(241, 152, 67, 245))
    draw.text((68, 148), "Permission", font=display, fill=(255, 255, 255, 255))
    draw.text((68, 226), "to Run", font=display, fill=(255, 255, 255, 255))
    draw.text((72, 334), "The 33-win jump—and the organization", font=regular, fill=(230, 234, 239, 238))
    draw.text((72, 372), "that turned an idea into an identity.", font=regular, fill=(230, 234, 239, 238))
    draw.text((72, 444), "29–53", font=stat, fill=(255, 255, 255, 205))
    draw.text((225, 444), "→", font=stat, fill=(39, 200, 194, 235))
    draw.text((294, 444), "62–20", font=stat, fill=(241, 152, 67, 255))

    team_logo = Image.open(ASSETS / "teams" / "suns" / "phoenix-suns-logo.png").convert("RGBA")
    team_logo.thumbnail((108, 108), Image.Resampling.LANCZOS)
    image.alpha_composite(team_logo, (1030, 44))
    draw = ImageDraw.Draw(image)
    draw.text((72, 548), "CURATED FOR MAT ISHBIA", font=tiny, fill=(241, 152, 67, 250))
    draw.text((72, 580), "Prepared by Accelerated Velocity Consulting", font=tiny, fill=(215, 222, 232, 180))
    image.convert("RGB").save(OG_OUT, quality=95)


if __name__ == "__main__":
    build_hero()
    build_og()
    print(HERO_OUT)
    print(OG_OUT)
