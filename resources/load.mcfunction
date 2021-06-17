#!set namespace = ctx.meta['lantern_load']['namespace']
#!set lantern_load = ctx.meta['lantern_load']

#!set init = namespace + ":init"
#!set tick = namespace + ":tick"
#!set tellraw_header = '{"text":"", "color":"gray"}, {"nbt": "' + lantern_load['shorthand'] + '.pretty_name", "storage": "rx:info", "interpret": true}, " "'


#!set major = ctx.project_version.split('.')[0]
#!set minor = ctx.project_version.split('.')[1]
#!set patch = ctx.project_version.split('.')[2]

scoreboard objectives add rx.temp dummy

data modify storage rx:info ec.name set value {{ctx.project_name}}
data modify storage rx:info ec.pretty_name set value {{ctx.meta.pretty_name}}

{% for d in lantern_load.dependencies %}
{%- set d_major = d['version'].split('.')[0] %}
{%- set d_minor = d['version'].split('.')[1] %}
execute if score {{d['namespace']}} load.status matches 1.. if score {{d['namespace']}} load.status matches {{d_major}} if score #{{d['namespace']}}.minor matches {{d_minor}}.. run scoreboard players set {{namespace}} load.status {{major}}
{%- endfor %}

execute if score {{namespace}} load.status matches 1.. run function {{init}}
execute if score {{namespace}} load.status matches 1.. run tellraw @a[tag=rx.admin] [{{tellraw_header}}, {"storage": "rx:info", "nbt": "{{lantern_load.shorthand}}.version.major"}, ".", {"storage": "rx:info", "nbt": "{{lantern_load.shorthand}}.version.minor"}, ".", {"storage": "rx:info", "nbt": "{{lantern_load.shorthand}}.version.patch"}, " loaded"]

execute unless score {{namespace}} load.status matches 1.. run schedule clear {{tick}}

{%- for d in lantern_load.dependencies %}
{%- set d_major = d['version'].split('.')[0] %}
{%- set d_minor = d['version'].split('.')[1] %}
execute unless score {{namespace}} load.status matches 1.. unless score {{d['namespace']}} load.status matches 1.. run tellraw @a {{d['missing']}}
execute unless score {{namespace}} load.status matches 1.. if score {{d['namespace']}} load.status matches 1.. run tellraw @a {{d['wrong_version']}}
{%- endfor %}
