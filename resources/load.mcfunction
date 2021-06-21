#!set config = ctx.meta['lantern_load']

scoreboard objectives add rx.temp dummy

# we use this throughout the project
data modify storage rx:info ec.name set value {{ctx.project_name}}
data modify storage rx:info ec.pretty_name set value '{{ctx.meta.globals.pretty_name | tojson}}'

# try to check for dependencies
#  if we have no dependencies, then just set our major status
{%- for dep in lantern_load.dependencies %}
execute if score {{dep.id}} load.status matches {{dep.version.major}} if score #{{dep.id}}.minor matches {{dep.version.minor}}.. run scoreboard players set {{ctx.project_id}} load.status {{ctx.meta.version.major}}
{%- else %}
scoreboard players set {{ctx.project_id}} load.status {{ctx.meta.version.major}}
{%- endfor %}

# tellraw if loading was a success
execute if score {{ctx.project_id}} load.status matches 1.. run function {{ctx.project_id}}:init
execute if score {{ctx.project_id}} load.status matches 1.. run tellraw @a[tag=rx.admin] [{"text": "", "color": "gray"}, {{ctx.meta.globals.pretty_name | tojson}}, " v{{ctx.project_version}} loaded"]

# stop tick loop if loading failed
execute unless score {{ctx.project_id}} load.status matches 1.. run schedule clear {{ctx.project_id}}:tick

# figure out what went wrong and tellraw to the user..
#>  TODO: this could be a singular tellraw *potentially*
{%- for dep in lantern_load.dependencies %}
execute unless score {{ctx.project_id}} load.status matches 1.. unless score {{dep.id}} load.status matches 1.. run tellraw @a {{dep.missing}}
execute unless score {{ctx.project_id}} load.status matches 1.. if score {{dep.id}} load.status matches 1.. run tellraw @a {{dep.wrong_version}}
{%- endfor -%}
