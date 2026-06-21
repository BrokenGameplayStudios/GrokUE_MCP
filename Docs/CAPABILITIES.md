# What Grok + Unreal MCP can do

Human-readable summary of **what we tested** in this repo (Phases 0–8, June 2026). For step-by-step history and screenshots, see [NOTES.md](NOTES.md). For tool argument details, see [.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md](../.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md).

**Legend:** ✅ verified end-to-end · 🔶 probed / partial · 📋 cataloged only · ❓ not probed (may exist) · ❌ failed or not available

> **This document is not a complete MCP API reference.** It summarizes what we exercised in this repo. Epic may ship more tools than we called; we often recorded tool **names** without running every one. For the live catalog, always use `list_toolsets` → `describe_toolset` in a connected session.

---

## How complete is this list?

| Question | Answer |
|----------|--------|
| Is this every MCP tool? | **No.** We document **20 toolsets** (19 Epic + `GrokProjectTools`) as of our UE 5.8 test window. Patches, plugins, or project changes can add or rename tools. |
| Did we run every tool in each toolset? | **No.** Phase 7 mixed **read probes**, **write probes**, and **catalog-only** passes (tool names from `describe_toolset`, not executed). A 📋 or ❓ row here does **not** mean “the only things left untested.” |
| What is authoritative? | **`list_toolsets`** — toolset names · **`describe_toolset`** — every tool name + JSON schema for that toolset · **[toolset-cheatsheet.md](../.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md)** — our notes on tools we touched most |
| What does “not tested” below mean? | **Examples** of gaps we know about — **not** a full inventory of everything we skipped. Many tools in probed toolsets were never called. |

---

## In plain language — ask Grok to…

