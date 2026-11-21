#!/usr/bin/env python3
"""Draw 'AURELIA — The Floating Isles', a vintage travel poster (1024x1024).

Invented place: Aurelia, a chain of floating islands adrift above a
bioluminescent sea, under an aurora sky. Drawn entirely with Pillow.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = "entry.png"

random.seed(20261121)


def font(name, size):
    import glob, os
    cands = glob.glob(f"/usr/share/fonts/truetype/**/{name}", recursive=True)
    if not cands:
        raise SystemExit(f"font not found: {name}")
    return ImageFont.truetype(cands[0], size)


F_TITLE = font("NotoSerifDisplay-Black.ttf", 168)
F_SUB = font("NotoSans-Bold.ttf", 44)
F_TAG = font("NotoSerifDisplay-Italic.ttf", 40)
F_SMALL = font("NotoSans-Bold.ttf", 26)
F_TINY = font("NotoSans-Regular.ttf", 22)

CREAM = (244, 230, 196)
GOLD = (212, 175, 105)
GOLD_DIM = (176, 138, 74)
INK = (24, 18, 48)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(base, stops):
    """stops: list of (y_fraction, rgb). Returns RGB image."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        f = y / (H - 1)
        for i in range(len(stops) - 1):
            y0, c0 = stops[i]
            y1, c1 = stops[i + 1]
            if y0 <= f <= y1:
                t = 0 if y1 == y0 else (f - y0) / (y1 - y0)
                col = lerp(c0, c1, t)
                break
        else:
            col = stops[-1][1]
        for x in range(W):
            px[x, y] = col
    return img


