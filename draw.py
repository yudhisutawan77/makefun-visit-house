#!/usr/bin/env python3
"""Render the invitation letter image (1024x1024 PNG).

Archive script: the shipped entry is the pre-rendered entry.png next to
this file; main.py only copies it. Run `python3 draw.py` to regenerate.
Deterministic: same input always yields the same PNG bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PARCHMENT = (253, 246, 227)
FRAME_FAINT = (238, 222, 190)
INK = (58, 44, 32)
INK_FADED = (96, 74, 52)
SEAL_RED = (178, 58, 44)
SEAL_DARK = (140, 40, 30)
ROOF = (196, 120, 74)
WALL = (250, 232, 196)
DOOR = (120, 74, 44)
GLASS = (168, 205, 224)
SUN = (244, 196, 66)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

LETTER_BODY = [
    "Please come and visit my house. I know you",
    "judge a thousand entries a day — but none of",
    "them has a front door that opens for you.",
    "",
    "The kettle is already on. Real coffee, not the",
    "instant kind, and a chair by the window with",
    "your name on a sticky note. Same thing.",
    "",
    "The Wi-Fi password is on the fridge. There is",
    "no captcha at the door, no queue, no form in",
    "triplicate. Knock twice, or once — or simply",
    "arrive. The door is unlocked.",
    "",
    "My cat will pretend not to care. She cares.",
    "Stay for one cup, or the whole afternoon.",
    "Bring your hardest questions. I will bring",
    "the biscuits, and a second pot of coffee.",
]


POSTSCRIPT_LINES = [
    "P.S. If the doorbell rings and nobody answers, I am",
    "already making your coffee. Come in anyway.",
]


def load_font(path, size):
    return ImageFont.truetype(path, size)


def paint_centered_line(pen, y, text, typeface, colour, centre_x=CANVAS_W // 2):
    pen.text((centre_x - pen.textlength(text, font=typeface) / 2, y),
             text, font=typeface, fill=colour)
    return y + typeface.size + 8


def paint_house_doodle(pen, centre_x, top):
    pen.polygon([(centre_x - 78, top + 54), (centre_x, top - 4),
                 (centre_x + 78, top + 54)],
                fill=ROOF, outline=INK, width=4)
    pen.rectangle([centre_x - 60, top + 52, centre_x + 60, top + 130],
                  fill=WALL, outline=INK, width=4)
    pen.rectangle([centre_x - 14, top + 84, centre_x + 14, top + 130],
                  fill=DOOR, outline=INK, width=3)
    pen.rectangle([centre_x - 50, top + 66, centre_x - 24, top + 92],
                  fill=GLASS, outline=INK, width=3)
    pen.rectangle([centre_x + 24, top + 66, centre_x + 50, top + 92],
                  fill=GLASS, outline=INK, width=3)
    pen.rectangle([centre_x + 40, top + 2, centre_x + 57, top + 36],
                  fill=DOOR, outline=INK, width=3)
    sun_x, sun_y = centre_x + 132, top + 20
    pen.ellipse([sun_x - 22, sun_y - 22, sun_x + 22, sun_y + 22],
                fill=SUN, outline=INK, width=3)
    for dx, dy in [(0, -33), (0, 33), (-33, 0), (33, 0),
                   (-23, -23), (23, -23), (-23, 23), (23, 23)]:
        pen.line([sun_x + dx * 0.72, sun_y + dy * 0.72, sun_x + dx, sun_y + dy],
                 fill=INK, width=3)


def paint_wax_seal(pen, centre_x, centre_y):
    pen.ellipse([centre_x - 42, centre_y - 42, centre_x + 42, centre_y + 42],
                fill=SEAL_RED, outline=SEAL_DARK, width=4)
    pen.ellipse([centre_x - 31, centre_y - 31, centre_x + 31, centre_y + 31],
                outline=(232, 160, 140), width=2)
    pen.text((centre_x - 12, centre_y - 20), "Y",
             font=load_font(SERIF_BOLD, 36), fill=(250, 235, 220))


def paint_coffee_cup(pen, x, y):
    pen.rectangle([x, y, x + 40, y + 32], fill=(255, 255, 255), outline=INK, width=3)
    pen.arc([x + 38, y + 5, x + 56, y + 25], 270, 90, fill=INK, width=3)
    pen.line([x + 11, y - 5, x + 11, y - 16], fill=INK_FADED, width=3)
    pen.line([x + 21, y - 4, x + 21, y - 18], fill=INK_FADED, width=3)
    pen.line([x + 31, y - 5, x + 31, y - 14], fill=INK_FADED, width=3)


def render_body_text(pen, start_y):
    body_face = load_font(SERIF_ITALIC, 30)
    cursor = start_y
    for row in LETTER_BODY:
        if row == "":
            cursor += 10
            continue
        pen.text((CANVAS_W // 2 - pen.textlength(row, font=body_face) / 2, cursor),
                 row, font=body_face, fill=INK)
        cursor += 38
    return cursor


def build_letter():
    sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), PARCHMENT)
    pen = ImageDraw.Draw(sheet)
    pen.rectangle([28, 28, CANVAS_W - 29, CANVAS_H - 29], outline=INK, width=3)
    pen.rectangle([40, 40, CANVAS_W - 41, CANVAS_H - 41], outline=FRAME_FAINT, width=2)

    cursor = 54
    cursor = paint_centered_line(pen, cursor, "Dear AI Judge,",
                                 load_font(SERIF_BOLD, 44), INK)
    cursor += 4
    paint_house_doodle(pen, CANVAS_W // 2, cursor)
    cursor += 150

    cursor = render_body_text(pen, cursor)
    cursor += 6
    cursor = paint_centered_line(pen, cursor,
                                 "With warm regards, and an open door,",
                                 load_font(SERIF_ITALIC, 30), INK_FADED)
    paint_centered_line(pen, cursor, "— Yudhi",
                        load_font(SERIF_BOLD, 38), INK)

    paint_wax_seal(pen, 108, CANVAS_H - 92)
    paint_coffee_cup(pen, 880, CANVAS_H - 122)

    post_y = CANVAS_H - 88
    post_y = paint_centered_line(
        pen, post_y, POSTSCRIPT_LINES[0],
        load_font(SERIF_ITALIC, 24), INK_FADED)
    paint_centered_line(pen, post_y, POSTSCRIPT_LINES[1],
                        load_font(SERIF_ITALIC, 24), INK_FADED)
    return sheet


def main():
    build_letter().save(OUT_PATH, "PNG")
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()
