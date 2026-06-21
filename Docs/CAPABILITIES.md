# What Grok + Unreal MCP can do

Human-readable summary of **what we tested** in this repo (Phases 0–8, June 2026). For step-by-step history and screenshots, see [NOTES.md](NOTES.md). For tool argument details, see [.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md](../.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md).

**Legend:** ✅ verified end-to-end · 🔶 probed / partial · 📋 cataloged only · ❌ failed or not available

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
| Play In Editor from MCP | 📋 | Tools exist; **not automated** in our tests — user pressed Play |
| Import glTF/GLB meshes | ❌ | `FbxFactory` accepts **FBX and OBJ only** |
| Build or replace Landscape from heightmap | ❌ | No Landscape toolset in MCP |
| Restart the editor from MCP | 📋 | **Not tested** — human restart still required today |

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

Epic ships **19** toolsets; this project adds **`GrokProjectTools`** (20 total).

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
| **Level spawns in git** | `Content/__ExternalActors__/` is gitignored — save locally |

---

## What you still do manually

- Open the editor and keep it running (MCP on port **8000**)
- Restart editor after plugin / `init_unreal.py` changes
- Re-handshake MCP after restart (`/mcps` → `r`)
- Confirm results in viewport / Outliner
- Save the level (**Ctrl+S**)
- Press **Play** for PIE (unless we add `StartPIE` tests later)

---

## Not tested / future ideas

- `StartPIE` / `StopPIE` via MCP
- `SkeletalMeshTools` with a real rigged FBX
- glTF import path (or offline convert → OBJ)
- Real-world DEM → heightmap → Landscape
- Headless MCP (`-ModelContextProtocolStartServer`) for CI
- MCP-driven editor restart
- Custom `GrokProjectTools.import_mesh_sized` wrapping the scaler + `import_file`

---

## Where to go deeper

| Doc | Use when |
|-----|----------|
| [PHASE8_PROGRESS.md](PHASE8_PROGRESS.md) | Latest checkpoint + Kenney recipe |
| [NOTES.md](NOTES.md) | Full batch results, handoff, all screenshots |
| [PHASE7_PROGRESS.md](PHASE7_PROGRESS.md) | Per-toolset probe archive |
| [PLAN.md](PLAN.md) | Original setup phases, hitch template |
| [AGENTS.md](../AGENTS.md) | Rules for AI agents in this repo |