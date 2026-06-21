# Phase 7 — progress checkpoint

**Resume here.** Read this file only to know what to run next. Full results live in `Docs/NOTES.md` § Phase 7.

**Last probe:** 2026-06-20 (Cursor session) — `AssetTools.find_assets` scoped to new Blueprint  
**Next probe:** Optional — `TextureTools.get_size`, `DataTableTools.search_row_structs`, graph-level Blueprint probes

## GrokProjectTools — no editor UI

Custom Python MCP toolset only. No window, panel, or menu. Invoked via MCP `call_tool` from Grok/Cursor.

| Tool | Args | Verified |
|------|------|----------|
| `health_check` | `{}` | **Pass** |
| `get_session_info` | `{}` | **Pass** (Phase 6) |

Source: `Plugins/GrokUEMCPTools/Content/Python/grok_ue_mcp/toolsets/project_tools.py`

## Done — do not re-run

### Batch F — EditorApp read-only

| ID | Tool | Result |
|----|------|--------|
| F1 | `GetCameraTransform` | Pass |
| F2 | `IsPIERunning` | Pass — `false` |
| F3 | `GetContentBrowserPath` | Pass — `/Game` |
| F4 | `GetVisibleActors` | Pass — 63 actors |

### Batch G — LogsToolset

| ID | Tool | Result |
|----|------|--------|
| G1 | `GetLogCategories` | Pass |
| G2 | `GetLogEntries` | Pass — `pattern` required |

### Batch H — ActorTools (PlayerStart ref in NOTES.md)

| ID | Tool | Result |
|----|------|--------|
| H1–H5 | label, transform, tags, components, bounds | Pass |

### Batch I — Imaging

| ID | Tool | Result |
|----|------|--------|
| I1 | `CaptureAssetImage` Cube | Pass — PNG base64; omit payload in docs |

### Batch J — Editor utilities

| ID | Tool | Result |
|----|------|--------|
| J1 | `SearchCVars` | Pass |

### Batch K — AssetTools

| ID | Tool | Result |
|----|------|--------|
| K1 | `get_plugin_content_paths` | Pass — `/GrokUEMCPTools/` |
| K2 | `list_folders` `/Game` | Pass — Collections, Developers |
| K3 | `get_asset_class` Engine Cube | Pass — StaticMesh |
| K4 | `find_assets` `folder_path: ""`, `name: ""` | Pass — 2000+ engine/plugin paths (not `/Game`-scoped) |

### Batch L — ObjectTools

| ID | Tool | Result |
|----|------|--------|
| L1 | `search_subclasses` Actor→PlayerStart | Pass |
| L2 | `get_properties` PlayerStart `bHidden` | Pass — `false` |

### Batch M — BlueprintTools

| ID | Tool | Result |
|----|------|--------|
| M1 | `get_graph_dsl_docs` | Pass — DSL grammar returned |

### Batch N — CaptureViewport (hitch)

| ID | Tool | Result |
|----|------|--------|
| N1 | `CaptureViewport` `{}` | **Fail** — `captureTransform` needs default |
| N2 | `CaptureViewport` + camera only | **Fail** — `annotations` also needs default |
| N3 | `CaptureViewport` + `captureTransform` + `annotations` | **Pass** — PNG base64; omit payload in docs |

### Batch O — ProgrammaticToolset

| ID | Tool | Result |
|----|------|--------|
| O1 | `get_execution_environment` | Pass |
| O2 | `execute_tool_script` health+level | Pass |

### Batch P — PrimitiveTools (catalog only)

**Tool catalog (4 tools, all write):** `add_cube`, `add_sphere`, `add_cylinder`, `add_cone` — add StaticMeshComponent to actor. No read-only tools; write probes deferred.

### Batch Q — StaticMeshTools

**Tool catalog (16 tools):** `get_lod_count`, `get_triangle_count`, `get_vertex_count`, `get_bounds`, `get_material_slots`, `get_material`, `get_lod_thresholds`, `is_nanite_enabled`, `set_nanite_enabled`, `generate_lods`, `remove_lods`, `set_lod_thresholds`, `generate_convex_collisions`, `remove_collisions`, `set_material`, `import_file`.

| ID | Tool | Result |
|----|------|--------|
| Q1 | `get_lod_count` `/Engine/BasicShapes/Cube.Cube` | Pass — `1` |
| Q2 | `is_nanite_enabled` Engine Cube | Pass — `false` |
| Q3 | `get_bounds` Engine Cube | Pass — ±50 cm AABB |
| Q4 | `get_material_slots` Engine Cube | Pass — `["WorldGridMaterial"]` |

### Batch R — MaterialTools (catalog only)

**Tool catalog (22 tools):** `create_material`, `create_function`, `create_parameter_collection`, `add_expression`, `delete_expression`, `get_expressions`, `layout_expressions`, `list_expression_classes`, `list_parameter_groups`, `rename_parameter_group`, `delete_parameter_group`, `get_expression_input_names`, `get_expression_output_names`, `connect_expressions`, `disconnect_expressions`, `get_expression_inputs`, `get_property_input`, `connect_to_output`, `disconnect_from_output`, `delete_unused_expressions`, `recompile`, `get_referencing_materials`. Needs `/Game` Material asset for probes — deferred.

### Batch S — TextureTools (catalog only)

**Tool catalog (2 tools):** `get_size`, `import_file`. Read probe deferred (no test Texture2D path picked).

### Batch T — DataTableTools (catalog only)

**Tool catalog (10 tools):** `search_row_structs`, `create`, `import_file`, `get_schema`, `list_rows`, `add_rows`, `remove_rows`, `rename_rows`, `get_rows`, `set_rows`. No `/Game` DataTable yet — deferred.

### Batch U — AgentSkillToolset

**Tool catalog (4 tools):** `ListSkills`, `GetSkills`, `CreateSkill`, `UpdateSkill` (write tools need user OK).

| ID | Tool | Result |
|----|------|--------|
| U1 | `ListSkills` | Pass — 4 built-in EditorToolset Python skills |

### Batch V — BlueprintTools write (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| V1 | `create` `/Game/Developers/BP_GrokPhase7Test` parent `Actor` | Pass in-memory — **not on disk until `save_assets`** |
| V2 | `get_parent` | Pass — `/Script/Engine.Actor` |
| V3 | `list_graphs` | Pass — `EventGraph`, `UserConstructionScript` |
| V4 | `save_assets` then `move` → `/Game/Developers/Brian/` | Pass on disk — CB still empty |
| V5 | `move` → `/Game/MCPTest/` + `SetContentBrowserPath` | Pass — visible in normal content path |

**Hitches:** (1) `create` needs `save_assets`. (2) `/Game/Developers/` hidden from Content Browser unless **Show Developers Content** enabled.

**Test asset:** `/Game/MCPTest/BP_GrokPhase7Test`

## Queue — run in order (one MCP call at a time)

1. Optional: `TextureTools.get_size` on engine texture; `DataTableTools.search_row_structs`
2. Optional: graph probes on `BP_GrokPhase7Test` (`read_graph_dsl`, `list_functions`)

## Skipped for now

- `StartPIE` / `StopPIE`
- `set_actor_transform`, spawn (Phase 3 covers spawn)
- Full `describe_toolset` dumps — record tool **names** only in docs