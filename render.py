"""Renderer gambar ringkasan berita (Pillow saja, tanpa dependensi lain).

Satu fungsi publik: render_image(path) -> (width, height).
Deterministik: tanpa network, tanpa waktu acak, font & koordinat tetap
— dua run menghasilkan byte yang identik.
Semua teks diukur dengan textlength sebelum digambar, jadi tidak ada
teks yang keluar kanvas atau tumpang-tindih.
Ilustrasi bergaya kartun editorial / siluet — tanpa wajah fotorealistis.
"""

import os

from PIL import Image, ImageDraw, ImageFont

import layout
import news_data


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def _fit_font(draw, text, path, start_size, max_width, min_size=18):
    """Kecilkan font sampai teks muat dalam max_width."""
    size = start_size
    while size > min_size:
        font = _font(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return _font(path, min_size)


# ---------------------------------------------------------------- ilustrasi
def _draw_shenzhen(draw, x, y, w, h):
    """Air Force One + karpet merah + dua pemimpin bersiluet di Shenzhen."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.SKY)
    # matahari kecil
    draw.ellipse([x + w - 70, y + 16, x + w - 26, y + 60], fill=(255, 214, 90))
    # jet pengawal kecil
    jx, jy = x + int(w * 0.62), y + 26
    draw.polygon(
        [(jx, jy), (jx + 34, jy + 8), (jx, jy + 14), (jx + 8, jy + 7)],
        fill=(40, 40, 46),
    )
    # landasan
    run_y = y + int(h * 0.68)
    draw.rectangle([x, run_y, x + w, y + h], fill=(70, 72, 78))
    draw.rectangle([x, run_y, x + w, run_y + 6], fill=(220, 220, 224))
    # Air Force One: badan putih + garis biru + ekor
    fx, fy = x + 16, y + int(h * 0.30)
    draw.polygon(
        [(fx + 150, fy - 52), (fx + 168, fy - 52), (fx + 168, fy + 6),
         (fx + 150, fy + 6)],
        fill=layout.NAVY,
    )
    draw.ellipse([fx + 152, fy - 58, fx + 166, fy - 44], fill=(255, 214, 90))
    draw.rounded_rectangle(
        [fx, fy, fx + 300, fy + 52], radius=22, fill=(245, 245, 248),
    )
    draw.rectangle([fx + 6, fy + 30, fx + 296, fy + 44], fill=(30, 60, 140))
    for wx in range(fx + 40, fx + 260, 26):
        draw.rectangle([wx, fy + 12, wx + 12, fy + 20], fill=layout.NAVY)
    # tangga pesawat
    draw.line([fx + 250, fy + 52, fx + 224, run_y], fill=(200, 200, 204), width=8)
    # karpet merah
    car_y = run_y + 26
    draw.rectangle([x + 30, car_y, x + w - 30, car_y + 22], fill=(178, 34, 34))
    draw.rectangle([x + 30, car_y, x + w - 30, car_y + 4], fill=(200, 60, 60))
    # dua siluet pemimpin berjabat tangan di karpet merah
    for sx, suit, tie in (
        (x + int(w * 0.42), (24, 24, 30), (178, 34, 34)),
        (x + int(w * 0.58), (30, 30, 36), (30, 60, 140)),
    ):
        draw.ellipse([sx - 13, car_y - 58, sx + 13, car_y - 32], fill=(232, 196, 160))
        draw.rounded_rectangle(
            [sx - 20, car_y - 32, sx + 20, car_y + 22], radius=10, fill=suit,
        )
        draw.polygon(
            [(sx - 4, car_y - 30), (sx + 4, car_y - 30), (sx, car_y - 8)],
            fill=tie,
        )
    # jabat tangan di antara keduanya
    draw.ellipse(
        [x + int(w * 0.50) - 8, car_y - 14, x + int(w * 0.50) + 8, car_y + 2],
        fill=(232, 196, 160),
    )
    # bendera AS (kiri) dan China (kanan) di tiang
    for fx0, cols in (
        (x + 18, "us"),
        (x + w - 18 - 46, "cn"),
    ):
        fy0 = run_y - 74
        draw.line([fx0 + 2, fy0, fx0 + 2, run_y], fill=(60, 60, 66), width=3)
        if cols == "us":
            for i in range(5):
                draw.rectangle(
                    [fx0 + 4, fy0 + i * 7, fx0 + 46, fy0 + (i + 1) * 7],
                    fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255),
                )
            draw.rectangle([fx0 + 4, fy0, fx0 + 20, fy0 + 14], fill=(30, 50, 110))
        else:
            draw.rectangle([fx0 + 4, fy0, fx0 + 46, fy0 + 35], fill=(222, 40, 40))
            draw.ellipse([fx0 + 10, fy0 + 8, fx0 + 22, fy0 + 20], fill=(255, 220, 60))
    # pasukan kehormatan: baris siluet kecil
    for gx in range(x + 24, x + w - 24, 34):
        draw.ellipse([gx, run_y - 26, gx + 12, run_y - 14], fill=(40, 40, 46))
        draw.rectangle([gx - 2, run_y - 14, gx + 14, run_y], fill=(40, 40, 46))


def _draw_gulf(draw, x, y, w, h):
    """Drone menuju pangkalan Teluk + tanker di Selat Hormuz."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.SKY)
    sea_y = y + int(h * 0.55)
    draw.rectangle([x, sea_y, x + w, y + h], fill=layout.SEA)
    # pangkalan kecil di kanan (menara + radar)
    bx = x + w - 66
    draw.rectangle([bx, sea_y - 26, bx + 52, sea_y + 30], fill=(90, 90, 96))
    draw.rectangle([bx + 8, sea_y - 40, bx + 18, sea_y - 26], fill=(60, 60, 66))
    draw.ellipse([bx + 22, sea_y - 46, bx + 40, sea_y - 28], fill=(200, 200, 204))
    # ledakan kecil di pangkalan (tetap di dalam area seni)
    draw.polygon(
        [(bx + 30, sea_y - 30), (bx + 38, sea_y - 48), (bx + 46, sea_y - 30)],
        fill=layout.FLAME,
    )
    # dua drone quad (silang + 4 rotor)
    for dx, dy in ((x + 40, y + 18), (x + 110, y + 30)):
        draw.line([dx - 10, dy - 8, dx + 10, dy + 8], fill=(30, 30, 36), width=3)
        draw.line([dx - 10, dy + 8, dx + 10, dy - 8], fill=(30, 30, 36), width=3)
        for ox, oy in ((-10, -8), (10, -8), (-10, 8), (10, 8)):
            draw.ellipse([dx + ox - 4, dy + oy - 3, dx + ox + 4, dy + oy + 3],
                         fill=(60, 60, 66))
        draw.rectangle([dx - 5, dy - 4, dx + 5, dy + 4], fill=(30, 30, 36))
    # garis arah drone ke pangkalan
    draw.line([x + 120, y + 34, bx + 10, sea_y - 52], fill=(255, 255, 255), width=2)
    # tanker kecil di laut
    hx, hy = x + 14, sea_y + 12
    draw.polygon(
        [(hx, hy), (hx + 110, hy), (hx + 98, hy + 22), (hx + 10, hy + 22)],
        fill=(30, 30, 36),
    )
    draw.rectangle([hx + 16, hy - 12, hx + 40, hy], fill=(200, 60, 60))


def _draw_cyclone(draw, x, y, w, h):
    """Pusaran siklon besar di Teluk Benggala menuju pantai India."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 68, 120))
    # daratan India di kanan
    draw.polygon(
        [(x + w - 52, y), (x + w, y), (x + w, y + h),
         (x + w - 66, y + h), (x + w - 78, y + int(h * 0.55)),
         (x + w - 58, y + int(h * 0.30))],
        fill=(70, 130, 80),
    )
    # pusaran: busur konsentris putih
    cx, cy = x + int(w * 0.42), y + int(h * 0.52)
    for r, wd in ((58, 7), (44, 7), (30, 7), (16, 6)):
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=20, end=300, fill=(255, 255, 255), width=wd,
        )
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 214, 90))
    # panah ke daratan (landfall Friday)
    ay = cy + 6
    draw.line([cx + 62, ay, x + w - 72, ay], fill=(255, 214, 90), width=5)
    draw.polygon(
        [(x + w - 72, ay), (x + w - 88, ay - 9), (x + w - 88, ay + 9)],
        fill=(255, 214, 90),
    )


def _draw_alaska(draw, x, y, w, h):
    """Skor Senat 56–44 + bilah biru/merah."""
    draw.rectangle([x, y, x + w, y + h], fill=layout.NAVY)
    # bintang kecil
    sx, sy = x + 26, y + 20
    draw.polygon(
        [(sx, sy - 10), (sx + 3, sy - 3), (sx + 10, sy - 2), (sx + 5, sy + 3),
         (sx + 7, sy + 10), (sx, sy + 6), (sx - 7, sy + 10), (sx - 5, sy + 3),
         (sx - 10, sy - 2), (sx - 3, sy - 3)],
        fill=(255, 214, 90),
    )
    score_font = _font(layout.FONT_SANS_BOLD, 40)
    draw.text(
        (x + w / 2, y + 14), "56–44", font=score_font,
        fill=(255, 255, 255), anchor="ma",
    )
    # bilah Senat: 56 biru, 44 merah
    bar_y = y + h - 26
    blue_w = int((w - 36) * 0.56)
    draw.rectangle([x + 18, bar_y, x + 18 + blue_w, bar_y + 12], fill=(40, 110, 220))
    draw.rectangle(
        [x + 18 + blue_w, bar_y, x + w - 18, bar_y + 12], fill=(200, 60, 60),
    )


ART = {
    "shenzhen": _draw_shenzhen,
    "gulf": _draw_gulf,
    "cyclone": _draw_cyclone,
    "alaska": _draw_alaska,
}


# ---------------------------------------------------------------- render utama
def render_image(out_path):
    img = Image.new("RGB", (layout.W, layout.H), layout.PAPER)
    draw = ImageDraw.Draw(img)

    # --- Header navy ---
    draw.rectangle([0, 0, layout.W, layout.HEADER_H], fill=layout.NAVY)
    draw.rectangle(
        [0, layout.HEADER_H - 6, layout.W, layout.HEADER_H], fill=layout.RED
    )
    date_font = _font(layout.FONT_SANS_BOLD, 34)
    title_font = _fit_font(
        draw, news_data.TITLE, layout.FONT_SERIF_BOLD,
        64, layout.W - 2 * layout.MARGIN,
    )
    sub_font = _font(layout.FONT_SANS, 26)

    y = 16
    draw.text(
        (layout.W / 2, y), news_data.DATE_LINE, font=date_font,
        fill=(255, 214, 90), anchor="ma",
    )
    y += 46
    draw.text(
        (layout.W / 2, y), news_data.TITLE, font=title_font,
        fill=(255, 255, 255), anchor="ma",
    )
    y += 72
    draw.text(
        (layout.W / 2, y), news_data.SUBTITLE, font=sub_font,
        fill=(214, 222, 240), anchor="ma",
    )

    # --- Panel hero ---
    x0 = layout.MARGIN
    card_w = layout.W - 2 * layout.MARGIN
    hy = layout.HERO_TOP
    draw.rounded_rectangle(
        [x0, hy, x0 + card_w, hy + layout.HERO_H],
        radius=12, fill=layout.CARD_BG,
        outline=layout.CARD_BORDER, width=2,
    )
    art_w = 400
    ART[news_data.HERO["art"]](draw, x0 + 2, hy + 2, art_w - 2, layout.HERO_H - 4)
    tx = x0 + art_w + 26
    tw = card_w - art_w - 52
    tag_font = _font(layout.FONT_SANS_BOLD, 24)
    head_font = _font(layout.FONT_SERIF_BOLD, 40)
    body_font = _font(layout.FONT_SANS, 27)
    ty = hy + 26
    draw.text((tx, ty), news_data.HERO["tag"], font=tag_font, fill=layout.RED)
    ty += 40
    for line in layout.wrap_text(draw, news_data.HERO["headline"], head_font, tw)[:2]:
        draw.text((tx, ty), line, font=head_font, fill=layout.INK)
        ty += 48
    ty += 6
    for line in layout.wrap_text(draw, news_data.HERO["body"], body_font, tw)[:3]:
        draw.text((tx, ty), line, font=body_font, fill=layout.MUTED)
        ty += 36

    # --- Baris 3 panel ---
    pw = 306
    ptag_font = _font(layout.FONT_SANS_BOLD, 22)
    phead_font = _font(layout.FONT_SERIF_BOLD, 28)
    pbody_font = _font(layout.FONT_SANS, 23)
    for i, panel in enumerate(news_data.PANELS):
        px = x0 + i * (pw + layout.GUTTER)
        py = layout.ROW_TOP
        draw.rounded_rectangle(
            [px, py, px + pw, py + layout.ROW_H],
            radius=12, fill=layout.CARD_BG,
            outline=layout.CARD_BORDER, width=2,
        )
        ART[panel["art"]](draw, px + 2, py + 2, pw - 4, 96)
        ty = py + 108
        draw.text((px + 18, ty), panel["tag"], font=ptag_font, fill=layout.RED)
        ty += 30
        for line in layout.wrap_text(
            draw, panel["headline"], phead_font, pw - 36
        )[:2]:
            draw.text((px + 18, ty), line, font=phead_font, fill=layout.INK)
            ty += 34
        ty += 2
        for line in layout.wrap_text(
            draw, panel["body"], pbody_font, pw - 36
        )[:3]:
            draw.text((px + 18, ty), line, font=pbody_font, fill=layout.MUTED)
            ty += 27

    # --- Strip bawah ---
    sy = layout.STRIP_TOP
    draw.rounded_rectangle(
        [x0, sy, x0 + card_w, sy + layout.STRIP_H],
        radius=12, fill=layout.CARD_BG,
        outline=layout.CARD_BORDER, width=2,
    )
    stag_font = _font(layout.FONT_SANS_BOLD, 22)
    sbody_font = _font(layout.FONT_SANS, 23)
    col_w = (card_w - 60) // 2
    for i, (tag, text) in enumerate(news_data.STRIP):
        cx = x0 + 24 + i * (col_w + 36)
        if i == 1:
            draw.line(
                [cx - 18, sy + 16, cx - 18, sy + layout.STRIP_H - 16],
                fill=layout.RULE, width=2,
            )
        ty = sy + 16
        draw.text((cx, ty), tag, font=stag_font, fill=layout.RED)
        ty += 34
        for line in layout.wrap_text(draw, text, sbody_font, col_w)[:3]:
            draw.text((cx, ty), line, font=sbody_font, fill=layout.MUTED)
            ty += 28

    # --- Footer ---
    foot_font = _font(layout.FONT_SANS, 22)
    draw.text(
        (layout.W / 2, layout.FOOTER_Y), news_data.FOOTER,
        font=foot_font, fill=layout.MUTED, anchor="ma",
    )

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    img.save(out_path, "PNG")
    return img.size
