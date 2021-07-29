#!set config = ctx.meta['lantern_load']

{% macro dep_check(dep) -%}
if score {{dep.id}} load.status matches {{dep.version[0]}} if score #{{dep.id}}.minor matches {{dep.version[1]}}..
{% endmacro -%}

scoreboard objectives add rx.temp dummy

# we use this throughout the project
data modify storage rx:info ec.name set value {{ctx.project_name}}
data modify storage rx:info ec.pretty_name set value '{{ctx.meta.globals.pretty_name | tojson}}'

# try to check for dependencies
#  if we have no dependencies, then just set our major status
{%- if lantern_load.dependencies %}
execute {%- for dep in lantern_load.dependencies %} {{dep_check(dep)}} {% endfor %} run scoreboard players set {{ctx.project_id}} load.status {{ctx.meta.version.major}}
{%- else %}
scoreboard players set {{ctx.project_id}} load.status {{ctx.meta.version.major}}
{%- endif %}

# tellraw if loading was a success
execute if score {{ctx.project_id}} load.status matches 1.. run function {{ctx.project_id}}:init
execute if score {{ctx.project_id}} load.status matches 1.. run tellraw @a[tag=rx.admin] [{"text": "", "color": "gray"}, {{ctx.meta.globals.pretty_name | tojson}}, " v{{ctx.project_version}} loaded"]

# stop tick loop if loading failed
execute unless score {{ctx.project_id}} load.status matches 1.. run schedule clear {{ctx.project_id}}:tick

# figure out what went wrong and tellraw to the user..
{%- for dep in lantern_load.dependencies %}
execute unless score {{ctx.project_id}} load.status matches 1.. unless score {{dep.id}} load.status matches 1.. run tellraw @a {{dep.missing | tojson}}
execute unless score {{ctx.project_id}} load.status matches 1.. if score {{dep.id}} load.status matches 1.. run tellraw @a {{dep.wrong_version | tojson}}
execute unless score {{ctx.project_id}} load.status matches 1.. run tellraw @a {{dep.troubleshooting | tojson}}
{%- endfor -%}
