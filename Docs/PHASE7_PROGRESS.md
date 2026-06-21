# Phase 7 — progress checkpoint

**Resume here.** Read this file only to know what to run next. Full results live in `Docs/NOTES.md` § Phase 7.

**Last probe:** 2026-06-20 — `DataTableTools` create + row probes on `DT_GrokPhase7Test`  
**Next probe:** Phase 7 wrap-up (mark complete)

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
| Q5 | `get_triangle_count` Engine Cube | Pass — `48` |

### Batch R — MaterialTools (verified 2026-06-20)

**Tool catalog (22 tools):** expression graph editing, parameter groups, `recompile`, etc.

| ID | Tool | Result |
|----|------|--------|
| R1 | `create_material` `/Game/MCPTest/M_GrokPhase7Test` | Pass — + `save_assets` |
| R2 | `get_expressions` empty material | Pass — `[]` |

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
| V6 | User visual confirm | Pass — screenshot `Docs/images/phase7-v1-bp-grokphase7test-mcptest.jpg` |

**Hitches:** (1) `create` needs `save_assets`. (2) `/Game/Developers/` hidden from Content Browser unless **Show Developers Content** enabled.

**Test asset:** `/Game/MCPTest/BP_GrokPhase7Test` — user-confirmed

### Batch W — TextureTools read (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| W1 | `get_size` `/Engine/EngineResources/WhiteSquareTexture.WhiteSquareTexture` | Pass — 32×32 px |

### Batch X — DataTableTools read (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| X1 | `search_row_structs` `struct_name: "*"` | Pass — 15 engine/plugin row structs (GameplayTag, UMG RichText, etc.) |

### Batch Y — Blueprint graph read on `BP_GrokPhase7Test` (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| Y1 | `list_functions` | Pass — `UserConstructionScript` implemented |
| Y2 | `get_graph` `EventGraph` | Pass — graph ref returned |
| Y3 | `read_graph_dsl` EventGraph | Pass — default events (BeginPlay, BeginOverlap, Tick); omit full DSL in docs |
| Y4 | `list_events` | Pass — BeginPlay/BeginOverlap/Tick implemented; 20+ inheritable events listed |

### Batch Z — Spawn Blueprint actor (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| Z1 | `add_to_scene_from_asset` `BP_GrokPhase7Test` → `GrokPhase7TestActor` | Pass — user confirmed in viewport |
| Z2 | `find_actors` filter `GrokPhase7TestActor` | Pass — persists in `/Game/Maps/L_Grok` |

### Batch AA — Remaining toolsets (catalog 2026-06-20)

| Toolset | Tools (names only) |
|---------|-------------------|
| `CurveTableTools` | `create`, `import_file`, `list_rows`, `add_row`, `remove_row`, `rename_row`, `add_key`, `set_keys`, `get_keys` |
| `DataAssetTools` | `create` |
| `MaterialInstanceTools` | `create`, `list_parameters`, scalar/vector/texture/static-switch get/set, `set_parent`, `clear_parameters` |
| `SkeletalMeshTools` | `import_file`, LOD/vertex/section counts, bones/sockets/morphs/materials/physics (20 tools) — no engine SK path probed |
| `StringTableTools` | `create`, `import_file`, `list_keys`, `get_entry`, `set_entry`, `remove_entry`, `get_namespace`, `get_table_id` |

| ID | Tool | Result |
|----|------|--------|
| AA1 | `MaterialInstanceTools.list_parameters` on `M_GrokPhase7Test` | Pass — `[]` (no parameters on empty material) |

### Batch AB — Testing level `L_Grok` (verified 2026-06-20)

| ID | Item | Result |
|----|------|--------|
| AB1 | User saved map → `/Game/Maps/L_Grok` | Pass — `get_session_info` / `get_current_level` agree |
| AB2 | `Config/DefaultEngine.ini` `EditorStartupMap` + `GameDefaultMap` | **Pass** — user confirmed editor opens `L_Grok` after restart |
| AB3 | MCP cannot set maps via tool | `AssetTools.read_file` rejects `Config/`; ini edit in repo is the workflow |

