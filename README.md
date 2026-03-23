# 🕯️ Ember High Contrast theme for vscode

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/danielhdzzz.ember-high-contrast?label=VS%20Code%20Marketplace)](https://marketplace.visualstudio.com/items?itemName=danielhdzzz.ember-high-contrast)
[![Open VSX](https://img.shields.io/open-vsx/v/danielhdzzz/ember-high-contrast?label=Open%20VSX)](https://open-vsx.org/extension/danielhdzzz/ember-high-contrast)

A dark, high-contrast color theme for VS Code with 8 accent color variants: blue, gray, green, orange, purple, red, white, and yellow. Based on [74th/vscode-monokaicharcoal](https://github.com/74th/vscode-monokaicharcoal) with revised colors, themed scrollbars, chat, warning/git colors and find match colors.

![screenshot](./screenshots/screenshot-orange.png)

## Colors

### Blue

![blue(default)](./screenshots/screenshot-blue.png)

### Gray

![gray](./screenshots/screenshot-gray.png)

### Green

![green](./screenshots/screenshot-green.png)

### Orange

![orange](./screenshots/screenshot-orange.png)

### Purple

![purple](./screenshots/screenshot-purple.png)

### Red

![red](./screenshots/screenshot-red.png)

### White

![white](./screenshots/screenshot-white.png)

### Yellow

![yellow](./screenshots/screenshot-yellow.png)

## Install

Search for **Ember High Contrast** in the VS Code Extensions Marketplace, or install from the command line:

```bash
code --install-extension danielhdzzz.ember-high-contrast
```

### Install from .vsix

You can also package and install the theme manually:

```bash
npm install -g @vscode/vsce
vsce package
code --install-extension ember-high-contrast-<version>.vsix
```

For VSCodium:

```bash
codium --install-extension ember-high-contrast-<version>.vsix
```

## Development

1. Open this folder in VS Code and press **F5** — a second window opens with the theme loaded live.
2. Edit `generate_themes.py` (palette, token colors, color template) and regenerate:
   ```bash
   python3 generate_themes.py
   ```
3. The dev host picks up color changes automatically. If it doesn't, run **Developer: Reload Window** (`Cmd+Shift+P`).

No packaging or installing needed — just edit and see. Do not edit the theme JSON files by hand.
