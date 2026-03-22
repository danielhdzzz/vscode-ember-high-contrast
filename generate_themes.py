#!/usr/bin/env python3
"""Generate all 8 Ember High Contrast theme JSON files from a single source of truth."""

import json
import os

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

PALETTE = {
    "orange": "#E96401",
    "red":    "#F43F1A",
    "yellow": "#F9C449",
    "green":  "#19FC8E",
    "blue":   "#02B5FC",
    "purple": "#AE81FF",
    "white":  "#f1f1f1",
    "gray":   "#8f8f8f",
    "black":  "#000000",
    "cyan":   "#43B9D8",
}


def c(expr):
    """Resolve a ``"color"`` or ``"color/opacity"`` expression.

    Examples
    --------
    >>> c("red")
    '#F43F1A'
    >>> c("red/25")
    '#F43F1A40'
    """
    if "/" in expr:
        name, opacity_str = expr.split("/", 1)
        hex_color = PALETTE[name]
        opacity = int(opacity_str)
        # Convert 0-100 percentage to 0-255 byte, then to two-char hex.
        byte = round(opacity * 255 / 100)
        return f"{hex_color}{byte:02X}"
    return PALETTE[expr]


# ---------------------------------------------------------------------------
# Token colors (shared across all variants)
# ---------------------------------------------------------------------------

TOKEN_COLORS = [
    {
        "settings": {
            "foreground": "#FFFFFF",
            "background": "#000c18",
            "caret": "#F8F8F0",
            "invisibles": "#3B3A32",
            "lineHighlight": "#2c120b",
            "selection": "#2c120b",
            "findHighlight": "#FFE792",
            "findHighlightForeground": "#000000",
            "selectionBorder": "#222218",
            "activeGuide": "#9D550FB0",
            "bracketsForeground": "#F8F8F2A5",
            "bracketsOptions": "underline",
            "bracketContentsForeground": "#F8F8F2A5",
            "bracketContentsOptions": "underline",
            "tagsOptions": "stippled_underline",
        }
    },
    {
        "name": "Comment",
        "scope": ["comment"],
        "settings": {"foreground": "#787878"},
    },
    {
        "name": "String",
        "scope": "string",
        "settings": {"foreground": c("yellow")},
    },
    {
        "name": "Number",
        "scope": "constant.numeric",
        "settings": {"foreground": c("purple")},
    },
    {
        "name": "Built-in constant",
        "scope": "constant.language",
        "settings": {"foreground": c("purple")},
    },
    {
        "name": "User-defined constant",
        "scope": ["constant.character", "constant.other"],
        "settings": {"foreground": c("purple")},
    },
    {
        "name": "Variable",
        "scope": "variable",
        "settings": {"fontStyle": ""},
    },
    {
        "name": "Keyword",
        "scope": "keyword",
        "settings": {"fontStyle": "bold", "foreground": c("red")},
    },
    {
        "name": "Storage",
        "scope": "storage",
        "settings": {"fontStyle": "bold", "foreground": c("red")},
    },
    {
        "name": "Storage type",
        "scope": "storage.type",
        "settings": {"fontStyle": "italic", "foreground": c("blue")},
    },
    {
        "name": "Class name",
        "scope": "entity.name.class",
        "settings": {"fontStyle": "underline", "foreground": c("green")},
    },
    {
        "name": "Inherited class",
        "scope": "entity.other.inherited-class",
        "settings": {"fontStyle": "italic underline", "foreground": c("green")},
    },
    {
        "name": "Function name",
        "scope": "entity.name.function",
        "settings": {"fontStyle": "", "foreground": c("green")},
    },
    {
        "name": "Function argument",
        "scope": "variable.parameter",
        "settings": {"fontStyle": "italic", "foreground": c("orange")},
    },
    {
        "name": "Tag name",
        "scope": "entity.name.tag",
        "settings": {"fontStyle": "bold", "foreground": c("red")},
    },
    {
        "name": "Tag attribute",
        "scope": "entity.other.attribute-name",
        "settings": {"fontStyle": "", "foreground": c("green")},
    },
    {
        "name": "Library function",
        "scope": "support.function",
        "settings": {"fontStyle": "", "foreground": c("blue")},
    },
    {
        "name": "Library constant",
        "scope": "support.constant",
        "settings": {"fontStyle": "", "foreground": c("blue")},
    },
    {
        "name": "Library class/type",
        "scope": ["support.type", "support.class"],
        "settings": {"fontStyle": "italic", "foreground": c("blue")},
    },
    {
        "name": "Library variable",
        "scope": "support.other.variable",
        "settings": {"fontStyle": ""},
    },
    {
        "name": "Invalid",
        "scope": "invalid",
        "settings": {
            "background": c("red"),
            "fontStyle": "bold",
            "foreground": "#F8F8F0",
        },
    },
    {
        "name": "Invalid deprecated",
        "scope": "invalid.deprecated",
        "settings": {"background": c("purple"), "foreground": "#F8F8F0"},
    },
    {
        "name": "JSON String",
        "scope": ["meta.structure.dictionary.json", "string.quoted.double.json"],
        "settings": {"foreground": "#CFCFC2"},
    },
    {
        "name": "diff.header",
        "scope": "meta.diff, meta.diff.header",
        "settings": {"foreground": "#75715E"},
    },
    {
        "name": "diff.deleted",
        "scope": "markup.deleted",
        "settings": {"background": c("red"), "foreground": c("red")},
    },
    {
        "name": "diff.inserted",
        "scope": "markup.inserted",
        "settings": {"foreground": c("green")},
    },
    {
        "name": "diff.changed",
        "scope": "markup.changed",
        "settings": {"foreground": c("yellow")},
    },
    {
        "scope": "constant.numeric.line-number.find-in-files - match",
        "settings": {"foreground": "#AE81FFA0"},
    },
    {
        "scope": "entity.name.filename.find-in-files",
        "settings": {"foreground": c("yellow")},
    },
    {
        "name": "Language methods",
        "scope": ["variable.language"],
        "settings": {"foreground": c("green")},
    },
    {
        "scope": "heading.1.markdown",
        "settings": {"foreground": c("green"), "fontStyle": "bold"},
    },
    {
        "scope": "punctuation.definition.heading.markdown",
        "settings": {"foreground": c("green")},
    },
    {
        "scope": "entity.name.section.markdown",
        "settings": {"foreground": c("green")},
    },
    {
        "scope": "punctuation.definition.list.begin.markdown",
        "settings": {"foreground": c("purple")},
    },
    {
        "scope": "meta.image.inline.markdown",
        "settings": {"foreground": c("yellow")},
    },
    {
        "scope": "markup.bold.markdown",
        "settings": {"foreground": "#FFFFFF", "fontStyle": "bold"},
    },
    {
        "scope": "markup.italic.markdown",
        "settings": {"foreground": "#FFFFFF", "fontStyle": "italic"},
    },
    {
        "scope": "markup.inline.raw.string.markdown",
        "settings": {"foreground": c("blue")},
    },
    {
        "scope": "meta.separator.markdown",
        "settings": {"foreground": c("gray")},
    },
    {
        "scope": [
            "punctuation.definition.template-expression.begin",
            "punctuation.definition.template-expression.end",
        ],
        "settings": {"foreground": c("purple")},
    },
    {
        "scope": [
            "variable.other.object",
            "punctuation.accessor",
            "meta.brace.round",
            "variable.other.readwrite",
            "punctuation.separator.comma",
        ],
        "settings": {"foreground": "#FFFFFF"},
    },
]


