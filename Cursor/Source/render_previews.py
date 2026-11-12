#!/usr/bin/env python3
"""Generate preview renders from the v16 source crops (does not modify originals)."""
import os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "Cursor", "Source", "raw-crops")
STATIC_DIR = os.path.join(ROOT, "Cursor", "Static")
POSTER = os.path.join(ROOT, "Preview", "Poster", "poster.png")
SHEET = os.path.join(ROOT, "Preview", "Static-Overview.png")
DEMO = os.path.join(ROOT, "Preview", "Demo", "demo-montage.gif")

P_ARROW, P_CHAR = 50, 92
CHAR, ASIZE, AMARGIN = 0.88, 0.26, 0.014

STATIC = {
    "arrow":                    ("M", P_ARROW, True),
    "ibeam-laptop":             ("F", P_CHAR, False),
    "move-logo":                ("N", P_CHAR, False),
    "help-question":            ("G", P_CHAR, False),
    "not-allowed-bang":         ("B", P_CHAR, False),
    "not-allowed-plush":        ("C", P_CHAR, False),
    "resize-vertical-sleep":    ("D", P_CHAR, False),
    "resize-horizontal-prone":  ("E", P_CHAR, False),
    "drag-copy-angry":          ("K", P_CHAR, False),
    "drag-add-heart":           ("J", P_CHAR, False),
    "link-surprised":           ("I", P_CHAR, False),
    "resize-left-sitting":      ("A", P_CHAR, False),
    "move-annoyed":             ("H", P_CHAR, False),
    "resize-horizontal-sleepy": ("L", P_CHAR, False),
}

def place(f, size, fill):
    sc = size * fill / max(f.size)
    w, h = max(1, round(f.width * sc)), max(1, round(f.height * sc))
    a = np.asarray(f, dtype=np.float32) / 255.0
    al = a[..., 3:4]
    pm = np.concatenate([a[..., :3] * al, al], -1)
    small = np.asarray(Image.fromarray((pm * 255).round().astype(np.uint8), "RGBA")
                       .resize((w, h), Image.LANCZOS), dtype=np.float32) / 255.0
    sa = small[..., 3:4]
    rgb = np.divide(small[..., :3], np.where(sa == 0, 1.0, sa))
    img = Image.fromarray((np.concatenate([np.clip(rgb, 0, 1), sa], -1) * 255).round().astype(np.uint8), "RGBA")
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ox, oy = (size - w) // 2, (size - h) // 2
    c.paste(img, (ox, oy), img)
    return c, ox, oy, w, h

_ARROW = {}
def arrow(px):
    if px not in _ARROW:
        A = 512
        im = Image.new("RGBA", (A, A), (0, 0, 0, 0))
        pts = [(14, 12), (14, 196), (58, 152), (86, 232), (122, 214), (96, 140), (146, 140)]
        s = A / 256
        ImageDraw.Draw(im).polygon([(x * s, y * s) for x, y in pts], fill=(140, 110, 200, 255),
                                   outline=(58, 38, 98, 255), width=int(10 * s))
        _ARROW[px] = im.resize((px, px), Image.LANCZOS)
    return _ARROW[px]

def render(key, pt, pointer=False, scale=2):
    f = Image.open(os.path.join(SRC, key + ".png")).convert("RGBA")
    size = pt * scale
    c, ox, oy, w, h = place(f, size, CHAR)
    if not pointer:
        a = arrow(int(size * ASIZE))
        m = int(size * AMARGIN)
        c.alpha_composite(a, (m, m))
    return c

def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

AV = "/System/Library/Fonts/Avenir Next.ttc"
CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def generate_static():
    os.makedirs(STATIC_DIR, exist_ok=True)
    for name, (key, pt, ptr) in STATIC.items():
        img = render(key, pt, ptr)
        img.save(os.path.join(STATIC_DIR, name + ".png"))
    print("static:", len(STATIC))

def generate_sheet():
    cols, cell, pad = 7, 190, 14
    rows = 2
    W = cols * (cell + pad) + pad
    H = 150 + rows * (cell + 46) + pad
    bg = Image.new("RGB", (W, H), (20, 16, 33))
    d = ImageDraw.Draw(bg)
    d.text((pad + 4, 28), "GPT Little Dragon  ·  static cursor set", font=font(AV, 30, 0), fill=(236, 230, 255))
    d.text((pad + 4, 72), "14 static cursors · rendered from v16 materials at 2x", font=font(AV, 16, 5), fill=(150, 138, 185))
    names = list(STATIC)
    for i, name in enumerate(names):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad) + (cell - 184) // 2
        y = 130 + r * (cell + 46)
        tile = Image.new("RGBA", (cell, cell), (36, 28, 58, 255))
        img = Image.open(os.path.join(STATIC_DIR, name + ".png")).convert("RGBA")
        tile.alpha_composite(img, ((cell - img.width) // 2, (cell - img.height) // 2))
        bg.paste(tile, (x, y))
        label = name.replace("-", " ")
        f = font(AV, 11, 5)
        tw = d.textlength(label, font=f)
        d.text((x + (cell - tw) / 2, y + cell + 8), label, font=f, fill=(168, 158, 198))
    bg.save(SHEET)
    print("sheet:", SHEET)

def vertical_gradient(w, h, top, bottom):
    t = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - t) + np.array(bottom)[None, None, :] * t)
    return Image.fromarray(np.repeat(arr, w, axis=1).round().astype(np.uint8), "RGB")

