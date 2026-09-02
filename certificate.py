# -*- coding: utf-8 -*-
"""Generates the YCC membership certificate by compositing member data
onto the fixed certificate_template.png (labels/design always stay Uzbek
and identical to the original template — only name, grade, school and
photo change)."""

import io
from PIL import Image, ImageDraw, ImageFont, ImageOps

TEMPLATE_PATH = "assets/certificate_template.png"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Pixel regions measured against the 1086x1448 template.
PHOTO_BOX = (634, 205, 971, 645)          # (x0, y0, x1, y1)
PHOTO_RADIUS = 28

NAME_BOX = (200, 818, 590, 862)
GRADE_BOX = (200, 918, 590, 958)
SCHOOL_BOX = (200, 1012, 590, 1058)

TEXT_COLOR = (13, 33, 66)  # dark navy matching template text
BG_COLOR = (249, 248, 247)  # off-white background, sampled from template

# The underline sits just below each value's baseline in the template;
# we whiteout only up to just above that underline so it stays intact.
NAME_CLEAR = (196, 812, 585, 858)
GRADE_CLEAR = (196, 913, 585, 954)
SCHOOL_CLEAR = (196, 1012, 585, 1054)


def _fit_font(text: str, box, max_size=34, min_size=14):
    """Return a font object sized so `text` fits inside box width."""
    box_w = box[2] - box[0]
    size = max_size
    while size > min_size:
        font = ImageFont.truetype(FONT_BOLD, size)
        w = font.getbbox(text)[2]
        if w <= box_w:
            return font
        size -= 1
    return ImageFont.truetype(FONT_BOLD, min_size)


def _paste_photo(canvas: Image.Image, photo_bytes: bytes):
    photo = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
    photo = ImageOps.exif_transpose(photo)

    box_w = PHOTO_BOX[2] - PHOTO_BOX[0]
    box_h = PHOTO_BOX[3] - PHOTO_BOX[1]

    # Cover-fit crop (like CSS object-fit: cover)
    src_w, src_h = photo.size
    target_ratio = box_w / box_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        offset = (src_w - new_w) // 2
        photo = photo.crop((offset, 0, offset + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        offset = (src_h - new_h) // 2
        photo = photo.crop((0, offset, src_w, offset + new_h))

    photo = photo.resize((box_w, box_h), Image.LANCZOS)

    # Rounded-rectangle mask so corners match the template's frame
    mask = Image.new("L", (box_w, box_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, box_w, box_h), radius=PHOTO_RADIUS, fill=255)

    canvas.paste(photo, (PHOTO_BOX[0], PHOTO_BOX[1]), mask)


def _draw_text_line(draw: ImageDraw.ImageDraw, text: str, box, clear_box):
    draw.rectangle(clear_box, fill=BG_COLOR)
    font = _fit_font(text, box)
    x0, y0, x1, y1 = box
    # vertical center within the box
    bbox = font.getbbox(text)
    text_h = bbox[3] - bbox[1]
    y = y0 + ((y1 - y0) - text_h) // 2 - bbox[1]
    draw.text((x0, y), text, font=font, fill=TEXT_COLOR)


def generate_certificate(full_name: str, school: str, grade: int, photo_bytes: bytes) -> bytes:
    """Build the final certificate PNG and return raw bytes."""
    canvas = Image.open(TEMPLATE_PATH).convert("RGB")

    # Photo first (so it sits behind nothing else needs to be drawn over it)
    _paste_photo(canvas, photo_bytes)

    draw = ImageDraw.Draw(canvas)
    _draw_text_line(draw, full_name, NAME_BOX, NAME_CLEAR)
    _draw_text_line(draw, f"{grade}-sinf", GRADE_BOX, GRADE_CLEAR)
    _draw_text_line(draw, school, SCHOOL_BOX, SCHOOL_CLEAR)

    out = io.BytesIO()
    canvas.save(out, format="PNG")
    out.seek(0)
    return out.getvalue()
