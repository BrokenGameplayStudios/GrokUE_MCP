# Phase 8 — Integrated content creation (planned)

**Status:** Phase 8 **complete** (2026-06-21) — H1 + H2; checkpoint `Docs/PHASE8_PROGRESS.md`.

**Goal:** Prove MCP can chain asset types with **logic** — each step is basic alone; the full pipeline is the stress test.

## Target scenario (user-specified)

Build a small vertical slice in `/Game/MCPTest/` on level `/Game/Maps/L_Grok`:

1. **Material** — create parent material (`MaterialTools.create_material`)
2. **Material function** — expression graph helper (MaterialTools expression tools)
3. **Material instance** — child of parent material (`MaterialInstanceTools.create` + parameter overrides)
4. **DataTable** — string rows (`DataTableTools` — pick a row struct with a string field, or use `RichTextStyleRow` / custom)
5. **Actor Blueprint** — static mesh component + assigned material instance
6. **Blueprint logic** — on BeginPlay (or custom event): **ForEach** DataTable rows → **Print String** each value

## Prerequisites (Phase 7 provides)

| Capability | Verified batch |
|------------|----------------|
| Material create + save | R |
| Material instance create | AC |
| DataTable create + rows | AF |
| Actor Blueprint create + spawn | V, Z |
| Blueprint graph read | Y |
| Blueprint variables | AG |
| ObjectTools set/get properties | AG |
| StringTable / DataTable string data | AD, AF |

## Batch H2 — Web mesh import (complete 2026-06-21)

1. Download CC0 mesh (Kenney Furniture Kit OBJ)
2. `ImportedAssets/scripts/scale_obj_to_ue_cm.py --kenney-ue --target-max-cm <N>`
3. `StaticMeshTools.import_file` (FBX/OBJ only; glTF fails)
4. `set_material` + `add_to_scene_from_asset` at scale 1, rotation 0

**Success criteria (H2 — met 2026-06-21):**

- [x] `import_file` probed (FBX + OBJ; glTF/GLB rejected)
- [x] Bounds-targeted size at actor scale 1 via pre-import scaler
- [x] Kenney axis fixes: Z-up, +X forward, normals, 180° Z — see `Docs/NOTES.md` § Phase 8
- [x] Final viewport — `Docs/images/phase8-h2-kenney-imports-final.jpg`

## Optional follow-ups

| Item | Status |
|------|--------|
| Save `L_Grok` spawns in git | User saves locally; `__ExternalActors__` gitignored |
| `StartPIE` via MCP | Skipped — user PIE confirmed prints (H1) |
| Phase 2 — DEM heightmap landscape | Planned — no Landscape MCP toolset |

## Suggested execution order (one MCP call at a time)

```
Material → Material Function (if separate) → wire parent material
→ Material Instance → DataTable (string rows) → save all
→ Actor BP → add StaticMeshComponent → set mesh + material instance
→ write_graph_dsl: BeginPlay → Get DataTable → ForEach → Print String
→ compile_blueprint → save → spawn in L_Grok → user confirms viewport + Output Log
```

## Success criteria (H1 — met 2026-06-20)

- [x] All assets on disk under `/Game/MCPTest/`
- [x] Spawned actor visible in `L_Grok` with custom material (`M_GrokPhase8_Inst`)
- [x] Output Log prints all 3 DataTable `mirroredName` strings on PIE — see `Docs/images/phase8-h1-pie-datatable-prints.jpg`

## Doc hygiene

Update `Docs/PHASE7_PROGRESS.md` when Phase 8 starts; record results in `Docs/NOTES.md` § Phase 8.