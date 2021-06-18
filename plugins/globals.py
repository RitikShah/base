"""Plugin for rx-module base"""


import json
from pathlib import Path
from beet.library.data_pack import Advancement

import yaml
from beet import Context, FunctionTag, Function
from beet.core.file import File, TextFile
import math


def advancements(ctx: Context):
    ctx.data['global:root'] = Advancement({
        "display": {
            "title": "Installed Datapacks",
            "description": "",
            "icon": {"item": "minecraft:knowledge_book"},
            "background": "minecraft:textures/block/gray_concrete.png",
            "show_toast": False,
            "announce_to_chat": False,
        },
        "criteria": {"trigger": {"trigger": "minecraft:tick"}},
    })

    ctx.data['global:rx97'] = Advancement({
        "display": {
            "title": "rx97",
            "description": "I guess I make datapacks",
            "icon": {"item": "minecraft:player_head", "nbt": "{SkullOwner: 'rx97'}"},
            "show_toast": False,
            "announce_to_chat": False,
        },
        "parent": "global:root",
        "criteria": {"trigger": {"trigger": "minecraft:tick"}},
    })

    ctx.data[f"{ctx.meta['namespace']}:global"] = Advancement({
        "display": {
            "title": ctx.meta["pretty_name"],
            "description": ctx.project_description,
            "icon": {"item": ctx.meta["global"]["item"]},
            "announce_to_chat": False,
            "show_toast": False,
        },
        "parent": "global:rx",
        "criteria": {"trigger": {"trigger": "minecraft:tick"}},
    })
