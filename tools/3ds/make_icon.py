#!/usr/bin/env python3
"""Make the 3DS app icon from the Mumbo token sprite in a bk.o2r.

The icon is game art, so it is never committed: each build takes it from the player's own
bk.o2r. Needs only the standard library.

Usage: make_icon.py <bk.o2r> <icon.png>
"""
import struct
import sys
import zipfile
import zlib

SPRITE = "assets/sprite/ASSET_41A_MUMBO_TOKEN_0"  # frame 0 faces the camera
ICON_SIZE = 48
ART_SIZE = 46  # leaves a pixel of margin on each side
RESOURCE_HEADER = 64


def read_texture(archive, path):
    data = archive.read(path)
    _, width, height, size = struct.unpack_from("<4I", data, RESOURCE_HEADER)
    return width, height, data[RESOURCE_HEADER + 16 : RESOURCE_HEADER + 16 + size]


def decode_sprite(archive):
    """The CI4 frame as rows of (r, g, b, a) in 0..1, alpha premultiplied."""
    width, height, pixels = read_texture(archive, SPRITE + "_0")
    _, _, tlut = read_texture(archive, SPRITE + "_TLUT")
    palette = []
    for i in range(16):
        (v,) = struct.unpack_from(">H", tlut, i * 2)  # RGBA5551
        a = float(v & 1)
        palette.append(((v >> 11 & 31) / 31 * a, (v >> 6 & 31) / 31 * a, (v >> 1 & 31) / 31 * a, a))
    image = []
    for y in range(height):
        row = []
        for x in range(width):
            byte = pixels[(y * width + x) // 2]
            row.append(palette[byte >> 4 if x % 2 == 0 else byte & 15])
        image.append(row)
    return image


def crop(image):
    rows = [y for y, row in enumerate(image) if any(p[3] > 0 for p in row)]
    cols = [x for x in range(len(image[0])) if any(row[x][3] > 0 for row in image)]
    return [row[cols[0] : cols[-1] + 1] for row in image[rows[0] : rows[-1] + 1]]


def resize(image, width, height):
    """Area-average resampling: each output pixel averages the source area it covers."""
    src_h, src_w = len(image), len(image[0])
    sx, sy = src_w / width, src_h / height

    def spans(i, scale, limit):
        start, end = i * scale, (i + 1) * scale
        for s in range(int(start), min(limit, int(end + 0.9999))):
            weight = min(end, s + 1) - max(start, s)
            if weight > 0:
                yield s, weight

    out = []
    for y in range(height):
        row = []
        for x in range(width):
            acc = [0.0, 0.0, 0.0, 0.0]
            for v, wy in spans(y, sy, src_h):
                for u, wx in spans(x, sx, src_w):
                    for c in range(4):
                        acc[c] += image[v][u][c] * wx * wy
            row.append([c / (sx * sy) for c in acc])
        out.append(row)
    return out


def write_png(path, image):
    raw = bytearray()
    for row in image:
        raw.append(0)
        for r, g, b, a in row:
            # back from premultiplied alpha
            rgb = (r / a, g / a, b / a) if a > 0 else (0, 0, 0)
            raw += bytes(min(255, round(c * 255)) for c in (*rgb, a))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    height, width = len(image), len(image[0])
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with zipfile.ZipFile(sys.argv[1]) as archive:
        art = crop(decode_sprite(archive))
    scale = ART_SIZE / max(len(art), len(art[0]))
    width, height = round(len(art[0]) * scale), round(len(art) * scale)
    art = resize(art, width, height)

    icon = [[(0.0, 0.0, 0.0, 0.0)] * ICON_SIZE for _ in range(ICON_SIZE)]
    left, top = (ICON_SIZE - width) // 2, (ICON_SIZE - height) // 2
    for y in range(height):
        icon[top + y] = icon[top + y][:left] + art[y] + icon[top + y][left + width :]
    write_png(sys.argv[2], icon)


if __name__ == "__main__":
    main()
