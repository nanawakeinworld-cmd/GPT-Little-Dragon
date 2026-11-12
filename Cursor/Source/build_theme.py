#!/usr/bin/env python3
"""v16：新素材（真透明）→ 主指针缩小 / 静态小龙放大 / 紫箭头加大"""
import numpy as np, io, os, glob, uuid, plistlib
from PIL import Image, ImageDraw, ImageFilter
from collections import deque

OUT = "dist16"; os.makedirs(OUT, exist_ok=True)
SRC = sorted(glob.glob("../incoming/2234*.png"))[-1]

# 尺寸（每类指针可不同）
P_ARROW = 50      # 主指针（明显放大）
P_CHAR  = 92      # 静态小龙（更大）
P_ANIM  = 80      # 动画指针
CHAR    = 0.88    # 角色占画布
ASIZE   = 0.26    # 紫箭头占比（原来 0.34）
AMARGIN = 0.014
FRAME_MS = 200

# 组件编号 → 素材分组（按上面坐标人工核对）
GROUPS = {
 "A": [1], "B": [2,3,4], "C": [5,6], "D": [7,8,9],
 "E": [13,14], "F": [10,15], "G": [11,16], "H": [12,17],
 "I": [18,19], "J": [20,21], "K": [22], "L": [23], "M": [24], "N": [25],
}

# 光标 ID → (素材, 尺寸)
STATIC = {
 "com.apple.coregraphics.Arrow": ("M", P_ARROW),   # 三角箭头 = 主指针（小）
 "com.apple.coregraphics.IBeam": ("F", P_CHAR),    # 笔记本 → 文本
 "com.apple.coregraphics.Move":  ("N", P_CHAR),    # logo → 四向移动
 "com.apple.cursor.40":          ("G", P_CHAR),    # ? → 帮助
 "com.apple.cursor.3":           ("B", P_CHAR),    # ! → 禁止
 "com.apple.cursor.25":          ("C", P_CHAR),    # 抱玩偶 → 禁止X
 "com.apple.cursor.32":          ("D", P_CHAR),    # zzz → 垂直调整
 "com.apple.cursor.28":          ("E", P_CHAR),    # 趴睡 → 水平调整
 "com.apple.cursor.2":           ("K", P_CHAR),    # 生气 → 拖拽拷贝
 "com.apple.cursor.5":           ("J", P_CHAR),    # 爱心 → 拖拽添加
 "com.apple.cursor.13":          ("I", P_CHAR),    # 惊讶大 → 链接
 "com.apple.cursor.38":          ("A", P_CHAR),    # 坐姿 → 向左调整
 "com.apple.cursor.19":          ("H", P_CHAR),    # 不爽 → 四向移动变体
 "com.apple.cursor.17":          ("L", P_CHAR),    # 瞌睡 → 水平调整变体
}

ANIM = {
 "com.apple.cursor.4":          (2, [0,1,2,3,6,7,8,12]),
 "com.apple.coregraphics.Wait": (1, [0,1,5,6,7,9,10]),
}


