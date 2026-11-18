#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page entirely in code.

Vector-style newspaper front page, 1024x1024, drawn with Pillow shapes
and DejaVu fonts. No photos, no copied artwork: every line and icon is
drawn here from primitives.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 32, 46)
RED = (178, 34, 34)
NAVY = (26, 42, 74)
GOLD = (198, 142, 30)
TEAL = (18, 110, 110)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- outer frame ----
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=4)
d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

# ---- masthead ----
d.text((48, 38), "THE WORLD", font=font(SERIF_B, 74), fill=NAVY)
d.text((48, 118), "IN ONE DAY", font=font(SERIF_B, 44), fill=INK)

# globe motif, top right
cx, cy, r = 880, 110, 78
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(173, 216, 230),
          outline=NAVY, width=4)
# meridians / parallels
for k in (-40, 0, 40):
    d.ellipse([cx - r + 34 + k, cy - r, cx + r - 34 - k, cy + r],
              outline=(90, 140, 170), width=2)
for k in (-38, 0, 38):
    d.line([cx - r + 12, cy + k, cx + r - 12, cy + k],
           fill=(90, 140, 170), width=2)
# simplified land blobs on the globe
d.ellipse([cx - 52, cy - 48, cx - 6, cy - 2], fill=(96, 160, 90))
d.ellipse([cx - 8, cy - 18, cx + 44, cy + 26], fill=(96, 160, 90))
d.ellipse([cx - 30, cy + 30, cx + 18, cy + 58], fill=(120, 175, 95))
# red dots marking the day's hot spots
for (dx, dy) in [(-30, -28), (22, -8), (38, 18), (-8, 34)]:
    d.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6],
              fill=RED, outline=WHITE, width=2)

# ---- date banner ----
d.rectangle([30, 196, W - 30, 252], fill=RED)
d.text((512, 200), "TUESDAY  •  17 NOVEMBER 2026",
       font=font(SANS_B, 40), fill=WHITE, anchor="ma")


def wrap(text, width):
    return textwrap.wrap(text, width=width)


def headline(draw, x, y, text, size=34, fill=INK, width=30):
    f = font(SANS_B, size)
    for i, line in enumerate(wrap(text, width)):
        draw.text((x, y + i * (size + 6)), line, font=f, fill=fill)
    return y + len(wrap(text, width)) * (size + 6)


def body(draw, x, y, text, size=23, fill=(60, 60, 60), width=44):
    f = font(SANS, size)
    for i, line in enumerate(wrap(text, width)):
        draw.text((x, y + i * (size + 7)), line, font=f, fill=fill)
    return y + len(wrap(text, width)) * (size + 7)


def kicker(draw, x, y, text, color):
    draw.text((x, y), text, font=font(SANS_B, 24), fill=color)
    return y + 34


def panel(x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 10], fill=accent)


# ================= LEAD STORY: UKRAINE =================
panel(30, 268, 964, 218, RED)
# bridge icon: deck, pillars, arch, explosion burst
bx, by = 58, 330
d.line([bx, by + 62, bx + 190, by + 62], fill=NAVY, width=8)
for px in (bx + 20, bx + 85, bx + 150):
    d.line([px, by + 62, px, by + 108], fill=NAVY, width=8)
d.arc([bx + 10, by - 6, bx + 180, by + 70], start=180, end=360,
      fill=NAVY, width=6)
# explosion burst above the bridge
ex, ey = bx + 118, by - 6
for ang in range(0, 360, 30):
    import math
    a = math.radians(ang)
    d.line([ex, ey, ex + 30 * math.cos(a), ey + 30 * math.sin(a)],
           fill=(230, 120, 20), width=5)
d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=(255, 200, 40),
          outline=(230, 120, 20), width=3)
y = kicker(d, 278, 286, "UKRAINE  —  LEAD STORY", RED)
y = headline(d, 278, y, "Kerch Bridge hit again", size=36, width=26)
body(d, 278, y + 4,
     "Ukraine strikes the Crimean bridge a second day running; Russia hits Kyiv's river bridges.",
     size=23, width=46)

# ================= GRID: 4 STORIES =================
# Layout per panel: small icon top-left, kicker to its right,
# headline full-width below, body at the bottom.
gx, gy, gw, gh, gap = 30, 502, 472, 236, 16
KX = 160           # kicker x-offset inside a grid panel
HY = 100           # headline y-offset inside a grid panel
BY = 178           # body y-offset inside a grid panel

