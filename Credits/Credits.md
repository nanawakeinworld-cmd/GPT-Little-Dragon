# Credits & provenance

This file records where every asset came from, what is confirmed, and what is
still unconfirmed. It is deliberately conservative: if a right cannot be
verified, the asset is marked **待确认 / unconfirmed** instead of being assumed
to be freely redistributable.

## At a glance

| Asset | Location | Origin | Rights status |
|---|---|---|---|
| Character sheet (1536×1024) | `Cursor/Source/原始拼图-1536x1024.png` | Provided by the project author; AI-assisted generation | ⚠️ Unconfirmed — see below |
| Cropped poses A–N | `Cursor/Source/raw-crops/` | Derived from the character sheet | ⚠️ Follows the sheet |
| Animated GIFs (3) | `Cursor/Source/animated-gifs/` | Provided by the project author; AI-assisted generation | ⚠️ Unconfirmed — see below |
| Static renders | `Cursor/Static/` | Rendered from A–N by `render_previews.py` | ⚠️ Follows the sheet |
| Packaged theme | `Cursor/GPT-Little-Dragon-v16.cursor` | Built from the above | ⚠️ Follows the artwork |
| Poster, overview, montage | `Preview/` | Generated for this repository | ✅ CC BY-NC-SA 4.0 |
| Build / preview scripts | `Cursor/Source/*.py` | Author + AI assistance | ✅ MIT |
| MaCursor | Not bundled | Writronic, GPL-3.0 | ✅ External dependency |
| Mousecape | Not bundled | Alex Zielenski | ✅ External reference |

## Character artwork

**What is known**

- The artwork was supplied by the project author as a single 1536×1024 sheet
  containing 25 visible components, which the build script groups into 14
  poses (A–N).
- The visual style is consistent with AI-generated anime/chibi illustration.
- The author states the character is an original fan design, not an official
  OpenAI mascot.

**Disclosure**

The author did not keep a record of the exact tool(s), model version(s), dates
or prompts. This repository discloses that gap instead of guessing:

- the artwork is treated as **AI-assisted**;
- the licence claims only the rights the author can reasonably grant;
- no commercial clearance is claimed;
- if the records are recovered later, they should be added here.

**Why this matters**

Copyright in AI-generated images is unsettled in many jurisdictions. The
project can only license what the author actually owns. The artwork is
therefore offered as **source-available for non-commercial fan use**, not as a
cleanly cleared commercial asset.

## OpenAI marks

The OpenAI knot logo appears on:

- the character's hair clip,
- the laptop lid,
- the plush toy,
- the main arrow,
- the move cursor,
- the hourglass/busy icon.

These are **fan references**, not licensed assets. "GPT", "OpenAI" and the knot
logo are trademarks of OpenAI. This project:

- does **not** claim affiliation with, endorsement by, or sponsorship from OpenAI;
- does **not** grant any trademark rights;
- will rename or remove the marks if OpenAI requests it.

Because the marks are embedded in the artwork, even non-commercial
redistribution carries some trademark risk. Do not sell the theme and do not
market it as an official OpenAI product.

## Code

| File | Purpose | Licence |
|---|---|---|
| `Cursor/Source/build_theme.py` | Original v16 theme builder (archived as-is) | MIT |
| `Cursor/Source/render_previews.py` | Static renders, poster, contact sheet, montage | MIT |

Both scripts were written with AI assistance and reviewed by the author.

> **Known limitation:** `build_theme.py` still points at the original working
> paths (`../incoming/2234*.png`, `../incoming/*.gif`, `assets/v16/`). It is kept
> for transparency. It needs a prepared `Cursor/incoming/` folder to run;
> see `Cursor/Source/README.md` for the tested rebuild steps.

## Third-party tools

- **[MaCursor](https://github.com/writronic/MaCursor)** — the cursor manager
  that imports and applies the `.cursor` theme. GPL-3.0, not bundled here.
- **[Mousecape](https://github.com/alexzielenski/Mousecape)** — prior art for
  macOS cursor theming. Not bundled; see its upstream licence.
- **Python 3 / Pillow / NumPy** — used to build and render previews. Not
  bundled; see their respective licences.
- **Apple system fonts** — used only to render preview images. No font files
  are redistributed.

## Fonts

No third-party font files are included in this repository. The poster and
contact sheet were rendered with macOS system fonts (Avenir Next, Hiragino Sans
GB), which are not redistributed.

## How to report a rights issue

Open an issue in the repository with:

- the asset path,
- the right you believe is affected,
- the action you want (credit change, replacement, removal).

Claims will be reviewed in good faith. If a valid concern is confirmed, the
asset will be replaced or removed in the next revision.