def components(path):
    im = Image.open(path).convert("RGBA")
    fg = np.array(im)[..., 3] > 10
    H, W = fg.shape
    lab = np.zeros((H, W), np.int32); comps = []; cur = 0
    for y in range(H):
        for x in range(W):
            if fg[y, x] and lab[y, x] == 0:
                cur += 1; q = deque([(y, x)]); lab[y, x] = cur
                x0 = x1 = x; y0 = y1 = y; n = 0
                while q:
                    cy, cx = q.popleft(); n += 1
                    x0 = min(x0, cx); x1 = max(x1, cx); y0 = min(y0, cy); y1 = max(y1, cy)
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and fg[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; q.append((ny, nx))
                if n >= 400:
                    comps.append([x0, y0, x1+1, y1+1])
    comps.sort(key=lambda c: (c[1]//200, c[0]))
    return im, {i+1: b for i, b in enumerate(comps)}


def crop_group(im, boxes, keys, pad=12):
    bs = [boxes[k] for k in keys]
    x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs)
    x1 = max(b[2] for b in bs); y1 = max(b[3] for b in bs)
    return im.crop((max(0,x0-pad), max(0,y0-pad), min(im.width,x1+pad), min(im.height,y1+pad)))


def place(f, size, fill, hs=None):
    sc = size * fill / max(f.size)
    w, h = max(1, round(f.width*sc)), max(1, round(f.height*sc))
    a = np.asarray(f, dtype=np.float32)/255.0; al = a[...,3:4]
    pm = np.concatenate([a[...,:3]*al, al], -1)
    small = np.asarray(Image.fromarray((pm*255).round().astype(np.uint8),"RGBA")
                       .resize((w,h), Image.LANCZOS), dtype=np.float32)/255.0
    sa = small[...,3:4]; rgb = np.divide(small[...,:3], np.where(sa==0,1.0,sa))
    img = Image.fromarray((np.concatenate([np.clip(rgb,0,1), sa], -1)*255).round().astype(np.uint8),"RGBA")
    c = Image.new("RGBA",(size,size),(0,0,0,0)); ox, oy = (size-w)//2, (size-h)//2
    c.paste(img,(ox,oy),img)
    return c, ox, oy, w, h


_ARROW = {}
def arrow(px):
    if px not in _ARROW:
        A=512; im=Image.new("RGBA",(A,A),(0,0,0,0))
        pts=[(14,12),(14,196),(58,152),(86,232),(122,214),(96,140),(146,140)]
        s=A/256
        ImageDraw.Draw(im).polygon([(x*s,y*s) for x,y in pts], fill=(140,110,200,255),
                                   outline=(58,38,98,255), width=int(10*s))
        _ARROW[px]=im.resize((px,px), Image.LANCZOS)
    return _ARROW[px]


def entry(frames, pt, duration, pointer=False):
    hs=None; sheets=[]
    for i in (0,1):
        size = pt*2**i
        sh=Image.new("RGBA",(size,size*len(frames)),(0,0,0,0))
        for k,f in enumerate(frames):
            c,ox,oy,w,h = place(f,size,CHAR)
            if pointer:
                tip=(ox+w*0.02, oy+h*0.02)
            else:
                a=arrow(int(size*ASIZE)); m=int(size*AMARGIN)
                c.alpha_composite(a,(m,m)); tip=(m+a.width*0.0547, m+a.height*0.0469)
            if i==0: hs=(round(tip[0],2), round(tip[1],2))
            sh.paste(c,(0,k*size))
        sheets.append(sh)
    def png(im):
        b=io.BytesIO(); im.save(b,"PNG",optimize=True); return b.getvalue()
    return {"FrameCount":len(frames), "FrameDuration":duration,
            "HotSpotX":hs[0], "HotSpotY":hs[1],
            "PointsWide":float(pt), "PointsHigh":float(pt),
            "Representations":[png(sheets[0]), png(sheets[1])]}, hs


def main():
    im, boxes = components(SRC)
    os.makedirs("assets/v16", exist_ok=True)
    mats = {}
    for k, keys in GROUPS.items():
        c = crop_group(im, boxes, keys)
        c.save(f"assets/v16/{k}.png"); mats[k]=c
    print(f"抠出素材 {len(mats)} 个")

    cursors = {}
    for cid,(key,pt) in STATIC.items():
        e,_ = entry([mats[key]], pt, 1.0, pointer=(cid=="com.apple.coregraphics.Arrow"))
        cursors[cid]=e

    gifs=sorted(glob.glob("../incoming/*.gif"))
    for cid,(gi,idxs) in ANIM.items():
        g=Image.open(gifs[gi]); fr=[]
        for i in range(g.n_frames):
            g.seek(i); fr.append(g.convert("RGBA"))
        e,_=entry([fr[i] for i in idxs], P_ANIM, FRAME_MS/1000.0)
        cursors[cid]=e

    theme={"Creator":"GPT 小龙 cursor set","Cursors":cursors,"HiDPI":True,
           "Identifier":"gpt-little-dragon-v16","ThemeName":"GPT 小龙 v16",
           "ThemeVersion":"11.0","UUID":str(uuid.uuid4()).upper()}
    p=f"{OUT}/GPT小龙v16.cursor"
    plistlib.dump(theme, open(p,"wb"), fmt=plistlib.FMT_XML, sort_keys=False)
    print(f"生成 {p}  {os.path.getsize(p)/1024:.0f}KB  共 {len(cursors)} 个")


if __name__ == "__main__":
    main()
