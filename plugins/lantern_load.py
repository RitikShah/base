"""Plugin for rx-module base"""


import json
import math
from collections import namedtuple
from itertools import chain
from pathlib import Path
from typing import cast

import yaml
from beet import Context, Function, FunctionTag
from beet.core.file import File, TextFile
from beet.core.utils import JsonDict
from colour import Color
from lectern import Document

SemVer = namedtuple("version", ("major", "minor", "patch"))


def get_path(ctx: Context):
    return ctx.directory / "base"


def beet_default(ctx: Context):
    """Sets up Lantern Load tags + the default load file"""

    # Config things
    config = ctx.meta.get("lantern_load", cast(JsonDict, {}))
    namespace = config.get("id", ctx.project_id)

    # Bootstrap default LL via lectern
    ctx.inject(Document).load(get_path(ctx) / "resources" / "lantern_load.md")

    template = "#{pack}:load"
    tag: JsonDict = {
        "values": [
            {
                "value": f"#{dep['id']}:load",
                "required": False,
            }
            for dep in config.get("dependencies", [])
        ]
    }
    tag["values"].append("#{namespace}:load")
    ctx.data["load:load"] = FunctionTag(tag)

    ctx.data[f"{namespace}:load"] = FunctionTag({"values": [f"{namespace}:load"]})

    messages = yaml.safe_load(
        (get_path(ctx) / "resources" / "messages.yaml").read_text()
    )["messages"]

    troubleshooting = messages["troubleshooting"]

    for i, dep in enumerate(config.get("dependencies", [])):
        parts = dep["id"].split(".")
        render_vars = {
            "version": SemVer(*dep["version"].split(".")),
            "shorthand": parts[1] if len(parts) > 1 else parts[0],
        }

        config["dependencies"][i] |= render_vars

        dep["missing"] = ctx.template.render_json(messages["missing"], **render_vars)
        dep["wrong_version"] = ctx.template.render_json(
            messages["wrong_version"], **render_vars
        )
        dep["troubleshooting"] = ctx.template.render_json(
            messages["troubleshooting"], **render_vars
        )

    load = ctx.template.render_file(
        TextFile((get_path(ctx) / "resources" / "load.mcfunction").read_text()),
        troubleshooting=troubleshooting,
    )

    content = load.content if load.content is not None else ""
    ctx.data[f"{namespace}:load"] = Function(content.split("\n"))
