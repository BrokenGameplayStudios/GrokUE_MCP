# Toolset cheatsheet (GrokUE_MCP)

## Meta-tools (top-level)

- `list_toolsets`
- `describe_toolset` — `{ "toolset_name": "..." }`
- `call_tool` — `{ "toolset_name", "tool_name", "arguments" }`

## Scene (`editor_toolset.toolsets.scene.SceneTools`)

| Tool | Notes |
|------|-------|
| `get_current_level` | No args — canonical test level: `/Game/Maps/L_Grok` |
| `load_level` | `level_path` e.g. `/Game/Maps/L_Grok` |
| `find_actors` | Requires `name`, `tag`, `collision_channels` (use `""`, `""`, `[]` for all) |
| `add_to_scene_from_asset` | `asset_path`, `name`, `xform` — works with Blueprints (e.g. `/Game/MCPTest/BP_GrokPhase7Test`) |
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
| `CaptureViewport` | Needs explicit `captureTransform` (from `GetCameraTransform`) **and** `annotations`; `bShowUI` optional — PNG base64 |

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
| `save_assets` | `asset_paths` array — **required after Blueprint `create`** |

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
| `get_lod_count` | `mesh.refPath` e.g. `/Engine/BasicShapes/Cube.Cube` → `1` |
| `get_triangle_count` | Engine Cube → `48` |
| `is_nanite_enabled` | Engine Cube → `false` |
| `get_bounds` | Engine Cube → ±50 cm AABB |
| `get_material_slots` | Engine Cube → `["WorldGridMaterial"]` |

## Blueprint (`editor_toolset.toolsets.blueprint.BlueprintTools`)

| Tool | Notes |
|------|-------|
| `get_graph_dsl_docs` | No blueprint needed — DSL grammar |
| `create` | `folder_path`, `asset_name`, `asset_type.refPath` — then **`save_assets`**; use `/Game/MCPTest/` not `/Game/Developers/` (CB hides Developers) |
| `get_parent` / `list_graphs` / `list_functions` / `list_events` | `blueprint.refPath` |
| `get_graph` | `blueprint.refPath`, `graph_name` (e.g. `EventGraph`) |
| `read_graph_dsl` / `write_graph_dsl` | `graph.refPath` from `get_graph` |

## Programmatic (`editor_toolset.toolsets.programmatic.ProgrammaticToolset`)

| Tool | Notes |
|------|-------|
| `get_execution_environment` | Call once before scripting |
| `execute_tool_script` | Python `run()` → dict; batch MCP calls |

## Material (`editor_toolset.toolsets.material.MaterialTools`)

| Tool | Notes |
|------|-------|
| `create_material` | `folder_path`, `asset_name` — then **`save_assets`** |
| `get_expressions` | `material_or_function.refPath` — empty on new material |

22 graph-editing tools total; graph write probes deferred.

## Texture (`editor_toolset.toolsets.texture.TextureTools`)

| Tool | Notes |
|------|-------|
| `get_size` | `texture.refPath` — e.g. WhiteSquareTexture → 32×32 |
| `import_file` | Write — `folder_path`, `asset_name`, `source_file` |

## Data table (`editor_toolset.toolsets.data_table.DataTableTools`)

| Tool | Notes |
|------|-------|
| `search_row_structs` | `struct_name` — use `"*"` for all TableRowBase subclasses |
| `create`, `list_rows`, `get_rows`, `set_rows` | Need existing DataTable asset |

## Agent skills (`ToolsetRegistry.AgentSkillToolset`)

| Tool | Notes |
|------|-------|
| `ListSkills` | No args — returns built-in EditorToolset Python skills |
| `GetSkills` | `skillPaths` array |
| `CreateSkill` / `UpdateSkill` | Write — needs user OK |

## Curve table (`editor_toolset.toolsets.curve_table.CurveTableTools`)

| Tool | Notes |
|------|-------|
| `list_rows` | `curve_table.refPath` |
| `add_key` / `get_keys` | `row_name` + `SimpleCurveKey` — then `save_assets` |

## Material instance (`editor_toolset.toolsets.material_instance.MaterialInstanceTools`)

| Tool | Notes |
|------|-------|
| `create` | `folder_path`, `asset_name`, `parent.refPath` — then **`save_assets`** |
| `list_parameters` | On empty parent material → `[]` |

## String table (`editor_toolset.toolsets.string_table.StringTableTools`)

| Tool | Notes |
|------|-------|
| `create` | `folder_path`, `asset_name` — then **`save_assets`** |
| `list_keys` | `string_table.refPath` |
| `get_namespace` / `get_table_id` | Namespace = asset name; table ID = full refPath |
| `set_entry` / `get_entry` | `key`, `value` — then **`save_assets`** |

## Data asset (`editor_toolset.toolsets.data_asset.DataAssetTools`)

| Tool | Notes |
|------|-------|
| `create` | `folder_path`, `asset_name`, `asset_type.refPath` — then **`save_assets`** |
| | Abstract types (`DataAsset`, `PrimaryDataAsset`) appear in CB but stay unsaved — `save_assets` → `false` even on retry; use concrete subclass (e.g. `InputAction`) |

## Data table (`editor_toolset.toolsets.data_table.DataTableTools`)

| Tool | Notes |
|------|-------|
| `search_row_structs` | `struct_name: "*"` — pick a `TableRowBase` struct |
| `create` | `folder_path`, `asset_name`, `schema.refPath` — then **`save_assets`** |
| `list_rows` / `get_schema` / `get_rows` | `data_table.refPath` |
| `add_rows` / `set_rows` | `set_rows` takes `values` as JSON **string** — then **`save_assets`** |

## Skeletal mesh (`editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools`)

20 tools (bones, sockets, LOD, materials, `import_file`) — no engine skeletal mesh probed in blank project.

**Quirk:** `CaptureViewport` fails with `{}` — pass explicit `captureTransform` + `annotations` (Batch N).

## Custom (`grok_ue_mcp.toolsets.project_tools.GrokProjectTools`)

| Tool | Notes |
|------|-------|
| `health_check` | No args — confirms plugin loaded |
| `get_session_info` | No args — project name, dirs, level path |

## After editing custom tools

UE console: `ModelContextProtocol.RefreshTools` → Grok `/mcps` → `r`