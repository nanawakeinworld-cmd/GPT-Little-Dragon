# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Repository scaffold: `Preview/`, `Cursor/`, `Installation/`, `Credits/`.
- Real macOS screenshots: Finder arrow, TextEdit I-beam, Dock arrow.
- Bilingual README (English / 简体中文).
- Dual-licence draft: MIT for code, CC BY-NC-SA 4.0 for artwork.
- Install, uninstall and troubleshooting guides.
- Credits and provenance record.

### Changed
- Reorganised the original working folder into a publishable structure without
  modifying the source assets.
- Regenerated the theme UUID and set `ThemeVersion` to `16.0`, so MaCursor treats
  this build as a distinct theme instead of colliding with an older import.
  The pre-normalisation file is preserved at
  `Cursor/Source/GPT-Little-Dragon-v16-original.cursor`.

### Known issues
- The Idle animation (`01_普通待机_小龙.gif`) is source-only by design: macOS has
  no idle cursor role that animates while the pointer rests. It is kept as a
  preview / future asset.
- Tested on macOS 27.2 (arm64) with MaCursor 2.8.0: the theme imports, applies, and all
  16 cursors render. A clean-install and macOS 13/14/15 test are still pending.
- `Cursor/Source/build_theme.py` still references the original external
  `../incoming/` and `assets/v16/` paths; it can be re-run with a prepared
  `Cursor/incoming/` folder, but a fresh build is not fully identical.
- Rebuild test: the 14 static cursors are byte-identical, but the two animated
  cursors come out slightly smaller than in the shipped `v16` file. The source
  GIFs are likely a different revision. See `Cursor/Source/README.md`.

## [v16] - 2026-11-12

### Added
- 16-cursor MaCursor theme: 1 main arrow, 13 static character cursors,
  2 animated cursors.
- HiDPI (1× / 2×) representations for every cursor.
- Purple click indicator on all character cursors.
- Source crops A–N, the original 1536×1024 character sheet, and the three
  source GIFs.

### Notes
- Theme identifier: `gpt-little-dragon-v16`.
- Theme display name: `GPT 小龙 v16`.
- `ThemeVersion` was `11.0` when first packaged; it is now normalised to `16.0`
  and the UUID was regenerated (2026-11-13). The original file is kept at
  `Cursor/Source/GPT-Little-Dragon-v16-original.cursor`.
- Structural validation passed: 16 cursors, 32 image representations, correct
  frame-sheet dimensions, hotspots inside bounds, alpha channel present.
