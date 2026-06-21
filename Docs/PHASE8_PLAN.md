# Phase 8 — Integrated content creation (planned)

**Status:** In progress — checkpoint `Docs/PHASE8_PROGRESS.md`.

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

## Open probes (remaining)

| Item | Toolset | Status |
|------|---------|--------|
| PIE / runtime verify | `EditorAppToolset` | Pending — user Output Log or `StartPIE` |
| Persist spawn in git | save `L_Grok` | Pending — user save map |

## Suggested execution order (one MCP call at a time)

```
Material → Material Function (if separate) → wire parent material
→ Material Instance → DataTable (string rows) → save all
→ Actor BP → add StaticMeshComponent → set mesh + material instance
→ write_graph_dsl: BeginPlay → Get DataTable → ForEach → Print String
→ compile_blueprint → save → spawn in L_Grok → user confirms viewport + Output Log
```

## Success criteria

- All assets on disk under `/Game/MCPTest/`
- Spawned actor visible in `L_Grok` with custom material
- Output Log shows printed strings from DataTable rows when PIE runs (or graph compile pass if PIE skipped)

## Doc hygiene

Update `Docs/PHASE7_PROGRESS.md` when Phase 8 starts; record results in `Docs/NOTES.md` § Phase 8.