# ---------------------------------------------------------------------------
# Per-variant overrides
# ---------------------------------------------------------------------------

# editorSuggestWidget.highlightForeground and editorHint.foreground
HIGHLIGHT_MAP = {
    "orange": c("yellow"),     # #F9C449
    "red":    c("yellow"),     # #F9C449
    "yellow": c("orange"),     # #E96401
    "green":  c("cyan"),       # #43B9D8
    "blue":   c("orange"),     # #E96401
    "purple": c("cyan"),       # #43B9D8
    "white":  c("cyan"),       # #43B9D8
    "gray":   c("cyan"),       # #43B9D8
}

# statusBar.debuggingBackground — blue uses its own accent, others use cyan.
# The "15" suffix is a hand-chosen hex alpha, not a computed percentage.
DEBUG_BG_MAP = {
    "orange": "#43B9D815",
    "red":    "#43B9D815",
    "yellow": "#43B9D815",
    "green":  "#43B9D815",
    "blue":   "#02B5FC15",
    "purple": "#43B9D815",
    "white":  "#43B9D815",
    "gray":   "#43B9D815",
}

# list.activeSelectionBackground — per-variant exact values
LIST_ACTIVE_MAP = {
    "orange": "#E96401CC",
    "red":    "#F43F1ACC",
    "yellow": "#f9c4499a",
    "green":  "#19fc8e9c",
    "blue":   "#02B5FCCC",
    "purple": "#AE81FFCC",
    "white":  "#f1f1f17c",
    "gray":   "#8f8f8fCC",
}

