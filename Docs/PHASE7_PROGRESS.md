# Phase 7 — progress checkpoint

**Resume here.** Read this file only to know what to run next. Full results live in `Docs/NOTES.md` § Phase 7.

**Last probe:** 2026-06-20 (Cursor session)  
**Next probe:** `EditorAppToolset.SearchCVars` — `name: r.Shadow`

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
| F1 | `GetCameraTransform` | Pass — location ~(130, 82, 71) |
| F2 | `IsPIERunning` | Pass — `false` |
| F3 | `GetContentBrowserPath` | Pass — `/Game` |
| F4 | `GetVisibleActors` | Pass — 63 actors in frustum |

### Batch G — LogsToolset read-only

| ID | Tool | Result |
|----|------|--------|
| G1 | `GetLogCategories` `filter: ModelContextProtocol` | Pass — 2 categories |
| G2 | `GetLogEntries` `category: LogModelContextProtocol`, `pattern: Starting MCP server` | Pass — 1 entry, port 8000 |

**Quirk:** `GetLogEntries` requires `pattern` (can be `""` for all).

### Batch H — ActorTools read-only (PlayerStart)

**refPath:** `/Temp/Untitled_1.Untitled_1:PersistentLevel.PlayerStart_UAID_F02F74551BF5599B01_1153002503`

| ID | Tool | Result |
|----|------|--------|
| H1 | `get_label` | Pass — `PlayerStart` |
| H2 | `get_actor_transform` | Pass — location (-200, 0, 92), yaw 180 |
| H3 | `get_tags` | Pass — `[]` |
| H4 | `get_components` | Pass — CollisionCapsule, Sprite, Sprite2, Arrow |
| H5 | `get_actor_bounds` | Pass — valid AABB around PlayerStart |

### Batch I — Editor imaging read-only

| ID | Tool | Result |
|----|------|--------|
| I1 | `CaptureAssetImage` `/Engine/BasicShapes/Cube` | Pass — `image/png` base64 (~3 KB); **do not log full payload in docs** |

## Queue — run in order (one MCP call at a time)

1. `EditorAppToolset.SearchCVars` — `name: r.Shadow`
4. `AssetTools` — `describe_toolset` then first list/search read tool
5. `ObjectTools` — `describe_toolset` then class-discovery read tool
6. `BlueprintTools` — `describe_toolset` only (blank `/Game` project)
7. `EditorAppToolset.CaptureViewport` — `{}` (large base64; note size only in docs)
8. `ProgrammaticToolset` — `describe_toolset` then minimal script if safe

## Skipped for now (write / PIE / level mutation)

- `StartPIE` / `StopPIE`
- `set_actor_transform`, `add_tag`, spawn tests (Phase 3 already covers spawn)
- Blueprint/material create tools (need `/Game` assets first)