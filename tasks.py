import json
import copy

from invoke import context, task

@task
def build_colors(c):

    base_colors = ["#43B9D8", "#02B5FC75", "#02B5FC25", "#02B5FC15", "#FD971F", "#FD971F15"]

    features = {
        "orange": ["#FD971F", "#FD971F75", "#FD971F25", "#FD971F15", "#F9C449", "#F9C44915"],
        "green ": ["#19FC8E", "#19FC8E75", "#19FC8E25", "#19FC8E15", "#43B9D8", "#43B9D815"],
        "purple": ["#AE81FF", "#AE81FF75", "#AE81FF25", "#AE81FF15", "#43B9D8", "#43B9D815"],
        "yellow": ["#F9C449", "#F9C44975", "#F9C44925", "#F9C44915", "#FD971F", "#FD971F15"],
        "red   ": ["#F43F1A", "#F43F1A75", "#F43F1A25", "#F43F1A15", "#F9C449", "#F9C44915"],
        "gray  ": ["#8f8f8f", "#8f8f8f75", "#8f8f8f25", "#8f8f8f15", "#43B9D8", "#43B9D815"],
        "white ": ["#f1f1f1", "#f1f1f175", "#f1f1f125", "#f1f1f115", "#43B9D8", "#43B9D815"],
    }

    with open("themes/ember-high-contrast.json") as f:
        base_theme = json.load(f)

    for feature_name, colors in features.items():
        feature_name = feature_name.strip()
        theme = copy.deepcopy(base_theme)
        theme["name"] = theme["name"] + f" ({feature_name})"

        for name, hex_code in theme["colors"].items():
            for i, base_hex_code in enumerate(base_colors):
                if base_hex_code == hex_code:
                    theme["colors"][name] = colors[i]

        file_name = f"themes/ember-high-contrast-{feature_name}.json"
        with open(file_name, "w") as f:
            json.dump(theme, f)
        c.run(f"npx prettier --write {file_name}")

@task
def deploy(c):
	c.run("npx vsce package")
	c.run("npx vsce publish")

@task
def convert_vim(c):
    c.run("~/.gem/ruby/2.7.0/bin/tm2vim ./themes/ember-high-contrast.xml ./themes/ember-high-contrast.vim")

if __name__ == "__main__":
    build_colors(context.Context())