#!/usr/bin/env python3
"""Generate all 8 Ember High Contrast theme JSON files from a single source of truth."""

import json
import os

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

PALETTE = {
    # Accent colors (one per theme variant)
    "orange":       "#E96401",
    "red":          "#F43F1A",
    "yellow":       "#F9B031",
    "green":        "#19FC8E",
    "blue":         "#02B5FC",
    "purple":       "#AE81FF",
    "white":        "#f1f1f1",
    "gray":         "#8f8f8f",
    "cyan":         "#43B9D8",
    # Terminal overrides (differ from accent colors of the same name)
    "term_green":   "#98d800",
    "term_blue":    "#5ccaef",
    "term_magenta": "#f57f00",
    "term_cyan":    "#a57fff",
    # Neutrals
    "fg":           "#FFFFFF",
    "bg":           "#000000",
    "transparent":  "#00000000",
    "ivory":        "#F8F8F0",
    "chalk":        "#F8F8F2",
    "smoke":        "#CFCFC2",
    "dim_gray":     "#787878",
    "charcoal":     "#505050",
    "soot":         "#3B3A32",
    "ash":          "#222218",
    "midnight":     "#101010",
    "ink":          "#060621",
    "coal":         "#000c18",
    # Tints
    "indigo":       "#3924be",
    "amber":        "#9D550F",
    "gold":         "#FFE792",
    "khaki":        "#75715E",
    "teal":         "#31958A",
    "rose":         "#892F46",
    "cerise":       "#AB395B",
    "sage":         "#5B7E7A",
    "cobalt":       "#0063a5",
    "mahogany":     "#2c120b",
}

FG          = PALETTE["fg"]
BG          = PALETTE["bg"]
TRANSPARENT = PALETTE["transparent"]


def c(expr):
    """Resolve ``"color"`` or ``"color/alpha"`` where alpha is 0–255.

    >>> c("red")
    '#F43F1A'
    >>> c("red/160")
    '#F43F1AA0'
    """
    if "/" in expr:
        name, alpha_str = expr.split("/", 1)
        return f"{PALETTE[name]}{int(alpha_str):02X}"
    return PALETTE[expr]


# ---------------------------------------------------------------------------
# Token colors (shared across all variants)
# ---------------------------------------------------------------------------