# list.inactiveSelectionBackground — per-variant exact values
LIST_INACTIVE_MAP = {
    "orange": "#E9640160",
    "red":    "#F43F1A60",
    "yellow": "#f9c44953",
    "green":  "#19FC8E60",
    "blue":   "#02B5FC60",
    "purple": "#AE81FF60",
    "white":  "#f1f1f14f",
    "gray":   "#8f8f8f60",
}


def build_colors(accent):
    """Build the ``colors`` dict for a given accent name."""
    a = PALETTE[accent]  # accent color, e.g. "#E96401"

    # Helper for accent + alpha suffix
    def aa(alpha_hex):
        return f"{a}{alpha_hex}"

    return {
        "foreground": "#FFFFFF",
        "icon.foreground": "#ffffff",
        "contrastBorder": aa("75"),
        "contrastActiveBorder": "#00000000",
        "focusBorder": aa("75"),
        "editor.foreground": "#FFFFFF",
        "editor.background": "#000000",
        "editor.inactiveSelectionBackground": "#3924bea4",
        "editor.findMatchBackground": a,
        "editor.findMatchForeground": "#FFFFFFCC",
        "editor.findMatchBorder": "#00000000",
        "editor.selectionBackground": "#3924be",
        "editor.selectionForeground": "#000c18",
        "editor.lineHighlightBorder": aa("75"),
        "editorLineNumber.foreground": a,
        "editorLineNumber.activeForeground": a,
        "editorMarkerNavigation.background": "#060621",
        "editorMarkerNavigationError.background": "#AB395B",
        "editorMarkerNavigationWarning.background": "#5B7E7A",
        "editorLink.activeForeground": "#0063a5",
        "editor.findMatchHighlightBackground": aa("66"),
        "editor.findMatchHighlightForeground": "#FFFFFF",
        "terminal.ansiBlack": c("gray"),
        "terminal.ansiBrightBlack": c("gray"),
        "terminal.ansiRed": c("red"),
        "terminal.ansiBrightRed": c("red"),
        "terminal.ansiGreen": "#98d800",
        "terminal.ansiBrightGreen": "#98d800",
        "terminal.ansiYellow": c("yellow"),
        "terminal.ansiBrightYellow": c("yellow"),
        "terminal.ansiBlue": "#5ccaef",
        "terminal.ansiBrightBlue": "#5ccaef",
        "terminal.ansiMagenta": "#f57f00",
        "terminal.ansiBrightMagenta": "#f57f00",
        "terminal.ansiCyan": "#a57fff",
        "terminal.ansiBrightCyan": "#a57fff",
        "terminal.ansiWhite": c("white"),
        "terminal.ansiBrightWhite": c("white"),
        "titleBar.activeForeground": a,
        "editorSuggestWidget.background": "#000000",
        "editorSuggestWidget.foreground": "#FFFFFF",
        "editorSuggestWidget.border": a,
        "editorSuggestWidget.highlightForeground": HIGHLIGHT_MAP[accent],
        "editorSuggestWidget.selectedBackground": aa("75"),
        "editorHoverWidget.background": "#000000",
        "editorHoverWidget.border": aa("75"),
        "editorWidget.background": "#000000",
        "editorWidget.border": "#000000",
        "editorIndentGuide.activeBackground": "#505050",
        "breadcrumb.foreground": a,
        "menu.background": "#000000",
        "menu.border": aa("75"),
        "panel.background": "#000000",
        "panel.dropBorder": a,
        "panel.border": aa("75"),
        "panelTitle.activeForeground": a,
        "panelTitle.inactiveForeground": aa("75"),
        "panelSection.border": aa("75"),
        "sideBar.background": "#000",
        "sideBarSectionHeader.border": aa("75"),
        "sideBar.border": aa("75"),
        "sideBarTitle.foreground": a,
        "sideBar.foreground": "#FFFFFF",
        "sideBarSectionHeader.background": "#000000",
        "sideBarSectionHeader.foreground": a,
        "badge.background": "#000000",
        "badge.foreground": a,
        "activityBar.background": "#000",
        "activityBar.foreground": a,
        "activityBar.border": aa("75"),
        "activityBar.inactiveForeground": aa("75"),
        "activityBarBadge.background": "#000",
        "activityBarBadge.foreground": a,
        "titleBar.activeBackground": "#000000",
        "titleBar.border": aa("75"),
        "titleBar.inactiveBackground": "#000000",
        "titleBar.inactiveForeground": a,
        "tab.activeForeground": "#FFFFFF",
        "tab.inactiveForeground": "#FFFFFF",
        "tab.unfocusedActiveForeground": "#FFFFFF",
        "tab.unfocusedInactiveForeground": "#FFFFFF",
        "tab.activeBackground": "#000000",
        "tab.inactiveBackground": "#000000",
        "tab.unfocusedActiveBackground": "#000000",
        "tab.unfocusedInactiveBackground": "#000000",
        "tab.hoverBackground": aa("25"),
        "tab.unfocusedHoverBackground": aa("25"),
        "tab.border": aa("75"),
        "tab.activeBorder": "#FFFFFF",
        "tab.unfocusedActiveBorder": a,
        "tab.activeModifiedBorder": aa("75"),
        "tab.inactiveModifiedBorder": aa("75"),
        "tab.hoverBorder": aa("75"),
        "editorGroupHeader.tabsBackground": "#000000",
        "editorGroup.border": aa("75"),
        "editorGroupHeader.tabsBorder": "#000000",
        "editorGroupHeader.border": "#000000",
        "editorGroupHeader.noTabsBackground": "#000000",
        "statusBar.background": "#000000",
        "statusBar.foreground": a,
        "statusBar.border": aa("75"),
        "statusBar.noFolderBackground": "#000000",
        "statusBar.noFolderForeground": a,
        "statusBar.debuggingBackground": DEBUG_BG_MAP[accent],
        "statusBar.debuggingForeground": a,
        "statusBarItem.hoverBackground": "#101010",
        "notificationCenter.border": a,
        "notifications.foreground": "#FFFFFF",
        "notifications.background": "#000000",
        "notifications.border": aa("75"),
        "notificationCenterHeader.background": "#000000",
        "notificationCenterHeader.foreground": "#FFFFFF",
        "editorHint.foreground": HIGHLIGHT_MAP[accent],
        "diffEditor.insertedTextBackground": "#31958A55",
        "diffEditor.insertedTextBorder": "#31958A55",
        "diffEditor.removedTextBackground": "#892F4688",
        "diffEditor.removedTextBorder": "#31958A55",
        "merge.border": aa("75"),
        "peekView.border": aa("75"),
        "peekViewTitle.background": "#000000",
        "peekViewTitleLabel.foreground": "#ffffff",
        "debugExceptionWidget.background": "#000000",
        "debugExceptionWidget.border": a,
        "debugToolBar.background": "#000000",
        "debugToolBar.border": a,
        "button.background": "#000000",
        "button.foreground": "#FFFFFF",
        "button.hoverBackground": "#000000",
        "dropdown.border": aa("75"),
        "dropdown.background": "#000000",
        "dropdown.foreground": "#FFFFFF",
        "input.background": "#000000",
        "input.foreground": "#FFFFFF",
        "input.border": aa("75"),
        "input.placeholderForeground": aa("75"),
        "checkbox.border": aa("75"),
        "quickInput.background": "#000000",
        "list.activeSelectionBackground": LIST_ACTIVE_MAP[accent],
        "list.inactiveSelectionBackground": LIST_INACTIVE_MAP[accent],
        "list.hoverBackground": aa("75"),
        "list.inactiveFocusOutline": a,
        "gitlens.trailingLineBackgroundColor": "#000000",
        "gitlens.trailingLineForegroundColor": a,
        "terminal.border": aa("75"),
        "editorWarning.foreground": c("orange"),
        "list.warningForeground": c("orange"),
        "editorOverviewRuler.warningForeground": c("orange"),
        "gitDecoration.modifiedResourceForeground": c("yellow"),
        "gitDecoration.addedResourceForeground": c("green"),
        "gitDecoration.deletedResourceForeground": c("red"),
        "gitDecoration.untrackedResourceForeground": c("green"),
        "gitDecoration.ignoredResourceForeground": c("gray"),
        "gitDecoration.conflictingResourceForeground": c("orange"),
        "gitDecoration.renamedResourceForeground": c("blue"),
        "gitDecoration.stageDeletedResourceForeground": c("red"),
        "gitDecoration.stageModifiedResourceForeground": c("yellow"),
        "gitDecoration.submoduleResourceForeground": c("purple"),
        "scrollbar.shadow": "#000000",
        "scrollbarSlider.background": aa("40"),
        "scrollbarSlider.hoverBackground": aa("70"),
        "scrollbarSlider.activeBackground": aa("CC"),
    }


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------

