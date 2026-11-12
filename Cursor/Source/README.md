# Source files

These are the original working files for the `v16` theme, kept for transparency.
Nothing here is required to install the theme.

| File | What it is |
|---|---|
| `原始拼图-1536x1024.png` | Original character sheet supplied by the author |
| `raw-crops/A.png` … `N.png` | 14 pose crops produced by `build_theme.py` |
| `animated-gifs/01_普通待机_小龙.gif` | Idle animation, 16 frames, 60 ms |
| `animated-gifs/02_忙碌等待_小龙.gif` | Busy / waiting animation, 16 frames, 60 ms |
| `animated-gifs/03_后台工作_小龙.gif` | Background-work animation, 16 frames, 60 ms |
| `build_theme.py` | Original theme builder (archived as-is) |
| `render_previews.py` | Generates `Cursor/Static/`, the poster, the contact sheet and the montage |

## About `build_theme.py`

The script is preserved **unmodified** from the original working folder. It expects:

```
../incoming/2234*.png    # the character sheet
../incoming/*.gif        # the three animations
assets/v16/              # output crops
```

Those paths do not exist in this repository, so the script needs a prepared
`incoming/` folder before it will run (see the rebuild test below). It is kept
as a record of how `v16` was built; a one-command reproducible build is still
on the roadmap.

`render_previews.py` **does** run from this repository and only reads
`raw-crops/`; it writes to `Cursor/Static/` and `Preview/`.

## Rebuild test — 2026-11-12

The archived script was re-run against the files in this folder to check whether
the build can be reproduced.

Environment: Python 3.12, Pillow 12.3.0, NumPy 2.3.5, macOS 27.2 (arm64).

```bash
cd Cursor/Source
mkdir -p ../incoming
cp 原始拼图-1536x1024.png ../incoming/2234-sheet.png
cp animated-gifs/*.gif ../incoming/
python3 build_theme.py
```

Result:

- 14 source crops extracted, 16 cursors written in ~1.2 s.
- **Static cursors:** all 14 are byte-for-byte identical to the shipped
  `Cursor/GPT-Little-Dragon-v16.cursor`.
- **Animated cursors:** both rebuild successfully, but the frames differ
  slightly from the shipped file. At 160 px, the shipped character bounding box
  is 139 px wide versus 135 px in the rebuild, and the alpha coverage differs by
  roughly 6 points. The poses and frame order match; the scale does not.

Interpretation: the static pipeline is reproducible. The GIFs in
`animated-gifs/` are probably **not the exact revision** used to build the
shipped `v16` file (or the animated fill/scale changed between builds). Until
that is reconciled, treat the shipped `.cursor` as the reference and do not
overwrite it with a fresh rebuild.

A future fix should either:

1. locate the exact GIF revision and record its hash, or
2. re-bake both animated cursors from the current GIFs and re-validate them,
   accepting a deliberate visual change.