TOKEN_COLORS = [
    {
        "settings": {
            "foreground": FG,
            "background": c("coal"),
            "caret": c("ivory"),
            "invisibles": c("soot"),
            "lineHighlight": c("mahogany"),
            "selection": c("mahogany"),
            "findHighlight": c("gold"),
            "findHighlightForeground": BG,
            "selectionBorder": c("ash"),
            "activeGuide": c("amber/176"),
            "bracketsForeground": c("chalk/165"),
            "bracketsOptions": "underline",
            "bracketContentsForeground": c("chalk/165"),
            "bracketContentsOptions": "underline",
            "tagsOptions": "stippled_underline",
        }
    },
    {
        "name": "Comment",
        "scope": ["comment"],
        "settings": {"foreground": c("dim_gray")},
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
            "foreground": c("ivory"),
        },
    },
    {
        "name": "Invalid deprecated",
        "scope": "invalid.deprecated",
        "settings": {"background": c("purple"), "foreground": c("ivory")},
    },
    {
        "name": "JSON String",
        "scope": ["meta.structure.dictionary.json", "string.quoted.double.json"],
        "settings": {"foreground": c("smoke")},
    },
    {
        "name": "diff.header",
        "scope": "meta.diff, meta.diff.header",
        "settings": {"foreground": c("khaki")},
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
        "settings": {"foreground": c("purple/160")},
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
        "settings": {"foreground": FG, "fontStyle": "bold"},
    },
    {
        "scope": "markup.italic.markdown",
        "settings": {"foreground": FG, "fontStyle": "italic"},
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
        "settings": {"foreground": FG},
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

# editor.findMatchBackground — accent + alpha
FIND_MATCH_ALPHA = {
    "orange": 255, "red": 255, "yellow": 200, "green": 200,
    "blue":   255, "purple": 255, "white": 150, "gray": 255,
}

# list.activeSelectionBackground — accent + alpha (lighter accents need lower
# opacity to achieve similar visual weight)
LIST_ACTIVE_ALPHA = {
    "orange": 204, "red": 204, "yellow": 154, "green": 156,
    "blue":   204, "purple": 204, "white": 124, "gray": 204,
}

# list.inactiveSelectionBackground — accent + alpha
LIST_INACTIVE_ALPHA = {
    "orange": 96, "red": 96, "yellow": 83, "green": 96,
    "blue":   96, "purple": 96, "white": 79, "gray": 96,
}


def build_colors(accent):
    """Build the ``colors`` dict for a given accent name."""
    a = PALETTE[accent]  # accent color, e.g. "#E96401"

    # Helper for accent + alpha (0–255)
    def aa(alpha):
        return f"{a}{alpha:02X}"

    return {
        "foreground": FG,
        "icon.foreground": FG,
        "contrastBorder": aa(117),
        "contrastActiveBorder": TRANSPARENT,
        "focusBorder": aa(117),
        "editor.foreground": FG,
        "editor.background": BG,
        "editor.inactiveSelectionBackground": c("indigo/164"),
        "editor.findMatchBackground": aa(FIND_MATCH_ALPHA[accent]),
        "editor.findMatchForeground": c("fg/204"),
        "editor.findMatchBorder": TRANSPARENT,
        "editor.selectionBackground": c("indigo"),
        "editor.selectionForeground": c("coal"),
        "editor.lineHighlightBorder": aa(117),
        "editorLineNumber.foreground": a,
        "editorLineNumber.activeForeground": a,
        "editorMarkerNavigation.background": c("ink"),
        "editorMarkerNavigationError.background": c("cerise"),
        "editorMarkerNavigationWarning.background": c("sage"),
        "editorLink.activeForeground": c("cobalt"),
        "editor.findMatchHighlightBackground": aa(102),
        "editor.findMatchHighlightForeground": FG,
        "terminal.ansiBlack": c("gray"),
        "terminal.ansiBrightBlack": c("gray"),
        "terminal.ansiRed": c("red"),
        "terminal.ansiBrightRed": c("red"),
        "terminal.ansiGreen": c("term_green"),
        "terminal.ansiBrightGreen": c("term_green"),
        "terminal.ansiYellow": c("yellow"),
        "terminal.ansiBrightYellow": c("yellow"),
        "terminal.ansiBlue": c("term_blue"),
        "terminal.ansiBrightBlue": c("term_blue"),
        "terminal.ansiMagenta": c("term_magenta"),
        "terminal.ansiBrightMagenta": c("term_magenta"),
        "terminal.ansiCyan": c("term_cyan"),
        "terminal.ansiBrightCyan": c("term_cyan"),
        "terminal.ansiWhite": c("white"),
        "terminal.ansiBrightWhite": c("white"),
        "titleBar.activeForeground": a,
        "editorSuggestWidget.background": BG,
        "editorSuggestWidget.foreground": FG,
        "editorSuggestWidget.border": a,
        "editorSuggestWidget.highlightForeground": HIGHLIGHT_MAP[accent],
        "editorSuggestWidget.selectedBackground": aa(117),
        "editorHoverWidget.background": BG,
        "editorHoverWidget.border": aa(117),
        "editorWidget.background": BG,
        "editorWidget.border": BG,
        "editorIndentGuide.activeBackground": c("charcoal"),
        "breadcrumb.foreground": a,
        "menu.background": BG,
        "menu.border": aa(117),
        "panel.background": BG,
        "panel.dropBorder": a,
        "panel.border": aa(117),
        "panelTitle.activeForeground": a,
        "panelTitle.inactiveForeground": aa(117),
        "panelSection.border": aa(117),
        "sideBar.background": BG,
        "sideBarSectionHeader.border": aa(117),
        "sideBar.border": aa(117),
        "sideBarTitle.foreground": a,
        "sideBar.foreground": FG,
        "sideBarSectionHeader.background": BG,
        "sideBarSectionHeader.foreground": a,
        "badge.background": BG,
        "badge.foreground": a,
        "activityBar.background": BG,
        "activityBar.foreground": a,
        "activityBar.border": aa(117),
        "activityBar.inactiveForeground": aa(117),
        "activityBarBadge.background": BG,
        "activityBarBadge.foreground": a,
        "titleBar.activeBackground": BG,
        "titleBar.border": aa(117),
        "titleBar.inactiveBackground": BG,
        "titleBar.inactiveForeground": a,
        "tab.activeForeground": FG,
        "tab.inactiveForeground": FG,
        "tab.unfocusedActiveForeground": FG,
        "tab.unfocusedInactiveForeground": FG,
        "tab.activeBackground": BG,
        "tab.inactiveBackground": BG,
        "tab.unfocusedActiveBackground": BG,
        "tab.unfocusedInactiveBackground": BG,
        "tab.hoverBackground": aa(37),
        "tab.unfocusedHoverBackground": aa(37),
        "tab.border": aa(117),
        "tab.activeBorder": FG,
        "tab.unfocusedActiveBorder": a,
        "tab.activeModifiedBorder": aa(117),
        "tab.inactiveModifiedBorder": aa(117),
        "tab.hoverBorder": aa(117),
        "editorGroupHeader.tabsBackground": BG,
        "editorGroup.border": aa(117),
        "editorGroupHeader.tabsBorder": BG,
        "editorGroupHeader.border": BG,
        "editorGroupHeader.noTabsBackground": BG,
        "statusBar.background": BG,
        "statusBar.foreground": a,
        "statusBar.border": aa(117),
        "statusBar.noFolderBackground": BG,
        "statusBar.noFolderForeground": a,
        "statusBar.debuggingBackground": aa(21) if accent == "blue" else c("cyan/21"),
        "statusBar.debuggingForeground": a,
        "statusBarItem.hoverBackground": c("midnight"),
        "notificationCenter.border": a,
        "notifications.foreground": FG,
        "notifications.background": BG,
        "notifications.border": aa(117),
        "notificationCenterHeader.background": BG,
        "notificationCenterHeader.foreground": FG,
        "editorHint.foreground": HIGHLIGHT_MAP[accent],
        "diffEditor.insertedTextBackground": c("teal/85"),
        "diffEditor.insertedTextBorder": c("teal/85"),
        "diffEditor.removedTextBackground": c("rose/136"),
        "diffEditor.removedTextBorder": c("teal/85"),
        "merge.border": aa(117),
        "peekView.border": aa(117),
        "peekViewTitle.background": BG,
        "peekViewTitleLabel.foreground": FG,
        "debugExceptionWidget.background": BG,
        "debugExceptionWidget.border": a,
        "debugToolBar.background": BG,
        "debugToolBar.border": a,
        "button.background": BG,
        "button.foreground": FG,
        "button.hoverBackground": BG,
        "dropdown.border": aa(117),
        "dropdown.background": BG,
        "dropdown.foreground": FG,
        "input.background": BG,
        "input.foreground": FG,
        "input.border": aa(117),
        "input.placeholderForeground": aa(117),
        "checkbox.border": aa(117),
        "quickInput.background": BG,
        "list.activeSelectionBackground": aa(LIST_ACTIVE_ALPHA[accent]),
        "list.inactiveSelectionBackground": aa(LIST_INACTIVE_ALPHA[accent]),
        "list.hoverBackground": aa(117),
        "list.inactiveFocusOutline": a,
        "gitlens.trailingLineBackgroundColor": BG,
        "gitlens.trailingLineForegroundColor": a,
        "terminal.border": aa(117),
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
        "scrollbar.shadow": BG,
        "scrollbarSlider.background": aa(64),
        "scrollbarSlider.hoverBackground": aa(112),
        "scrollbarSlider.activeBackground": aa(204),
        # Chat UI
        "chat.requestBubbleBackground": aa(37),
        "chat.requestBubbleHoverBackground": aa(50),
        "chat.requestCodeBorder": aa(80),
        "chat.slashCommandBackground": aa(37),
        "chat.slashCommandForeground": a,
        "chat.avatarBackground": BG,
        "chat.avatarForeground": a,
        "chat.editedFileForeground": a,
        "chat.linesAddedForeground": c("green"),
        "chat.linesRemovedForeground": c("red"),
        "chat.checkpointSeparator": aa(117),
        "chat.thinkingShimmer": a,
        # Inline Chat
        "inlineChat.background": BG,
        "inlineChat.foreground": FG,
        "inlineChat.border": aa(117),
        "inlineChatInput.border": aa(117),
        "inlineChatInput.focusBorder": a,
        "inlineChatInput.background": BG,
        "inlineChatInput.placeholderForeground": aa(117),
        "inlineChatDiff.inserted": c("teal/85"),
        "inlineChatDiff.removed": c("rose/136"),
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