def serialize_theme(theme_dict):
    """Serialize the theme dict to JSON with consistent formatting."""
    return _serialize_compact(theme_dict)


def _serialize_compact(theme_dict):
    """Serialize a theme dict to JSON with compact single-line settings."""
    lines = []
    lines.append("{")
    lines.append(f'    "$schema": "vscode://schemas/color-theme",')
    lines.append(f'    "name": {json.dumps(theme_dict["name"])},')
    lines.append(f'    "tokenColors": [')

    token_colors = theme_dict["tokenColors"]
    for i, entry in enumerate(token_colors):
        comma = "," if i < len(token_colors) - 1 else ""
        _emit_token_entry_compact(lines, entry, comma)

    lines.append("    ],")
    lines.append('    "colors": {')

    colors = theme_dict["colors"]
    color_keys = list(colors.keys())
    for i, key in enumerate(color_keys):
        comma = "," if i < len(color_keys) - 1 else ""
        lines.append(f'        {json.dumps(key)}: {json.dumps(colors[key])}{comma}')

    lines.append("    }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _emit_token_entry_compact(lines, entry, comma):
    """Emit a single tokenColors entry in compact format."""
    settings = entry.get("settings", {})
    scope = entry.get("scope")
    name = entry.get("name")

    # First entry (base settings, no scope/name) gets special treatment
    if scope is None and name is None:
        lines.append("        {")
        lines.append('            "settings": {')
        settings_keys = list(settings.keys())
        for j, sk in enumerate(settings_keys):
            sc = "," if j < len(settings_keys) - 1 else ""
            lines.append(f'                {json.dumps(sk)}: {json.dumps(settings[sk])}{sc}')
        lines.append("            }")
        lines.append(f"        }}{comma}")
        return

    # Inherited class entry has multi-line settings
    if name == "Inherited class":
        lines.append("        {")
        lines.append(f'            "name": {json.dumps(name)},')
        lines.append(f'            "scope": {json.dumps(scope)},')
        lines.append('            "settings": {')
        skeys = list(settings.keys())
        for j, sk in enumerate(skeys):
            sc = "," if j < len(skeys) - 1 else ""
            lines.append(f'                {json.dumps(sk)}: {json.dumps(settings[sk])}{sc}')
        lines.append("            }")
        lines.append(f"        }}{comma}")
        return

    # Invalid entry has multi-line settings (3 keys: background, fontStyle, foreground)
    if name == "Invalid" and scope == "invalid":
        lines.append("        {")
        lines.append(f'            "name": {json.dumps(name)},')
        lines.append(f'            "scope": {json.dumps(scope)},')
        lines.append('            "settings": {')
        skeys = list(settings.keys())
        for j, sk in enumerate(skeys):
            sc = "," if j < len(skeys) - 1 else ""
            lines.append(f'                {json.dumps(sk)}: {json.dumps(settings[sk])}{sc}')
        lines.append("            }")
        lines.append(f"        }}{comma}")
        return

    # All other entries: compact single-line settings
    settings_str = _inline_obj(settings)
    lines.append("        {")

    if name is not None:
        lines.append(f'            "name": {json.dumps(name)},')

    if scope is not None:
        if _should_expand_scope(scope):
            _emit_scope_array(lines, scope, has_next=True)
        else:
            lines.append(f'            "scope": {json.dumps(scope)},')

    lines.append(f'            "settings": {settings_str}')
    lines.append(f"        }}{comma}")


def _inline_obj(obj):
    """Serialize a small dict as ``{ "key": "value", ... }`` with spaces."""
    items = []
    for k, v in obj.items():
        items.append(f"{json.dumps(k)}: {json.dumps(v)}")
    return "{ " + ", ".join(items) + " }"


def _should_expand_scope(scope):
    """Return True if a scope array should be expanded across multiple lines."""
    if not isinstance(scope, list) or len(scope) <= 1:
        return False
    # Expand when the inline representation would be long (matches original formatting)
    inline = json.dumps(scope)
    return len(inline) > 50


def _emit_scope_array(lines, scope_list, has_next=True):
    """Emit a multi-element scope array expanded across lines."""
    comma_after = "," if has_next else ""
    lines.append('            "scope": [')
    for j, s in enumerate(scope_list):
        sc = "," if j < len(scope_list) - 1 else ""
        lines.append(f"                {json.dumps(s)}{sc}")
    lines.append(f"            ]{comma_after}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

VARIANTS = ["orange", "red", "yellow", "green", "blue", "purple", "white", "gray"]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    themes_dir = os.path.join(script_dir, "themes")

    for accent in VARIANTS:
        theme = {
            "$schema": "vscode://schemas/color-theme",
            "name": f"Ember High Contrast ({accent})",
            "tokenColors": TOKEN_COLORS,
            "colors": build_colors(accent),
        }
        output = serialize_theme(theme)
        path = os.path.join(themes_dir, f"ember-high-contrast-{accent}.json")
        with open(path, "w", newline="\n") as f:
            f.write(output)
        print(f"  wrote {path}")

    print("Done.")


if __name__ == "__main__":
    main()
