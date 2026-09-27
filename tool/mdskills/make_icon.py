# -*- coding: utf-8 -*-
"""Napravi icon.ico za mdskills, bez ijedne vanjske biblioteke.

PNG se sastavi rucno (zlib je u standardnoj biblioteci), pa se zapakira u
ICO kontejner. Windows od Viste prihvaca PNG unutar ICO-a, pa je dovoljna
jedna velika slicica: sustav je sam smanjuje.

Motiv: tamni zaobljeni kvadrat, tri retka teksta, gornji u akcentnoj boji.
Citljivo i na 16 px, gdje se vidi samo silueta.
"""
import io
import os
import struct
import zlib

SIZE = 256
BG = (28, 25, 19, 255)          # topla gotovo crna, ista obitelj kao alat
EDGE = (60, 54, 44, 255)
ACCENT = (255, 90, 43, 255)     # flare
INK = (243, 238, 227, 255)
INK_DIM = (150, 142, 126, 255)


def blank(w, h, rgba):
    return [[rgba for _ in range(w)] for _ in range(h)]


def rounded_rect(px, x0, y0, x1, y1, r, color):
    for y in range(max(0, y0), min(len(px), y1 + 1)):
        for x in range(max(0, x0), min(len(px[0]), x1 + 1)):
            dx = dy = 0
            if x < x0 + r:
                dx = x0 + r - x
            elif x > x1 - r:
                dx = x - (x1 - r)
            if y < y0 + r:
                dy = y0 + r - y
            elif y > y1 - r:
                dy = y - (y1 - r)
            if dx * dx + dy * dy <= r * r:
                px[y][x] = color


def png_bytes(px):
    h, w = len(px), len(px[0])
    raw = bytearray()
    for row in px:
        raw.append(0)                       # filtar 0 po redu
        for (r, g, b, a) in row:
            raw += bytes((r, g, b, a))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def ico_bytes(png, size):
    w = 0 if size >= 256 else size          # 0 znaci 256 u ICO zapisu
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(png), 22)
    return header + entry + png


def build():
    px = blank(SIZE, SIZE, (0, 0, 0, 0))

    # tijelo: rub pa unutrasnjost, da se dobije hairline obrub
    rounded_rect(px, 8, 8, SIZE - 9, SIZE - 9, 46, EDGE)
    rounded_rect(px, 11, 11, SIZE - 12, SIZE - 12, 43, BG)

    # tri retka: prvi u akcentu, dva prigusena
    left, bar_h, radius = 54, 22, 11
    rows = [(78, 148, ACCENT), (124, 122, INK), (170, 96, INK_DIM)]
    for (top, width, color) in rows:
        rounded_rect(px, left, top, left + width, top + bar_h, radius, color)

    png = png_bytes(px)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    with open(out, "wb") as f:
        f.write(ico_bytes(png, SIZE))
    print("napravljeno: %s  (%d bajtova, %dx%d PNG unutar ICO-a)"
          % (out, os.path.getsize(out), SIZE, SIZE))


if __name__ == "__main__":
    build()
