#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

A newspaper front page built from scratch with PIL: a dark masthead with a
DATE CHECK box, three illustrated leads, a dark world map with eight
numbered pins, a day-in-figures strip, a six-continent band, a twenty-item
grid and a ticker. Every story was verified against reporting dated
Friday 20 November 2026 before it was drawn.

Story count: heroes 3 + map 8 + continents 6 + grid 20 + ticker 3 = 40.
The figures strip holds statistics, not stories. Deterministic output:
no timestamps, no randomness, fixed font paths.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (247, 243, 232)
PANEL = (255, 255, 255)
INK = (17, 17, 17)
RED = (176, 42, 42)
BLUE = (31, 78, 121)
GRAY = (102, 102, 102)
CREAM = (247, 243, 232)
GOLD = (201, 162, 39)
DARK = (20, 20, 20)
MAPBG = (26, 42, 58)
LAND = (216, 210, 189)
LANDLINE = (138, 132, 116)

FDIR = "/usr/share/fonts/truetype/dejavu"


def fnt(name, size):
    paths = {
        "serif": "DejaVuSerif-Bold.ttf",
        "serifreg": "DejaVuSerif.ttf",
        "sans": "DejaVuSans-Bold.ttf",
        "sansreg": "DejaVuSans.ttf",
    }
    return ImageFont.truetype(os.path.join(FDIR, paths[name]), size)


def wrap(dr, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if dr.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(dr, x, y, text, font, maxw, color, lh=None, align="left"):
    lh = lh or int(font.size * 1.28)
    for line in wrap(dr, text, font, maxw):
        if align == "center":
            dr.text((x + maxw / 2, y), line, font=font, fill=color, anchor="ma")
        else:
            dr.text((x, y), line, font=font, fill=color)
        y += lh
    return y


def rule(dr, x0, x1, y, width=2, color=INK):
    dr.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(dr, x, y, text, size=12):
    dr.text((x, y), text, font=fnt("sans", size), fill=RED)


# ---- Simplified continent outlines (lon, lat), hand-approximated ----
NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-70, 62), (-60, 55), (-55, 47),
                 (-65, 44), (-75, 38), (-80, 32), (-85, 29), (-90, 21),
                 (-97, 16), (-94, 17), (-86, 13), (-83, 9), (-79, 9),
                 (-85, 11), (-92, 14), (-100, 17), (-105, 20), (-110, 23),
                 (-114, 29), (-120, 34), (-125, 40), (-124, 48), (-130, 55),
                 (-140, 60), (-155, 58), (-165, 60)]
SOUTH_AMERICA = [(-79, 9), (-72, 11), (-62, 10), (-52, 5), (-50, 0),
                 (-44, -3), (-35, -8), (-40, -20), (-48, -27), (-57, -38),
                 (-65, -45), (-68, -52), (-70, -54), (-73, -50), (-73, -37),
                 (-70, -20), (-77, -12), (-81, -5), (-80, 1)]
