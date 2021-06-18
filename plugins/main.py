"""Plugin for rx-module base"""


import json
from pathlib import Path

import yaml
from beet import Context, FunctionTag, Function
from beet.core.file import File, TextFile
from beet.core.utils import JsonDict
from lectern import Document
from colour import Color
import math
from itertools import chain


def get_path(ctx: Context):
    return ctx.directory / "base"

def beet_default(ctx: Context):
    yield
    ctx.require("beet.contrib.render")
    ctx.require("beet.contrib.hangman")
    ctx.require("beet.contrib.yellow_shulker_box")


def function_headers(ctx: Context):
    for name, func in ctx.data.functions.items():
        func.lines.insert(0, f"# {name}")


def lantern_load(ctx: Context):
    meta = ctx.meta
    ll = meta["lantern_load"]

    temp = ll["namespace"].split(".")
    ll["shorthand"] = temp[1] if len(temp) > 1 else temp[0]

    ctx.inject(Document).load(get_path(ctx) / "resources" / "lantern_load.md")

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

    meta["pretty_name"] = pretty_name(ctx, ll["colors"][0], ll["colors"][1])

    messages = yaml.safe_load(
        (get_path(ctx) / "resources" / "messages.yaml").read_text()
    )["messages"]

    major, minor, patch = ctx.project_version.split('.')

    for d in ll["dependencies"]:
        d["storage_shorthand"] = ll["shorthand"]

        d["major"], d["minor"], d["patch"] = major, minor, patch

        missing = ctx.template.render_json(messages["missing"], **d)
        d["missing"] = json.dumps(
            missing
        )

        wrong_version = ctx.template.render_json(messages["wrong_version"], **d)
        d["wrong_version"] = json.dumps(
            wrong_version
        )

    load = ctx.template.render_file(
        TextFile((get_path(ctx) / "resources" / "load.mcfunction").read_text())
    )

    ctx.data[f"{ll['namespace']}:load"] = Function(load.content.split("\n"))


def pretty_name(ctx, color1, color2):
    name = ctx.project_name

    color1, color2 = Color(color1), Color(color2)

    first_half = color1.range_to(color2, math.floor(len(name) / 2))
    second_half = color2.range_to(color1, math.ceil(len(name) / 2))

    return [
        {"text": letter, "color": color.hex_l}
        for letter, color in zip(name, chain(first_half, second_half))
    ]
