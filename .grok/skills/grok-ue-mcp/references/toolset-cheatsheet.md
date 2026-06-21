# Toolset cheatsheet (GrokUE_MCP)

## Meta-tools (top-level)

- `list_toolsets`
- `describe_toolset` — `{ "toolset_name": "..." }`
- `call_tool` — `{ "toolset_name", "tool_name", "arguments" }`

## Scene (`editor_toolset.toolsets.scene.SceneTools`)

| Tool | Notes |
|------|-------|
| `get_current_level` | No args |
| `find_actors` | Requires `name`, `tag`, `collision_channels` (use `""`, `""`, `[]` for all) |
| `add_to_scene_from_asset` | `asset_path`, `name`, `xform` |
| `remove_from_scene` | `actor.refPath` |

## Editor app (`EditorToolset.EditorAppToolset`)

| Tool | Notes |
|------|-------|
| `GetSelectedActors` | No args |
| `FocusOnActors` | `actors: [{ refPath }]` |
| `GetCameraTransform` | No args — Phase 7 verified |
| `GetVisibleActors` | No args — actors in viewport frustum |
| `GetContentBrowserPath` | No args — e.g. `/Game` |
| `IsPIERunning` | No args |
| `CaptureAssetImage` | `assetPath` — PNG base64; don't log payload |
| `CaptureViewport` | Optional annotations (large payload) |

## Logs (`EditorToolset.LogsToolset`)

| Tool | Notes |
|------|-------|
| `GetLogCategories` | `filter` substring |
| `GetLogEntries` | `pattern` required; `category`, `maxEntries` |

## Actor (`editor_toolset.toolsets.actor.ActorTools`)

| Tool | Notes |
|------|-------|
| `get_label` | `actor.refPath` |
| `get_actor_transform` | `actor.refPath` |
| `get_actor_bounds` | `actor.refPath` |
| `get_components` | `actor.refPath` |
| `get_tags` | `actor.refPath` |

## Asset (`editor_toolset.toolsets.asset.AssetTools`)

| Tool | Notes |
|------|-------|
| `get_plugin_content_paths` | `include_engine` optional |
| `list_folders` | `root_path`, `recursive` |
| `get_asset_class` | `asset_path` — e.g. `/Engine/BasicShapes/Cube` → StaticMesh |
| `find_assets` | `folder_path`, `name` required (`""` = all); empty folder = engine+plugin-wide; use `/Game` to scope |

## Object (`editor_toolset.toolsets.object.ObjectTools`)

| Tool | Notes |
|------|-------|
| `search_subclasses` | `base_class.refPath`, `class_name` filter |
| `get_properties` / `list_properties` | `instance.refPath`; returns JSON string |

## Primitive (`editor_toolset.toolsets.primitive.PrimitiveTools`)

Write-only: `add_cube`, `add_sphere`, `add_cylinder`, `add_cone` — adds mesh component to actor.

## Static mesh (`editor_toolset.toolsets.static_mesh.StaticMeshTools`)

| Tool | Notes |
|------|-------|
| `get_lod_count` | `mesh.refPath` e.g. `/Engine/BasicShapes/Cube.Cube` |
| `is_nanite_enabled` | Read |
| `get_bounds` / `get_material_slots` | Read |

## Blueprint (`editor_toolset.toolsets.blueprint.BlueprintTools`)

| Tool | Notes |
|------|-------|
| `get_graph_dsl_docs` | No blueprint needed — DSL grammar |
| `create` | Needs `/Game` folder + parent class — write test |
| `read_graph_dsl` / `write_graph_dsl` | Needs existing Blueprint asset |

## Programmatic (`editor_toolset.toolsets.programmatic.ProgrammaticToolset`)

| Tool | Notes |
|------|-------|
| `get_execution_environment` | Call once before scripting |
| `execute_tool_script` | Python `run()` → dict; batch MCP calls |

**Quirk:** `CaptureViewport` fails with `{}` — optional `captureTransform` binding issue (Batch N).

## Custom (`grok_ue_mcp.toolsets.project_tools.GrokProjectTools`)

| Tool | Notes |
|------|-------|
| `health_check` | No args — confirms plugin loaded |
| `get_session_info` | No args — project name, dirs, level path |

## After editing custom tools

UE console: `ModelContextProtocol.RefreshTools` → Grok `/mcps` → `r`