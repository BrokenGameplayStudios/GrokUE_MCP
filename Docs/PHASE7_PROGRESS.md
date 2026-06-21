# Phase 7 — progress checkpoint

**Resume here.** Read this file only to know what to run next. Full results live in `Docs/NOTES.md` § Phase 7.

**Last probe:** 2026-06-20 (Cursor session) — `StaticMeshTools.get_lod_count` Engine Cube  
**Next probe:** `StaticMeshTools` — more read probes or `CaptureViewport` retry

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
| N1 | `CaptureViewport` | **Fail** — optional `captureTransform` binding |

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

## Queue — run in order (one MCP call at a time)

1. `StaticMeshTools` — `is_nanite_enabled`, `get_bounds`, `get_material_slots` on Engine Cube
2. `CaptureViewport` — retry with explicit `captureTransform` from F1 camera pose
3. Blueprint write test — `BlueprintTools.create` under `/Game/Developers/` (needs user OK)
4. Remaining toolsets: MaterialTools, TextureTools, DataTableTools, AgentSkillToolset (catalog only)

## Skipped for now

- `StartPIE` / `StopPIE`
- `set_actor_transform`, spawn (Phase 3 covers spawn)
- Full `describe_toolset` dumps — record tool **names** only in docs