# --- 2. GULF ---
panel(gx, gy, gw, gh, TEAL)
# radar + drone icon (64px)
rx, ry = gx + 22, gy + 26
d.ellipse([rx, ry, rx + 64, ry + 64], outline=TEAL, width=4)
d.ellipse([rx + 26, ry + 26, rx + 38, ry + 38], fill=TEAL)
d.line([rx + 32, ry + 32, rx + 58, ry + 8], fill=TEAL, width=4)
d.polygon([(rx + 74, ry + 4), (rx + 90, ry + 14), (rx + 74, ry + 24),
           (rx + 64, ry + 14)], fill=INK)
y = kicker(d, gx + KX, gy + 26, "THE GULF", TEAL)
y = headline(d, gx + 22, gy + HY, "Iran drones target US base in Bahrain", size=30, width=24)
body(d, gx + 22, gy + BY,
     "Intercepted, no casualties. Tankers hit mines near Hormuz.",
     size=19, width=44)

# --- 3. SHENZHEN SUMMIT ---
panel(gx + gw + gap, gy, gw, gh, GOLD)
# three flags on poles (64px tall)
fx, fy = gx + gw + gap + 22, gy + 26
for i, col in enumerate([(178, 34, 34), (26, 42, 74), (200, 200, 200)]):
    px = fx + i * 46
    d.line([px, fy, px, fy + 64], fill=INK, width=4)
    d.rectangle([px, fy, px + 40, fy + 22], fill=col, outline=INK, width=2)
y = kicker(d, gx + gw + gap + KX, gy + 26, "CHINA", GOLD)
y = headline(d, gx + gw + gap + 22, gy + HY, "Xi, Trump, Putin to meet in Shenzhen", size=30, width=24)
body(d, gx + gw + gap + 22, gy + BY,
     "First three-way talks, Thursday 19 Nov, on APEC sidelines.",
     size=19, width=44)

# --- 4. ESTONIA ---
panel(gx, gy + gh + gap, gw, gh, NAVY)
# border barrier icon (64px tall)
exx, eyy = gx + 22, gy + gh + gap + 26
d.rectangle([exx, eyy + 16, exx + 100, eyy + 30], fill=WHITE,
            outline=NAVY, width=3)
for i in range(5):
    x0 = exx + 6 + i * 20
    d.polygon([(x0, eyy + 30), (x0 + 10, eyy + 16), (x0 + 20, eyy + 16),
               (x0 + 10, eyy + 30)], fill=RED)
d.line([exx + 6, eyy + 30, exx + 6, eyy + 64], fill=NAVY, width=6)
d.line([exx + 94, eyy + 30, exx + 94, eyy + 64], fill=NAVY, width=6)
y = kicker(d, gx + KX, gy + gh + gap + 26, "ESTONIA", NAVY)
y = headline(d, gx + 22, gy + gh + gap + HY, "Estonia shuts Russia border", size=30, width=24)
body(d, gx + 22, gy + gh + gap + BY,
     "All crossings close from 1 Dec, after a foiled Russian arson and sabotage plot.",
     size=19, width=44)

# --- 5. JAPAN ---
panel(gx + gw + gap, gy + gh + gap, gw, gh, (120, 60, 140))
# fighter jet icon (64px tall)
jx, jy = gx + gw + gap + 22, gy + gh + gap + 26
d.polygon([(jx + 8, jy + 30), (jx + 92, jy + 30), (jx + 104, jy + 36),
           (jx + 92, jy + 42), (jx + 8, jy + 42)], fill=INK)
d.polygon([(jx + 36, jy + 30), (jx + 58, jy + 10), (jx + 68, jy + 30)],
          fill=INK)
d.polygon([(jx + 36, jy + 42), (jx + 58, jy + 62), (jx + 68, jy + 42)],
          fill=INK)
d.polygon([(jx + 74, jy + 28), (jx + 90, jy + 16), (jx + 94, jy + 30)],
          fill=INK)
d.polygon([(jx + 74, jy + 44), (jx + 90, jy + 56), (jx + 94, jy + 42)],
          fill=INK)
for i in range(2):
    d.line([jx - 2 - i * 12, jy + 36, jx + 8 - i * 12, jy + 36],
           fill=GREY, width=3)
y = kicker(d, gx + gw + gap + KX, gy + gh + gap + 26, "JAPAN", (120, 60, 140))
y = headline(d, gx + gw + gap + 22, gy + gh + gap + HY, "Jets scrambled as Russian planes intrude", size=30, width=24)
body(d, gx + gw + gap + 22, gy + gh + gap + BY,
     "Suspected Russian aircraft violate Japanese airspace.",
     size=19, width=44)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
