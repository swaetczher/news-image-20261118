"""Data berita dunia Rabu 18 November 2026 — dari riset.md (Riset, 18 Nov ~23:50 WIB).

Semua fakta terverifikasi tanggalnya dari >=2 sumber independen.
HATI-HATI:
- Peltola: proyeksi Selasa malam ET, dilaporkan luas Rabu — tulis
  "called overnight", JANGAN "voted today".
- Klaim dagang Trump–Filipina: TIDAK ADA yang ditandatangani — tulis
  "CLAIMS", JANGAN "deal agreed" sebagai fakta.
- Klaim Iran soal kerusakan Patriot di Kuwait: belum terverifikasi —
  JANGAN dicantumkan sebagai fakta.
- Angin Akvan pakai buletin terbaru IMD: 90–100 km/jam, gust 110.
- JANGAN pakai sebagai berita 18 Nov: putusan ICJ Myanmar (19 Nov),
  KTT tiga pihak (19 Nov), pendaratan Akvan (20 Nov), runtuhnya
  Jembatan Kerch (17 Nov — hanya lanjutan/aftermath di strip).
"""

TITLE = "THE WORLD IN ONE DAY"
DATE_LINE = "WEDNESDAY, 18 NOVEMBER 2026"
SUBTITLE = "Five stories from around the world — in one picture"

HERO = {
    "tag": "CHINA  •  TOP STORY",
    "headline": "XI HUGS TRUMP IN SHENZHEN",
    "body": (
        "Rare tarmac welcome as APEC opens; first-ever "
        "Trump–Xi–Putin summit Thursday."
    ),
    "art": "shenzhen",
}

PANELS = [
    {
        "tag": "MIDDLE EAST",
        "headline": "GULF WAR WIDENS",
        "body": (
            "Iran drones US bases in Kuwait and Bahrain at dawn."
        ),
        "art": "gulf",
    },
    {
        "tag": "ASIA  •  WEATHER",
        "headline": "CYCLONE AKVAN",
        "body": (
            "Strengthens to a severe storm; red alert, "
            "landfall Friday."
        ),
        "art": "cyclone",
    },
    {
        "tag": "USA  •  ELECTION",
        "headline": "ALASKA GOES BLUE",
        "body": (
            "Peltola flips final seat overnight; Democrats 56–44."
        ),
        "art": "alaska",
    },
]

STRIP = [
    (
        "TRUMP CLAIMS PHILIPPINES DEAL",
        "Trump hails a 'very big' trade deal in Manila — but nothing "
        "signed, Manila silent on terms.",
    ),
    (
        "KERCH AFTERMATH",
        "Rail traffic resumes on the Crimea bridge; road span still "
        "down in the strait.",
    ),
]

FOOTER = "Sources: AFP · AP · Reuters · Bloomberg · IMD · CNN — 18 November 2026"