AFRICA = [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31),
          (35, 28), (40, 15), (43, 11), (48, 11), (51, 10), (44, 0),
          (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
          (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
           (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
           (100, 77), (110, 74), (120, 73), (130, 72), (140, 72),
           (150, 70), (160, 69), (170, 66), (178, 65), (170, 60),
           (162, 56), (158, 52), (150, 59), (142, 55), (140, 50),
           (135, 43), (130, 38), (127, 35), (122, 38), (120, 32),
           (115, 23), (110, 20), (108, 18), (105, 10), (100, 8), (98, 12),
           (95, 16), (92, 21), (89, 22), (86, 20), (80, 15), (76, 10),
           (72, 20), (66, 25), (60, 25), (57, 27), (52, 28), (50, 29),
           (48, 30), (44, 29), (40, 32), (36, 36), (30, 36), (26, 38),
           (22, 37), (19, 42), (15, 44), (12, 44), (8, 44), (3, 43),
           (0, 40), (-2, 37), (-9, 37)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (-1, 51), (-4, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 38), (141, 41),
         (143, 43), (141, 45), (140, 42), (138, 38), (135, 35), (132, 33)]
ISLANDS_SE_ASIA = [(95, 5), (98, 3), (100, 0), (103, -2), (106, -6),
                    (110, -7), (114, -8), (118, -9), (120, -10), (119, -5),
                    (117, 0), (115, 3), (112, 5), (108, 2), (104, 1),
                    (100, 5)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
             (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
             (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
             (126, -14), (122, -17), (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -43), (174, -41), (177, -38), (175, -37),
               (173, -40), (169, -43)]
LAND_POLYS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, BRITAIN,
              JAPAN, ISLANDS_SE_ASIA, AUSTRALIA, NEW_ZEALAND]

MX, MY, MW, MH = 28, 362, 560, 120


def project(lon, lat):
    x = MX + (lon + 180.0) / 360.0 * MW
    y = MY + (78.0 - lat) / 136.0 * MH
    return (x, y)

# ============================ draw the page ============================
img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img)

# ---------- masthead ----------
dr.rectangle([0, 0, W, 98], fill=DARK)
dr.text((W / 2, 8), "THE DAILY GLOBE", font=fnt("serif", 52), fill=CREAM,
        anchor="ma")
para(dr, 28, 68,
     "FRIDAY 20 NOVEMBER 2026  •  40 STORIES  •  THREE LEADS  •  SIX CONTINENTS",
     fnt("sans", 13), 968, CREAM, align="center")
dr.rectangle([862, 12, 996, 56], fill=RED, outline=CREAM, width=1)
dr.text((929, 16), "DATE CHECK", font=fnt("sans", 11), fill=CREAM, anchor="ma")
dr.text((929, 32), "FRI 20 NOV 2026", font=fnt("sans", 11), fill=CREAM,
        anchor="ma")

# ---------- three leads ----------
LEADS = [
    ("LEAD  •  UKRAINE",
     "Russia smashes three Kyiv bridges in overnight barrage",
     "Ballistic strikes kill three in the capital and two in Lviv; power, "
     "water and heat cut. The attack came hours after Putin's Shenzhen talks.",
     "Reuters, AP, CNN  •  20 Nov"),
    ("LEAD  •  WEATHER",
     "Cyclone Akvan strikes Odisha as 300,000 flee",
     "Landfall near Gopalpur at 70–80 km/h; the third cyclone in a month. "
     "No major damage reported as the storm weakens inland.",
     "Reuters, IMD  •  20 Nov"),
    ("LEAD  •  MARKETS",
     "Anthropic slides 6% before the bell after record debut",
     "Day one closed at $97.17, up 17% on the $83 IPO price; $81.3bn raised, "
     "the biggest flotation ever.",
     "Bloomberg, CNBC  •  20 Nov"),
]
COLX = [28, 356, 684]
COLW = 312
for (kick, head, deck, src), x in zip(LEADS, COLX):
    kicker(dr, x, 108, kick)
    para(dr, x, 128, head, fnt("serif", 21), COLW, INK, lh=25)
    # illustration band y 208-260
    if x == COLX[0]:
        # bridge over a river, middle span hit
        bx, by = x, 212
        dr.rectangle([bx, by + 40, bx + COLW, by + 48], fill=BLUE)
        for i in range(3):
            ax = bx + 8 + i * 100
            dr.arc([ax, by + 8, ax + 88, by + 52], 180, 360, fill=INK, width=3)
            dr.line([(ax, by + 30), (ax + 88, by + 30)], fill=INK, width=3)
        for dx, dy in ((-6, -8), (0, -12), (6, -8), (-10, 0), (10, 0),
                       (-4, 6), (4, 6)):
            dr.line([(bx + 152 + dx, by + 2 + dy), (bx + 152, by + 2)],
                    fill=RED, width=2)
    elif x == COLX[1]:
        # cyclone spiral
        cx, cy = x + 40, 236
        for r in (34, 26, 18, 10):
            dr.arc([cx - r, cy - r, cx + r, cy + r], 30, 300, fill=BLUE,
                   width=4)
        dr.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
        dr.text((x + 88, 216), "70–80 km/h", font=fnt("sans", 15), fill=INK)
        dr.text((x + 88, 236), "gusts 90 km/h", font=fnt("sansreg", 12),
                fill=GRAY)
        dr.text((x + 88, 254), "300,000+ evacuated",
                font=fnt("sansreg", 12), fill=GRAY)
    else:
        # price bar $80-$115: IPO $83, open $111.50, close $97.17, pre $91.40
        px0, px1 = x, x + COLW
        def px(v):
            return px0 + (v - 80) / 35.0 * (px1 - px0)
        dr.rectangle([px0, 232, px1, 250], outline=INK, width=2)
        dr.rectangle([px(83), 232, px(97.17), 250], fill=BLUE)
        dr.line([(px(111.50), 224), (px(111.50), 258)], fill=GOLD, width=3)
        dr.line([(px(97.17), 224), (px(97.17), 258)], fill=RED, width=3)
        dr.text((px(111.50), 204), "$111.50 open", font=fnt("sans", 11),
                fill=INK, anchor="ma")
        dr.text((px(97.17), 258), "$97.17 close", font=fnt("sans", 11),
                fill=RED, anchor="ma")
        dr.text((px(83), 258), "$83 IPO", font=fnt("sans", 11), fill=GRAY,
                anchor="ma")
    para(dr, x, 272, deck, fnt("sansreg", 13), COLW, INK, lh=17)
    dr.text((x, 322), src, font=fnt("sansreg", 11), fill=GRAY)
rule(dr, 28, 996, 336, 2)

# ---------- dark world map + key ----------
kicker(dr, 28, 344, "THE WORLD — EIGHT PLACES IN THE NEWS", size=13)
dr.rectangle([MX, MY, MX + MW, MY + MH], fill=MAPBG, outline=INK, width=1)
for poly in LAND_POLYS:
    pts = [project(lon, lat) for lon, lat in poly]
    dr.polygon(pts, fill=LAND, outline=LANDLINE)
# (number, lon, lat, nudge_x, nudge_y)
PINS = [("1", 22.7, 50.5, 0, 0), ("2", 46.7, 24.7, 1, 2),
        ("3", 30.7, 36.9, -2, 2), ("4", 4.35, 50.85, 0, 0),
        ("5", -91.4, 40.8, 0, 0), ("6", 44.8, 41.7, 2, -2),
        ("7", 174.8, -41.3, 0, 0), ("8", 36.2, 50.0, 2, -2)]
for num, lon, lat, nx, ny in PINS:
    x, y = project(lon, lat)
    x, y = x + nx, y + ny
    dr.ellipse([x - 7, y - 7, x + 7, y + 7], fill=RED, outline=CREAM,
               width=2)
    dr.text((x, y - 1), num, font=fnt("sans", 9), fill=CREAM, anchor="mm")
KEY = ["1  POLAND — Unknown objects probed near Ukraine border",
       "2  RIYADH — Defences down Houthi missile, two drones",
       "3  ANTALYA — COP31 final day ends with no deal",
       "4  BRUSSELS — UK–EU summit: youth visas, 100,000 a year",
       "5  IOWA — Army delays unstable-explosives blast",
       "6  TBILISI — Georgia declares 22 Nov day of mourning",
       "7  WELLINGTON — Phillips 118; NZ 368 v India",
       "8  KHARKIV — Hospital hit by Russian drone; four hurt"]
ky = 364
for line in KEY:
    dr.text((608, ky), line, font=fnt("sansreg", 11), fill=INK)
    ky += 15
rule(dr, 28, 996, 492, 1)

# ---------- day in figures ----------
FIGS = [("3", "Kyiv bridges hit overnight"),
        ("$97.17", "Anthropic debut close, +17%"),
        ("300,000+", "evacuated for Cyclone Akvan"),
        ("100,000", "UK–EU youth visas a year")]
for i, (num, lab) in enumerate(FIGS):
    x = 28 + i * 242
    dr.rectangle([x, 500, x + 232, 552], fill=PANEL, outline=INK, width=1)
    dr.line([(x, 500), (x + 232, 500)], fill=RED, width=3)
    dr.text((x + 10, 508), num, font=fnt("serif", 20), fill=INK)
    dr.text((x + 10, 532), lab, font=fnt("sansreg", 10), fill=GRAY)

# ---------- six continents ----------
kicker(dr, 28, 562, "SIX CONTINENTS — ONE TOP STORY FROM EACH", size=13)
CONT = [("NORTH AMERICA", "Las Vegas GP practice washed out"),
        ("SOUTH AMERICA", "Argentina Senate backs disability law, 71–0"),
        ("EUROPE", "Youth protests sweep Europe over living costs"),
        ("AFRICA", "Egypt seals $2.3bn IMF deal"),
        ("ASIA", "Japan core inflation 2.2%; Dec hike eyed"),
        ("OCEANIA", "M5.6 quake off New Caledonia")]
for i, (cont, head) in enumerate(CONT):
    x = 28 + i * 163
    dr.rectangle([x, 580, x + 153, 632], fill=PANEL, outline=INK, width=1)
    dr.line([(x, 580), (x + 153, 580)], fill=RED, width=3)
    dr.text((x + 6, 584), cont, font=fnt("sans", 10), fill=RED)
    para(dr, x + 6, 598, head, fnt("sansreg", 11), 141, INK, lh=13)

# ---------- grid: 20 stories ----------
kicker(dr, 28, 642, "AROUND THE WORLD", size=13)
rule(dr, 28, 996, 660, 1)
GRID = [("PARIS", "Macron hosts Harris; talk of a 2028 run"),
        ("WASHINGTON", "White House taps Kirsten Davies as cyber chief"),
        ("USA", "Sanctions hit Comancheros and 'Ndrangheta"),
        ("USA", "Court curbs agriculture chief's emails"),
        ("BRUSSELS", "EU to summon Russian envoy over Kyiv damage"),
        ("PENTAGON", "US–Iran war cost put at $48.3bn"),
        ("LEBANON", "Israeli strike hits Hezbollah missile site"),
        ("MARKETS", "Dollar nears 19-month high on AI jitters"),
        ("TORONTO", "Telus jumps 12% as BCE weighs rival bid"),
        ("SUPREME COURT", "Trump asks justices to let EPA axe climate grants"),
        ("SHENZHEN", "APEC summit plays backdrop to power politics"),
        ("ANTALYA", "Venezuela touts AI for cleaner oil at COP31"),
        ("USA", "FEMA hit by bed bug infestation"),
        ("TEXAS", "Execution takes over an hour to carry out"),
        ("BASEBALL", "Ex-MLB pitcher Lance Broadway dies at 43"),
        ("TURIN", "Zverev 3–0; Alcaraz to face Shelton in semis"),
        ("DELHI", "Jayawardene to run Capitals' WPL side"),
        ("ROME", "Italy's young 'targeted on security, ignored on economy'"),
        ("YEMEN", "'It's just fireworks': life in a besieged city"),
        ("PARIS", "Macron backs Diallo's bid for FIFA presidency")]
for i, (place, head) in enumerate(GRID):
    col, row = i % 4, i // 4
    x, y = 28 + col * 242, 668 + row * 54
    dr.text((x, y), place, font=fnt("sans", 10), fill=RED)
    para(dr, x, y + 14, head, fnt("sansreg", 11), 230, INK, lh=13)

# ---------- ticker + footer ----------
rule(dr, 28, 996, 944, 2)
dr.text((28, 952), "ALSO TODAY", font=fnt("sans", 12), fill=RED)
dr.text((150, 952),
        "South Africa holds rates  •  Macron urges debate on Ukraine's NATO "
        "entry  •  Hamilton: 'not even thought about' new Ferrari deal",
        font=fnt("sansreg", 11), fill=INK)
rule(dr, 28, 996, 978, 1)
para(dr, 28, 986,
     "The Daily Globe  •  Friday 20 November 2026  •  40 stories  •  "
     "Sources: Reuters, CNN, AP, BBC, Bloomberg, USGS, IMD, Le Monde, WSJ",
     fnt("sansreg", 11), 968, GRAY, align="center")
dr.rectangle([0, 1016, W, H], fill=RED)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