def glow(size, color=(120, 80, 210), alpha=90):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size, size), fill=color + (alpha,))
    return im.filter(ImageFilter.GaussianBlur(size // 6))

def generate_poster():
    W, H = 1600, 1000
    bg = vertical_gradient(W, H, (18, 13, 32), (38, 26, 68)).convert("RGBA")
    bg.alpha_composite(glow(900, (110, 70, 200), 70), (830, 60))
    bg.alpha_composite(glow(500, (60, 200, 220), 28), (1050, 620))
    d = ImageDraw.Draw(bg)

    # top rule + label
    d.line((90, 105, 1510, 105), fill=(90, 72, 140, 180), width=1)
    d.text((92, 62), "UNOFFICIAL FAN PROJECT", font=font(AV, 15, 2), fill=(170, 150, 220))

    # title
    d.text((86, 168), "GPT", font=font(AV, 132, 0), fill=(245, 240, 255))
    d.text((86, 300), "Little Dragon", font=font(AV, 126, 0), fill=(178, 142, 245))
    d.text((92, 472), "A macOS cursor theme  ·  GPT 小龙", font=font(CJK, 34, 2), fill=(210, 200, 235))
    d.text((92, 520), "白发紫瞳的小恶魔龙，陪你在桌面打工。", font=font(CJK, 24, 0), fill=(150, 140, 185))

    # chips
    chips = ["16 cursors", "2 animations", "HiDPI", "MaCursor"]
    x = 92
    for c in chips:
        f = font(AV, 16, 2)
        tw = d.textlength(c, font=f)
        d.rounded_rectangle((x, 585, x + tw + 34, 623), radius=19, outline=(120, 98, 180), width=1)
        d.text((x + 17, 594), c, font=f, fill=(200, 188, 235))
        x += tw + 48

    # character
    ch = Image.open(os.path.join(SRC, "A.png")).convert("RGBA")
    scale = 520 / ch.height
    ch = ch.resize((round(ch.width * scale), 520), Image.LANCZOS)
    bg.alpha_composite(ch, (1240 - ch.width // 2, 300))

    # palette
    pal = [(245, 242, 255), (196, 168, 250), (140, 110, 200), (86, 58, 138), (42, 28, 64), (108, 220, 226)]
    for i, col in enumerate(pal):
        d.ellipse((92 + i * 56, 700, 92 + i * 56 + 36, 736), fill=col + (255,), outline=(255, 255, 255, 40))

    d.text((92, 800), "Free to use  ·  Credit required  ·  No commercial use", font=font(AV, 17, 5), fill=(160, 150, 195))
    d.text((92, 900), "Not affiliated with, endorsed by, or sponsored by OpenAI.", font=font(AV, 14, 2), fill=(120, 110, 150))
    d.text((92, 924), "GPT / OpenAI marks are trademarks of their respective owners.", font=font(AV, 14, 2), fill=(120, 110, 150))
    bg.convert("RGB").save(POSTER, quality=95)
    print("poster:", POSTER)

def generate_montage():
    files = [("idle.gif", "IDLE"), ("waiting.gif", "WAITING"), ("working.gif", "WORKING")]
    cell, gap, top = 176, 22, 52
    W = gap + 3 * (cell + gap)
    H = top + cell + gap
    frames = []
    gifs = [Image.open(os.path.join(ROOT, "Preview", "Demo", n)) for n, _ in files]
    n = min(g.n_frames for g in gifs)
    for i in range(n):
        canvas = Image.new("RGB", (W, H), (18, 13, 32))
        d = ImageDraw.Draw(canvas)
        for j, ((name, label), g) in enumerate(zip(files, gifs)):
            g.seek(i)
            fr = g.convert("RGBA").resize((cell, cell), Image.LANCZOS)
            x = gap + j * (cell + gap)
            tile = Image.new("RGBA", (cell, cell), (32, 24, 52, 255))
            tile.alpha_composite(fr, (0, 0))
            canvas.paste(tile, (x, top))
            f = font(AV, 13, 2)
            tw = d.textlength(label, font=f)
            d.text((x + (cell - tw) / 2, 22), label, font=f, fill=(186, 168, 232))
        frames.append(canvas)
    frames[0].save(DEMO, save_all=True, append_images=frames[1:], duration=60, loop=0, optimize=True)
    print("montage:", DEMO)


def generate_social():
    W, H = 1280, 640
    bg = vertical_gradient(W, H, (17, 12, 30), (40, 27, 72)).convert("RGBA")
    bg.alpha_composite(glow(640, (110, 70, 200), 80), (740, -120))
    bg.alpha_composite(glow(360, (60, 200, 220), 26), (980, 470))
    d = ImageDraw.Draw(bg)

    d.text((64, 56), "UNOFFICIAL FAN PROJECT", font=font(AV, 13, 2), fill=(170, 150, 220))
    d.text((60, 96), "GPT Little Dragon", font=font(AV, 72, 0), fill=(245, 240, 255))
    d.text((64, 196), "A macOS cursor theme  ·  GPT 小龙", font=font(CJK, 24, 2), fill=(200, 186, 235))
    d.text((64, 240), "16 cursors · 2 animations · HiDPI", font=font(AV, 17, 5), fill=(158, 146, 196))

    for i, col in enumerate([(245, 242, 255), (196, 168, 250), (140, 110, 200), (86, 58, 138), (108, 220, 226)]):
        d.ellipse((64 + i * 44, 304, 64 + i * 44 + 26, 330), fill=col + (255,))

    d.text((64, 520), "Not affiliated with, endorsed by, or sponsored by OpenAI.", font=font(AV, 13, 2), fill=(122, 112, 152))
    d.text((64, 542), "GPT / OpenAI marks are trademarks of their respective owners.", font=font(AV, 13, 2), fill=(122, 112, 152))

    ch = Image.open(os.path.join(SRC, "A.png")).convert("RGBA")
    scale = 440 / ch.height
    ch = ch.resize((round(ch.width * scale), 440), Image.LANCZOS)
    bg.alpha_composite(ch, (1272 - ch.width, 130))
    bg.convert("RGB").save(os.path.join(ROOT, "Preview", "Poster", "social-preview.png"), quality=95)
    print("social:", os.path.join(ROOT, "Preview", "Poster", "social-preview.png"))


def generate_red():
    W, H = 1080, 1350
    bg = vertical_gradient(W, H, (17, 12, 30), (44, 29, 78)).convert("RGBA")
    bg.alpha_composite(glow(820, (110, 70, 200), 70), (130, 60))
    bg.alpha_composite(glow(420, (60, 200, 220), 22), (700, 980))
    d = ImageDraw.Draw(bg)

    d.text((70, 62), "UNOFFICIAL FAN PROJECT  ·  GPT 小龙", font=font(CJK, 18, 2), fill=(176, 158, 220))
    d.line((70, 100, 1010, 100), fill=(90, 72, 140, 160), width=1)

    ch = Image.open(os.path.join(SRC, "A.png")).convert("RGBA")
    scale = 640 / ch.height
    ch = ch.resize((round(ch.width * scale), 640), Image.LANCZOS)
    bg.alpha_composite(ch, ((W - ch.width) // 2, 150))

    d.text((70, 830), "GPT Little Dragon", font=font(AV, 66, 0), fill=(245, 240, 255))
    d.text((74, 920), "GPT 小龙 · macOS 鼠标指针主题", font=font(CJK, 30, 2), fill=(196, 172, 248))
    d.text((74, 975), "白发紫瞳的小恶魔龙，陪你在桌面打工。", font=font(CJK, 23, 0), fill=(160, 148, 195))

    chips = ["16 个指针", "2 段动画", "HiDPI", "MaCursor"]
    x = 74
    for c in chips:
        f = font(CJK, 19, 2)
        tw = d.textlength(c, font=f)
        d.rounded_rectangle((x, 1048, x + tw + 36, 1092), radius=22, outline=(122, 100, 182), width=1)
        d.text((x + 18, 1060), c, font=f, fill=(206, 192, 240))
        x += tw + 50

    d.text((74, 1210), "免费分享 · 非商业 · 转载请注明", font=font(CJK, 17, 0), fill=(150, 138, 185))
    d.text((74, 1250), "Not affiliated with or endorsed by OpenAI.", font=font(AV, 15, 2), fill=(118, 108, 148))
    bg.convert("RGB").save(os.path.join(ROOT, "Preview", "Poster", "xiaohongshu-4x5.png"), quality=95)
    print("red:", os.path.join(ROOT, "Preview", "Poster", "xiaohongshu-4x5.png"))

if __name__ == "__main__":
    generate_static()
    generate_sheet()
    generate_poster()
    generate_social()
    generate_red()
    generate_montage()
