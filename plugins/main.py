"""Plugin for rx-module base"""


import json
from pathlib import Path

import yaml
from beet import Context, FunctionTag, Function
from beet.core.file import File, TextFile
from beet.core.utils import JsonDict
from lectern import Document
from importlib.resources import path, read_text
from .color import linear_gradient
import math


def function_headers(ctx: Context):
    for name, func in ctx.data.functions.items():
        func.lines.insert(0, f"# {name}")


def lantern_load(ctx: Context):
    meta = ctx.meta
    ll = meta["lantern_load"]

    temp = ll["namespace"].split(".")
    ll["shorthand"] = temp[1] if len(temp) > 1 else temp[0]

    ctx.inject(Document).add_markdown(read_text("rx_base.resources", "lantern_load.md"))

    template = "#{pack}:load"
    tag: JsonDict = {
        "values": [
            {
                "value": template.format(pack="rx." + d["name"].lower()),
                "required": False,
            }
            for d in ll["dependencies"]
        ]
    }
    tag["values"].append(template.format(pack=ll["namespace"]))
    ctx.data["load:load"] = FunctionTag(tag)

    ctx.data[f"{ll['namespace']}:load"] = FunctionTag(
        {"values": [f"{ll['namespace']}:load"]}
    )


def render_load(ctx: Context):
    meta = ctx.meta
    ll = meta["lantern_load"]

    temp = ll["namespace"].split(".")
    ll["shorthand"] = temp[1] if len(temp) > 1 else temp[0]

    meta["pretty_name"] = pretty_name(
        ctx.project_name, ll["colors"][0], ll["colors"][1]
    )

    messages = yaml.safe_load(read_text("rx_base.resources", "messages.yaml"))[
        "messages"
    ]

    for d in ll["dependencies"]:
        d["missing"] = json.dumps(ctx.template.render_json(messages["missing"], **d))
        d["wrong_version"] = json.dumps(
            ctx.template.render_json(messages["wrong_version"], **d)
        )

    load = ctx.template.render_file(
        TextFile(read_text("rx_base.resources", "load.mcfunction"))
    )

    ctx.data[f"{ll['namespace']}:load"] = Function(load.content.split("\n"))


def pretty_name(name, color1, color2):
    first_half = linear_gradient(color1, color2, math.floor(len(name) / 2))['hex']
    second_half = linear_gradient(color2, color1, math.ceil(len(name) / 2))['hex']
    pretty = [
        {"text": name, "color": color} for name, color in zip(name, first_half + second_half)
    ]
    return json.dumps(pretty)
