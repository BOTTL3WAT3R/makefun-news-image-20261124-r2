#!/usr/bin/env python3
"""Render poster.png: 24 November 2026 world news in one 1024x1024 image.

Six verified stories, one drawn panel each, newspaper style.
Deterministic: fixed seed, no network, no clock.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FD}/DejaVuSerif-Bold.ttf"
SANS_B = f"{FD}/DejaVuSans-Bold.ttf"
SANS = f"{FD}/DejaVuSans.ttf"

PAPER = (243, 238, 226)
INK = (24, 26, 32)
NAVY = (16, 34, 64)
RED = (168, 32, 40)
GREY = (96, 96, 96)

STORIES = [
    {
        "cat": "MARKETS",
        "color": (20, 110, 60),
        "head": "Nvidia Brings Back Jensen Huang as CEO",
        "body": "Eleven days after resigning amid scandal, Huang returns "
                "as Nvidia CEO after Trump intervened. Stock +31%; "
                "Nasdaq +6%, S&P 500 +5%.",
        "src": "Reuters / BBC / CNN",
        "motif": "chart",
    },
    {
        "cat": "WAR AT SEA",
        "color": (28, 74, 138),
        "head": "Ukrainian Drones Sink Russian Corvette in Libya",
        "body": "Seven Ukrainian naval drones sank the Russian corvette "
                "Merkury and hit cargo ship MV Angara in Benghazi port, "
                "2,400 km from the front line.",
        "src": "AP / WSJ / BBC",
        "motif": "ship",
    },
    {
        "cat": "CLIMATE",
        "color": (176, 108, 20),
        "head": "COP31 Talks in Antalya Collapse, No Deal",
        "body": "The longest-ever UN climate summit ended in division in "
                "Antalya, Turkey, as the EU and others rejected the draft "
                "pact. No deal.",
        "src": "Reuters / BBC / Le Monde",
        "motif": "globe",
    },
    {
        "cat": "INDONESIA",
        "color": (168, 32, 40),
        "head": "Candy Factory Fire in Cikande Kills 24",
        "body": "A Saturday-night blaze at a candy factory in Cikande, "
                "Banten left 24 confirmed dead and about 30 missing.",
        "src": "Reuters / AP",
        "motif": "flame",
    },
    {
        "cat": "MEXICO",
        "color": (110, 60, 140),
        "head": "Elite Soldiers Capture 'Chapo Isidro'",
        "body": "Mexican elite soldiers captured Beltran Leyva leader "
                "Fausto Isidro Meza Flores, 'Chapo Isidro', with US "
                "intelligence help.",
        "src": "Reuters / BBC",
        "motif": "badge",
    },
    {
        "cat": "US POLITICS",
        "color": (30, 90, 120),
        "head": "Democrats Win Biggest House Majority Since 1992",
        "body": "Democrats won their largest US House majority since "
                "1992 after flipping a North Carolina seat.",
        "src": "Reuters / BBC",
        "motif": "ballot",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def grain(img, seed=20261124, amp=4):
    rnd = random.Random(seed)
    px = img.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            d = rnd.randint(-amp, amp)
            r, g, b = px[x, y]
            v = (max(0, min(255, r + d)), max(0, min(255, g + d)),
                 max(0, min(255, b + d)))
            px[x, y] = v
            if x + 1 < W:
                px[x + 1, y] = v
            if y + 1 < H:
                px[x, y + 1] = v
            if x + 1 < W and y + 1 < H:
                px[x + 1, y + 1] = v
    return img


def motif(draw, kind, cx, cy, s, color):
    """Small line motif drawn in a box centred at (cx, cy), size s."""
    x0, y0, x1, y1 = cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2
    if kind == "chart":
        pts = [(x0, y1 - 6), (x0 + s // 3, y1 - s // 3),
               (x0 + s // 2, y1 - s // 4), (x1 - 8, y0 + 8)]
        draw.line(pts, fill=color, width=5, joint="curve")
        draw.polygon([(x1 - 8, y0 + 8), (x1 - 26, y0 + 10),
                      (x1 - 10, y0 + 26)], fill=color)
        draw.line([(x0, y1), (x1, y1)], fill=color, width=3)
    elif kind == "ship":
        draw.polygon([(x0 + 4, cy + 2), (x1 - 4, cy + 2),
                      (x1 - 16, cy + 14), (x0 + 16, cy + 14)], fill=color)
        draw.rectangle([cx - 15, cy - 12, cx + 12, cy + 2], fill=color)
        draw.line([(cx - 2, cy - 12), (cx - 2, cy - 24)], fill=color,
                  width=4)
        for i in range(3):
            wx = x0 + 4 + i * (s // 3)
            draw.arc([wx, y1 - 12, wx + s // 3, y1 + 6], 0, 180,
                     fill=color, width=3)
    elif kind == "globe":
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=color, width=4)
        draw.line([(cx, y0 + 4), (cx, y1 - 4)], fill=color, width=3)
        draw.arc([x0 + 14, y0 + 4, cx + 6, y1 - 4], 90, 270,
                 fill=color, width=3)
        draw.arc([cx - 6, y0 + 4, x1 - 14, y1 - 4], 270, 90,
                 fill=color, width=3)
        draw.line([(x0 + 4, cy), (x1 - 4, cy)], fill=color, width=3)
    elif kind == "flame":
        draw.polygon([(cx, y0 + 2), (x1 - 12, cy + 8), (cx + 8, y1 - 4),
                      (cx - 8, y1 - 4), (x0 + 12, cy + 8)], fill=color)
        draw.polygon([(cx, cy - 2), (cx + 9, cy + 14), (cx, y1 - 6),
                      (cx - 9, cy + 14)], fill=(240, 170, 40))
    elif kind == "badge":
        import math
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = s // 2 - 2 if i % 2 == 0 else s // 4
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(250, 246, 235))
    elif kind == "ballot":
        draw.rectangle([x0 + 6, cy - 4, x1 - 6, y1 - 4], outline=color,
                       width=4)
        draw.rectangle([x0 + 18, y0 + 2, x1 - 18, cy + 8], fill=color)
        draw.line([(x0 + 26, cy + 12), (cx - 2, y1 - 14)], fill=color,
                  width=5)
        draw.line([(cx - 2, y1 - 14), (x1 - 24, cy + 10)], fill=color,
                  width=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 134], fill=RED)
    f_title = font(SERIF_B, 56)
    title = "THE DAILY SIGNAL"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 14), title, font=f_title, fill=(250, 246, 235))
    f_date = font(SANS_B, 25)
    date_line = "TUESDAY  24  NOVEMBER  2026"
    dw = d.textlength(date_line, font=f_date)
    d.text(((W - dw) / 2, 84), date_line, font=f_date, fill=(255, 196, 66))
    f_tag = font(SANS, 19)
    tag = "The day's world news, in one image"
    gw = d.textlength(tag, font=f_tag)
    d.text((W - gw - 18, 141), tag, font=f_tag, fill=GREY)

    # Panels: 2 columns x 3 rows
    mx, gap = 26, 14
    top, bottom = 172, 962
    pw = (W - 2 * mx - gap) // 2
    ph = (bottom - top - 2 * gap) // 3
    f_cat = font(SANS_B, 17)
    f_head = font(SANS_B, 24)
    f_body = font(SANS, 19)
    f_src = font(SANS, 15)

    for i, st in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = mx + col * (pw + gap)
        y = top + row * (ph + gap)
        # panel frame + header bar
        d.rectangle([x, y, x + pw, y + ph], fill=(250, 246, 235),
                    outline=INK, width=2)
        d.rectangle([x, y, x + pw, y + 46], fill=st["color"])
        d.text((x + 12, y + 5), st["cat"], font=f_cat,
               fill=(255, 255, 255))
        head_lines = wrap(d, st["head"], f_head, pw - 24)
        hy = y + 54
        for ln in head_lines[:2]:
            d.text((x + 12, hy), ln, font=f_head, fill=INK)
            hy += 29
        body_lines = wrap(d, st["body"], f_body, pw - 24 - 92)
        by = hy + 6
        for ln in body_lines[:4]:
            if by + 22 > y + ph - 32:
                break
            d.text((x + 12, by), ln, font=f_body, fill=(40, 40, 44))
            by += 24
        motif(d, st["motif"], x + pw - 50, y + ph - 62, 68, st["color"])
        d.text((x + 12, y + ph - 24), "Sources: " + st["src"],
               font=f_src, fill=GREY)

    # Footer
    d.line([(mx, 972), (W - mx, 972)], fill=INK, width=2)
    f_foot = font(SANS, 16)
    foot = ("Every story verified against at least two independent "
            "reputable sources - Reuters, AP, BBC, WSJ, CNN, Le Monde.")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 982), foot, font=f_foot, fill=GREY)

    img = grain(img)
    img.save("poster.png", optimize=True)
    print("poster.png written")


if __name__ == "__main__":
    main()
