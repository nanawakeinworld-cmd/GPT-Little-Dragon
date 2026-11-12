# Screenshots

Real captures — no mock-ups.

Environment: **macOS 27.2 (Apple Silicon)**, **MaCursor 2.8.0**. The theme was imported
from this repository's `Cursor/GPT-Little-Dragon-v16.cursor` and applied before capturing.

| File | What it shows |
|---|---|
| `finder-arrow.png` | The purple dragon arrow over a Finder window showing this project's `Preview/` folder |
| `textedit-ibeam.png` | The dragon-with-laptop I-beam over text in TextEdit |
| `dock-arrow.png` | The arrow over the Dock |

## How they were captured

```bash
screencapture -x -C -R <x>,<y>,<w>,<h> <file>.png
```

`-C` includes the **real system cursor** — nothing was composited or drawn on afterwards.
The TextEdit content is demo text written for this test; the Finder window shows only
public project files. No personal information is included.

## Note on naming

MaCursor normalizes themes on import and appends a suffix when a theme with the same name
already exists. During this test the library entry was named `GPT 小龙 v16-3`; the visuals
are those of this repository's theme file, but the MaCursor copy is re-encoded internally.
