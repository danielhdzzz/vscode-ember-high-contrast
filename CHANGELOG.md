# Changelog

All notable changes to Ember High Contrast are documented in this file.

## [0.6.1] - 2026-03-23

### Changed

- Input background now uses a faint accent tint instead of pure black — gives chat user messages a distinct background

## [0.6.0] - 2026-03-23

### Added

- Chat panel colors: user message bubble background/hover, code borders, slash command styling, avatars, edited file foreground, added/removed line pills, checkpoint separator, thinking shimmer
- Inline chat colors: background, foreground, border, input focus/placeholder, diff inserted/removed
- Inline code (`textPreformat.foreground`) themed to accent color

## [0.5.0] - 2026-03-21

### Changed

- Per-variant find match background opacity for better legibility on lighter accents
- Tweaked yellow accent hue

## [0.4.0] - 2026-03-21

### Added

- Theme generator script (`generate_themes.py`) that produces all 8 theme JSON files from a single source of truth
- Exhaustive named color palette (36 colors) — zero magic hex strings in the template

### Changed

- Unified formatting across all theme files (fixed inconsistent casing and whitespace)
- All alpha/opacity values use 0–255 integers instead of hex suffixes

## [0.2.2] - 2026-03-21

### Added

- Full git decoration colors: added, deleted, untracked, ignored, conflicting, renamed, staged modified, staged deleted, and submodule

## [0.2.1] - 2026-03-21

### Changed

- Icon now uses transparency instead of black background

## [0.2.0] - 2026-03-21

### Added

- Scrollbar colors matching each theme's accent color (shadow, background, hover, active states)

### Changed

- Updated readme and screenshots

## [0.1.0] - 2026-03-21

### Added

- Warning and modified file colors themed to each variant's accent color (`editorWarning`, `list.warningForeground`, `editorOverviewRuler.warningForeground`)
- Git modified resource foreground color

### Changed

- New generated conic gradient ring icon
- More transparent active selection background

## [0.0.9] - 2026-03-21

### Changed

- Refined search match colors: unified find match background with theme accent, added explicit foreground colors for better legibility
- Transparent find match border for a cleaner look
- Softer find match highlight background with full-white foreground

## [0.0.8] - 2026-03-20

### Added

- `.vscodeignore` to reduce published extension size

### Changed

- More visible list selection backgrounds (higher opacity for active/inactive states)

### Removed

- Unused `.tmTheme` and `.vim` theme files
- Upstream `tasks.py` build script

## [0.0.7] - 2025-01-07

### Changed

- Darker shade of orange across the orange theme (`#FD971F` → `#E96401`), affecting borders, line numbers, focus borders, and function parameters

## [0.0.6] - 2024-10-01

### Changed

- Restored purple selection background while keeping orange search highlights

## [0.0.5] - 2024-10-01

### Changed

- More visible search/selection: switched editor selection and find match colors to orange (`#ff5900`) across all themes

## [0.0.4] - 2024-09-13

### Added

- MIT License
- Extension icon
- Screenshots

### Changed

- Refined yellow theme colors

## [0.0.3] - 2024-09-13

### Changed

- Refined red and blue theme syntax colors
- Blue theme tweak

## [0.0.1] - 2024-09-05

### Added

- Forked from [Monokai Charcoal High Contrast](https://github.com/74th/vscode-monokaicharcoal) and renamed to **Ember High Contrast**
- 8 theme variants: orange (default), gray, purple, red, yellow, green, blue, white
- Overhauled syntax colors across all variants (reds, greens, blues, yellows, comments, selection)
- Orange set as the default theme

### Changed

- Updated `@vscode/vsce` dependency
- Fully reworked comment, selection, and accent colors for each variant