**Canonical test level:** `/Game/Maps/L_Grok` (`Content/Maps/L_Grok.umap`)

### Batch AC — User + MCP assets in `/Game/MCPTest/` (verified 2026-06-20)

| ID | Tool / asset | Result |
|----|--------------|--------|
| AC1 | User `LinearCurveTable_GrokPhase7Test` — `list_rows` | Pass — `["Curve"]` |
| AC2 | `add_key` + `get_keys` on `Curve` row | Pass — `(0, 0)` + `save_assets` |
| AC3 | User `M_GrokPhase7Test_Inst` — `get_asset_class` | Pass — `MaterialInstanceConstant`; `list_parameters` → `[]` |
| AC4 | `MaterialInstanceTools.create` → `M_GrokPhase7Test_MCP` | Pass — + `save_assets` |

### Batch AD — StringTableTools (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| AD1 | `create` → `/Game/MCPTest/ST_GrokPhase7Test` | Pass — + `save_assets` (same hitch as Blueprint/Material create) |
| AD2 | `list_keys` (empty table) | Pass — `[]` |
| AD3 | `get_namespace` | Pass — `ST_GrokPhase7Test` |
| AD4 | `get_table_id` | Pass — `/Game/MCPTest/ST_GrokPhase7Test.ST_GrokPhase7Test` |
| AD5 | `set_entry` key `GrokHello` | Pass |
| AD6 | `get_entry` | Pass — `Hello from Phase 7 MCP` |
| AD7 | `list_keys` (after set) | Pass — `["GrokHello"]` |

**Test asset:** `/Game/MCPTest/ST_GrokPhase7Test`

### Batch AE — DataAssetTools (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| AE1 | `create` `asset_type: PrimaryDataAsset` → `DA_GrokPhase7Test` | Pass in-memory — **`save_assets` → false**; visible in Content Browser (unsaved) |
| AE1b | `create` `asset_type: DataAsset` → `DA_GrokPhase7Test2` | Same — in-memory + CB visible; `save_assets` → false |
| AE2 | `create` `asset_type: /Script/EnhancedInput.InputAction` → `DA_GrokPhase7Test_InputAction` | Pass — + `save_assets` on first try |
| AE3 | `get_asset_class` | Pass — `InputAction` |
| AE4 | `save_assets` retry on `DA_GrokPhase7Test` + `DA_GrokPhase7Test2` (after user delay) | **Still false** — rules out registration-timing hypothesis |

**Hitch:** Abstract `asset_type` (`DataAsset`, `PrimaryDataAsset`) creates **unsaved** assets that appear in Content Browser but `save_assets` never succeeds (retried). Use a **concrete** subclass (e.g. `InputAction`).

**Test asset:** `/Game/MCPTest/DA_GrokPhase7Test_InputAction`

### Batch AF — DataTableTools write (verified 2026-06-20)

| ID | Tool | Result |
|----|------|--------|
| AF1 | `create` schema `MirrorTableRow` → `DT_GrokPhase7Test` | Pass — + `save_assets` |
| AF2 | `list_rows` (empty) | Pass — `[]` |
| AF3 | `get_schema` | Pass — `name`, `mirroredName`, `mirrorEntryType`, `bEnabled` |
| AF4 | `add_rows` `GrokRow1` | Pass |
| AF5 | `get_rows` | Pass — defaults (`mirrorEntryType: Bone`, `bEnabled: true`) |
| AF6 | `set_rows` `mirroredName: GrokMirror`, `bEnabled: false` | Pass — round-trip via `get_rows` |

**Test asset:** `/Game/MCPTest/DT_GrokPhase7Test`

## Queue — run in order (one MCP call at a time)

1. Phase 7 wrap-up — mark complete in `NOTES.md` phase table + handoff

## Skipped for now

- `StartPIE` / `StopPIE`
- `set_actor_transform`, spawn (Phase 3 covers spawn)
- Full `describe_toolset` dumps — record tool **names** only in docs