| You want to… | Status | Example |
|--------------|--------|---------|
| Check the bridge is alive | ✅ | `GrokProjectTools.health_check` |
| See which level is open | ✅ | `SceneTools.get_current_level` → `/Game/Maps/L_Grok` |
| List actors in the level | ✅ | `SceneTools.find_actors` (empty name/tag filter) |
| Spawn a mesh or Blueprint in the level | ✅ | `SceneTools.add_to_scene_from_asset` |
| Move, rotate, or remove an actor | ✅ | `ActorTools.set_actor_transform`, `SceneTools.remove_from_scene` |
| Focus the viewport on something | ✅ | `EditorAppToolset.FocusOnActors` |
| Take a viewport or asset screenshot | ✅ | `CaptureViewport` / `CaptureAssetImage` (needs explicit camera args) |
| Read the UE Output Log | ✅ | `LogsToolset.GetLogEntries` |
| Create and save Blueprints | ✅ | `BlueprintTools.create` + **`AssetTools.save_assets`** |
| Add Blueprint graph logic (nodes, wires) | ✅ | `write_graph_dsl` — Phase 8 ForEach → Print String |
| Build materials + instances | ✅ | `MaterialTools`, `MaterialInstanceTools` — Phase 8 orange tint |
| Create DataTables and fill rows | ✅ | `DataTableTools.create` / `set_rows` |
| Import a web mesh (FBX/OBJ) | ✅ | `StaticMeshTools.import_file` + Kenney scaler script (Phase 8 H2) |
| Inspect mesh size, LODs, materials | ✅ | `get_bounds`, `get_triangle_count`, `get_material_slots` |
| Create string tables, curve tables | ✅ | `StringTableTools`, `CurveTableTools` |
| Create Primary Data Assets | 🔶 | Works via **Blueprint subclass** of `PrimaryDataAsset` (abstract bases won't save) |
| Run a short Python glue script in UE | ✅ | `ProgrammaticToolset.execute_tool_script` |
| List / read Epic agent skills | ✅ | `AgentSkillToolset.ListSkills` |
| Play In Editor from MCP | ❓ | `StartPIE` / `StopPIE` exist in `EditorAppToolset` — **not run** in our tests (user pressed Play for H1) |
| Import glTF/GLB meshes | ❌ | `FbxFactory` accepts **FBX and OBJ only** |
| Build or replace Landscape from heightmap | ❌ | No Landscape toolset in `list_toolsets` during our tests |
| Restart or launch the editor | ❌ | **No MCP tool**; agent `Start-Process` launch **crashed during startup** (2026-06-21) — open `.uproject` yourself |

---

## Verified workflows (multi-step)

These are the **real** things we proved, not just single tool calls.

### Scene basics (Phase 3)
Spawn cube → focus viewport → remove actor. Screenshots in `Docs/images/phase3-*`.

### Full content + logic chain (Phase 8 H1)
Material function → parent material → material instance → DataTable (3 string rows) → Actor Blueprint with cube mesh → `write_graph_dsl` (BeginPlay: read DataTable column → ForEach → Print String) → spawn in `L_Grok` → **user PIE** confirmed all three strings in Output Log.

### Web mesh import (Phase 8 H2)
Download Kenney CC0 OBJ → `ImportedAssets/scripts/scale_obj_to_ue_cm.py --kenney-ue --target-max-cm N` → `import_file` → assign `M_GrokPhase8_Inst` → spawn at **scale 1, rotation 0**. Bench **90 cm**, bear **60 cm**, correct Z-up, forward, normals. Final shot: `Docs/images/phase8-h2-kenney-imports-final.jpg`.

### Blueprint + assets in `/Game/MCPTest/` (Phase 7)
Create Blueprint → compile → set CDO properties → spawn actor from Blueprint asset. Move assets with `AssetTools.move`. Primary Data Asset via Blueprint `_C` class reference.

---

## 20 MCP toolsets at a glance

Epic ships **19** toolsets; this project adds **`GrokProjectTools`** (20 total when the custom plugin is enabled). Count was **19** before `GrokUEMCPTools` was enabled.

**Per-tool coverage is uneven.** Example: `MaterialTools` has ~22 tools — we verified `create_material` and expression wiring in Phase 8, not every graph editor. `SkeletalMeshTools` lists ~20 tools — we cataloged names only. Treat “Our testing” as **toolset-level**, not every function inside it.

| Toolset | What it's for | Our testing |
|---------|---------------|-------------|
| **Meta** (`list_toolsets`, `describe_toolset`, `call_tool`) | Discovery and invocation | ✅ Phase 3 |
| **SceneTools** | Level, actors, spawn, remove, folders | ✅ Read + write |
| **EditorAppToolset** | Selection, camera, viewport, content browser, PIE state | ✅ Read; viewport capture with quirks |
| **LogsToolset** | Output Log categories and entries | ✅ |
| **ActorTools** | Transforms, labels, components, bounds | ✅ |
| **AssetTools** | Find, move, duplicate, delete, save, metadata | ✅ `save_assets` critical after creates |
| **ObjectTools** | Property get/set, subclass search | ✅ |
| **BlueprintTools** | Create, compile, graphs, **DSL read/write** | ✅ Write + Phase 8 logic |
| **PrimitiveTools** | Add cube/sphere/cylinder/cone to actor | ✅ Phase 8 `add_cube` |
| **StaticMeshTools** | LOD, bounds, materials, collision, **`import_file`** | ✅ Read + import (FBX/OBJ) |
| **MaterialTools** | Create materials, expression graph | ✅ Phase 8 |
| **MaterialInstanceTools** | MI create, parameters | ✅ Phase 8 |
| **TextureTools** | Size, import | 🔶 `get_size` verified |
| **DataTableTools** | Create, schema, rows | ✅ Read + write |
| **DataAssetTools** | Create data assets | 🔶 Abstract-type hitch |
| **StringTableTools** | Localized string tables | ✅ |
| **CurveTableTools** | Curve tables + keys | ✅ |
| **SkeletalMeshTools** | Rigged meshes, bones, sockets | 📋 No test SK in project |
| **AgentSkillToolset** | List/read/create skills | ✅ List/read |
| **ProgrammaticToolset** | Sandboxed Python batching other tools | ✅ |
| **GrokProjectTools** (custom) | `health_check`, `get_session_info` | ✅ |

---

## Important quirks (read before you prompt)

| Topic | What we learned |
|-------|-----------------|
| **One call at a time** | Epic serializes on the game thread — parallel MCP calls can deadlock |
| **Save after create** | `BlueprintTools.create`, materials, etc. need `AssetTools.save_assets` or they vanish |
| **`find_actors` filter** | Pass `{"name":"","tag":"","collision_channels":[]}` — empty `{}` is rejected |
| **Kenney / web meshes** | Import tiny at scale 1; use `--kenney-ue` scaler for size + axes + normals |
| **FBX vs OBJ** | Same Kenney asset can differ in scale between formats |
| **DataAsset abstract types** | Use Blueprint subclass + `_C` refPath for `PrimaryDataAsset` |
| **Blueprint DSL** | Struct fields like `.mirroredName` not in expressions — use `GetDataTableColumnasString` |
| **CaptureViewport** | Needs explicit `captureTransform` + `annotations` — not `{}` |
| **Editor restart** | Invalidates MCP sessions → Grok `/mcps` → **`r`**; needed after plugin/Python changes |
| **Editor launch via agent** | ❌ Tested 2026-06-21: `Stop-Process` + `Start-Process` on `.uproject` — editor died during load; **manual open only** |
| **Level spawns in git** | `Content/__ExternalActors__/` is gitignored — save locally |

---

## What you still do manually

- **Open the editor yourself** — double-click `GrokUE_MCP.uproject` or Epic Launcher (agent shell launch is unreliable here)
- Keep it running while using MCP (port **8000**)
- **Close and reopen** the editor after plugin / `init_unreal.py` changes (no working MCP or agent restart path)
- Re-handshake MCP after restart (`/mcps` → `r`)
- Confirm results in viewport / Outliner
- Save the level (**Ctrl+S**)
- Press **Play** for PIE (unless we add `StartPIE` tests later)

---

## Known gaps and future ideas (not exhaustive)

These are **examples** of things we did not verify. Many other tools in the table above were also never called — run `describe_toolset` to see the full set for your editor session.

| Area | Notes |
|------|--------|
| **Undiscovered tools** | Any tool Epic adds after our test date, or any tool we never invoked, is simply **not listed here** |
| `StartPIE` / `StopPIE` | Present in `EditorAppToolset`; not run in Phase 8 (user PIE for H1) |
| **Most `MaterialTools` graph editors** | Cataloged; only Phase 8 expression path exercised |
| **`SkeletalMeshTools`** | ~20 tools cataloged; no rigged asset in blank project |
| **`TextureTools.import_file`** | Cataloged; read probe on engine texture only |
| **SceneTools** merge / level instance / trace | Many write tools cataloged, not all probed |
| glTF / GLB import | ❌ Rejected by `import_file` |
| Landscape / terrain | No toolset observed |
| Headless MCP (`-ModelContextProtocolStartServer`) | Not explored |
| Agent-driven editor open/restart | ❌ Tested; crashes on load — use human launch |
| `GrokProjectTools.import_mesh_sized` | Possible wrapper around scaler + `import_file` |

---

## Where to go deeper

| Doc | Use when |
|-----|----------|
| [PHASE8_PROGRESS.md](PHASE8_PROGRESS.md) | Latest checkpoint + Kenney recipe |
| [NOTES.md](NOTES.md) | Full batch results, handoff, all screenshots |
| [PHASE7_PROGRESS.md](PHASE7_PROGRESS.md) | Per-toolset probe archive |
| [PLAN.md](PLAN.md) | Original setup phases, hitch template |
| [AGENTS.md](../AGENTS.md) | Rules for AI agents in this repo |