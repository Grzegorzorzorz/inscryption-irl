#!/bin/env python3

# WARNING: this tool is fairly hacked together. You may have to modify it to
# make it work for your use case. Feel like refining it? Send a pull request!

import json
import pathlib


def make_json(basename: str, output_dir: pathlib.Path):
    j = {}
    j["name"] = basename
    j["images"] = {}
    j["images"]["front"] = f"{basename}.png"
    j["images"]["back"] = "common.png"

    with open(output_dir.joinpath(f"{basename}.json"),
              "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii="false", indent=4)


def main():
    project_root = pathlib.Path(__file__).resolve().parent.parent

    path_list = project_root.joinpath("res/fronts/").glob("**/*.png")

    for path in path_list:
        make_json(path.stem, project_root.joinpath("defs/cards/"))


if __name__ == "__main__":
    main()
