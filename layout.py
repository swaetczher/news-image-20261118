"""Konstanta layout + helper teks untuk gambar ringkasan berita.

Kanvas 1024 x 1024 (batas keras kompetisi: maks 1024x1024 px, <=1 MiB).
Syarat juri: terbaca di lebar ~300 px — jadi font tubuh minimal 26 px,
headline minimal 30 px, tanggal/judul jauh lebih besar.
Semua teks di-wrap dengan pengukuran font nyata (Pillow textlength),
bukan tebakan.
"""

W, H = 1024, 1024
MARGIN = 36
GUTTER = 16

# Warna (palet koran: navy gelap + aksen merah + kertas)
NAVY = (13, 27, 62)
NAVY_LIGHT = (24, 48, 96)
RED = (178, 34, 34)
PAPER = (250, 248, 243)
INK = (24, 24, 28)
MUTED = (88, 88, 96)
RULE = (200, 196, 188)
CARD_BG = (255, 255, 255)
CARD_BORDER = (222, 218, 210)

# Langit & laut untuk ilustrasi vektor sederhana
SKY = (176, 208, 232)
SEA = (46, 92, 138)
SEA_DARK = (30, 68, 110)
SMOKE = (120, 120, 124)
FLAME = (232, 116, 28)
FLAME2 = (244, 178, 44)

# Font (DejaVu tersedia di VM; fallback ke default Pillow)
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Geometri
HEADER_H = 180
HERO_TOP = HEADER_H + 14
HERO_H = 316
ROW_TOP = HERO_TOP + HERO_H + GUTTER
ROW_H = 292
STRIP_TOP = ROW_TOP + ROW_H + GUTTER
STRIP_H = 140
FOOTER_Y = H - 44


def wrap_text(draw, text, font, max_width):
    """Bungkus teks ke beberapa baris berdasarkan lebar piksel nyata."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