def tracked(draw, cx, y, text, fnt, fill, tracking=0, stroke_w=0, stroke_fill=None):
    """Draw text centered at cx with letter tracking."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill,
                  stroke_width=stroke_w, stroke_fill=stroke_fill)
        x += w + tracking
    return total


# ---------------------------------------------------------------- sky
sky = vgrad(None, [
    (0.00, (16, 12, 46)),
    (0.35, (46, 28, 84)),
    (0.55, (74, 44, 110)),
    (0.68, (22, 84, 96)),
    (1.00, (8, 44, 62)),
])
img = sky.convert("RGBA")
d = ImageDraw.Draw(img)

# stars
for _ in range(260):
    x = random.uniform(0, W)
    y = random.uniform(0, 620)
    r = random.choice([1, 1, 1, 2, 2, 3])
    a = random.randint(90, 235)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 230, a))
for _ in range(14):  # a few bright stars with cross sparkle
    x = random.uniform(40, W - 40)
    y = random.uniform(30, 300)
    s = random.randint(5, 9)
    d.line([x - s, y, x + s, y], fill=(255, 250, 230, 200), width=1)
    d.line([x, y - s, x, y + s], fill=(255, 250, 230, 200), width=1)

# moon with glow (upper right)
mx, my, mr = 800, 170, 74
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, a in [(190, 18), (150, 28), (115, 45)]:
    gd.ellipse([mx - r, my - r, mx + r, my + r], fill=(250, 240, 200, a))
glow = glow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, glow)
d = ImageDraw.Draw(img)
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(250, 238, 205, 255))
d.ellipse([mx - mr + 18, my - mr + 12, mx - mr + 42, my - mr + 36],
          fill=(232, 216, 178, 255))
d.ellipse([mx - mr + 46, my - mr + 52, mx - mr + 66, my - mr + 72],
          fill=(232, 216, 178, 255))
d.ellipse([mx - mr + 8, my - mr + 58, mx - mr + 22, my - mr + 72],
          fill=(238, 224, 186, 255))

# aurora ribbons
aur = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(aur)
for base_y, amp, col, alpha in [
        (150, 46, (64, 224, 180), 46),
        (210, 60, (120, 200, 255), 34),
        (270, 40, (170, 130, 255), 30)]:
    pts_top, pts_bot = [], []
    for x in range(0, W + 20, 20):
        y = base_y + amp * math.sin(x / 190.0 + base_y) + 18 * math.sin(x / 67.0)
        pts_top.append((x, y))
        pts_bot.append((x, y + 90))
    ad.polygon(pts_top + pts_bot[::-1], fill=col + (alpha,))
aur = aur.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, aur)
d = ImageDraw.Draw(img)

# distant clouds (soft, low)
cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cl)
for cx, cy, s in [(180, 560, 90), (300, 580, 120), (760, 600, 110),
                  (880, 560, 80), (60, 620, 70)]:
    for ox, oy, r in [(0, 0, s), (-s * 0.7, 8, s * 0.65),
                      (s * 0.7, 10, s * 0.6), (0, -14, s * 0.55)]:
        cd.ellipse([cx + ox - r, cy + oy - r * 0.45, cx + ox + r,
                    cy + oy + r * 0.45], fill=(190, 170, 220, 26))
cl = cl.filter(ImageFilter.GaussianBlur(10))
img = Image.alpha_composite(img, cl)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- sea
sea = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sea)
for y in range(700, H):
    t = (y - 700) / (H - 700)
    col = lerp((16, 96, 104), (4, 26, 44), t)
    sd.line([(0, y), (W, y)], fill=col + (255,))
# horizon glow
for i, a in enumerate(range(90, 0, -6)):
    sd.line([(0, 700 + i), (W, 700 + i)], fill=(120, 220, 200, a))
# moon reflection streak
for i in range(90):
    x = mx + random.uniform(-30, 30)
    y = 712 + i * 3.0
    ln = random.uniform(10, 40)
    sd.line([(x - ln / 2, y), (x + ln / 2, y)],
            fill=(250, 238, 200, random.randint(30, 90)), width=1)
# bioluminescent sparkles
for _ in range(320):
    x = random.uniform(0, W)
    y = random.uniform(716, H - 30)
    r = random.choice([1, 1, 2, 2, 3])
    col = random.choice([(90, 240, 210), (60, 200, 255), (150, 255, 220)])
    sd.ellipse([x - r, y - r, x + r, y + r],
               fill=col + (random.randint(90, 220),))
# gentle wave lines
for y in range(730, H, 34):
    for _ in range(6):
        x = random.uniform(0, W - 120)
        ln = random.uniform(40, 120)
        sd.line([(x, y), (x + ln, y)], fill=(140, 230, 215, 46), width=2)
img = Image.alpha_composite(img, sea)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- islands
def island(cx, top_y, w, h, hue_dark, hue_top, trees=True, falls=True):
    """Floating island: grassy top, rocky tapering underside, waterfalls."""
    pts = []
    n = 26
    # top edge (slightly domed)
    for i in range(n + 1):
        x = cx - w / 2 + w * i / n
        y = top_y + 10 * math.sin(math.pi * i / n) * -0.4 + random.uniform(-2, 2)
        pts.append((x, y))
    # underside: jagged taper to a point
    tip = (cx + random.uniform(-14, 14), top_y + h)
    under = []
    steps = 14
    for i in range(steps + 1):
        t = i / steps
        # from right top corner to tip
        x = cx + w / 2 - (w / 2 - (tip[0] - cx)) * t + random.uniform(-7, 7) * (1 - t)
        y = top_y + 14 + (tip[1] - top_y - 14) * t
        under.append((x, y))
    for i in range(steps, -1, -1):
        t = i / steps
        x = cx - w / 2 + (w / 2 + (tip[0] - cx)) * t + random.uniform(-7, 7) * (1 - t)
        y = top_y + 14 + (tip[1] - top_y - 14) * t
        under.append((x, y))
    body = pts + under
    d.polygon(body, fill=hue_dark)
    # grassy top band
    top_band = [(cx - w / 2, top_y + 4), (cx + w / 2, top_y + 4),
                (cx + w / 2 - 8, top_y + 26), (cx - w / 2 + 8, top_y + 26)]
    d.polygon(top_band, fill=hue_top)
    # rock shading: a few darker facets
    for _ in range(6):
        x0 = cx + random.uniform(-w / 2 + 20, w / 2 - 60)
        y0 = top_y + random.uniform(30, h * 0.55)
        d.polygon([(x0, y0), (x0 + 46, y0 + 10), (x0 + 18, y0 + 44)],
                  fill=(hue_dark[0] - 12, hue_dark[1] - 10, hue_dark[2] - 2))
    # trees
    if trees:
        for _ in range(int(w / 46)):
            tx = cx + random.uniform(-w / 2 + 24, w / 2 - 24)
            th = random.uniform(26, 46)
            ty = top_y - 4
            d.polygon([(tx, ty - th), (tx - th * 0.32, ty),
                       (tx + th * 0.32, ty)], fill=(16, 60, 44))
            d.rectangle([tx - 2, ty - 2, tx + 2, ty + 4], fill=(40, 28, 20))
    # waterfalls from the rim
    if falls:
        for fx in (cx - w * 0.30, cx + w * 0.22):
            wl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            wd = ImageDraw.Draw(wl)
            wd.line([(fx, top_y + 20), (fx + 6, top_y + 150)],
                    fill=(180, 235, 245, 190), width=7)
            wd.line([(fx + 8, top_y + 20), (fx + 12, top_y + 120)],
                    fill=(220, 250, 255, 150), width=3)
            wl = wl.filter(ImageFilter.GaussianBlur(2))
            img.paste(Image.alpha_composite(img, wl), (0, 0))
    return top_y


# back island (left, small)
island(210, 470, 300, 150, (38, 30, 66), (30, 84, 62), trees=True, falls=False)
# back island (right, small)
island(850, 500, 260, 130, (34, 28, 62), (28, 78, 58), trees=True, falls=False)
# main island (centre)
main_top = island(512, 560, 560, 260, (30, 24, 56), (26, 92, 66),
                  trees=True, falls=True)

# lighthouse on the main island
lx = 640
d.rectangle([lx - 14, main_top - 96, lx + 14, main_top + 2], fill=(244, 230, 196))
d.rectangle([lx - 14, main_top - 96, lx + 14, main_top - 78], fill=(196, 52, 52))
d.rectangle([lx - 14, main_top - 58, lx + 14, main_top - 40], fill=(196, 52, 52))
d.rectangle([lx - 18, main_top - 112, lx + 18, main_top - 96], fill=(40, 34, 60))
d.ellipse([lx - 12, main_top - 126, lx + 12, main_top - 102],
          fill=(250, 238, 200))
# light beams
beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(lx, main_top - 112), (lx + 250, main_top - 190),
            (lx + 250, main_top - 130)], fill=(250, 240, 190, 70))
bd.polygon([(lx, main_top - 112), (lx - 250, main_top - 175),
            (lx - 250, main_top - 125)], fill=(250, 240, 190, 55))
beam = beam.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img, beam)
d = ImageDraw.Draw(img)

# small domed pavilion on main island (left side)
px = 400
d.rectangle([px - 34, main_top - 44, px + 34, main_top + 2], fill=(232, 214, 170))
d.pieslice([px - 36, main_top - 84, px + 36, main_top - 20],
           180, 360, fill=(176, 138, 74))
d.rectangle([px - 4, main_top - 28, px + 4, main_top + 2], fill=(40, 34, 60))

# tiny sailboat on the sea for scale
bx, by = 250, 872
d.polygon([(bx, by), (bx - 34, by + 16), (bx + 34, by + 16)], fill=(30, 20, 46))
d.line([(bx, by), (bx, by - 52)], fill=(30, 20, 46), width=3)
d.polygon([(bx + 3, by - 50), (bx + 3, by - 4), (bx + 40, by - 4)],
          fill=(244, 230, 196))
d.polygon([(bx - 3, by - 44), (bx - 3, by - 4), (bx - 30, by - 4)],
          fill=(220, 205, 170))

# birds
for bx2, by2, s in [(330, 330, 9), (370, 300, 7), (690, 260, 8), (730, 300, 6)]:
    d.arc([bx2 - s, by2 - s, bx2, by2 + s], 200, 340, fill=(20, 14, 40), width=2)
    d.arc([bx2, by2 - s, bx2 + s, by2 + s], 200, 340, fill=(20, 14, 40), width=2)

# ---------------------------------------------------------------- text
# soft shadow + title
ty = 78
tracked(d, 512, ty + 6, "AURELIA", F_TITLE, (10, 8, 30), tracking=26)
tracked(d, 512, ty, "AURELIA", F_TITLE, CREAM, tracking=26)
# gold rule under title
d.rectangle([512 - 150, 268, 512 + 150, 272], fill=GOLD)
d.polygon([(512, 262), (522, 270), (512, 278), (502, 270)], fill=GOLD)
# subtitle
tracked(d, 512, 292, "T H E   F L O A T I N G   I S L E S", F_SUB, GOLD,
        tracking=0)
# tagline at bottom over the sea (auto-fit inside the border)
tag = "Where the islands drift and the sea glows beneath the stars."
tag_size = 40
while True:
    f_tag = font("NotoSerifDisplay-Italic.ttf", tag_size)
    tw = d.textlength(tag, font=f_tag)
    if tw <= 860 or tag_size <= 24:
        break
    tag_size -= 2
d.rectangle([512 - tw / 2 - 18, 906, 512 + tw / 2 + 18, 952],
            fill=(6, 20, 34, 170))
d.text((512 - tw / 2, 914), tag, font=f_tag, fill=CREAM)
# bottom line
tracked(d, 512, 964, "—  T R A V E L   B E Y O N D   T H E   M A P  —",
        F_TINY, (200, 190, 160), tracking=0)

# ---------------------------------------------------------------- border
d.rectangle([18, 18, W - 19, H - 19], outline=CREAM, width=5)
d.rectangle([34, 34, W - 35, H - 35], outline=GOLD, width=2)
# corner diamonds
for cx, cy in [(18, 18), (W - 19, 18), (18, H - 19), (W - 19, H - 19)]:
    d.polygon([(cx, cy - 12), (cx + 12, cy), (cx, cy + 12), (cx - 12, cy)],
              fill=GOLD)

img.convert("RGB").save(OUT, optimize=True)
print("saved", OUT)
