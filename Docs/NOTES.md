# GrokUE_MCP — Integration Notes

**Last updated:** 2026-06-20  
**Current phase:** Phase 7 in progress — expanding toolset coverage. Phases 0–6 pass. **Resume:** `Docs/PHASE7_PROGRESS.md`

This file records what we verified, what failed, and answers to open questions from [PLAN.md](PLAN.md). Update it as each phase completes.

---

## Handoff — new Grok session starts here

**You are picking up a finished integration.** The Grok ↔ Unreal MCP bridge is verified. Read this section first, then drive from `AGENTS.md` and the `/grok-ue-mcp` skill.

### 1. Confirm the session (30 seconds)

| Step | Action |
|------|--------|
| UE running? | `GrokUE_MCP.uproject` open; Output Log shows MCP on port **8000** |
| Grok from repo root? | `cd F:\git\GrokUE_MCP` → `grok` |
| MCP ready? | `/mcps` → `unreal-mcp` **[ready]** — press **`r`** after any editor restart |
| Health check | `call_tool` → `GrokProjectTools.health_check` → `GrokUE_MCP: custom toolset healthy` |

![Health check from a fresh Grok session](images/phase5-health-check-grok-session.jpg)

*Verified 2026-06-20: new Grok session → `GrokProjectTools.health_check` via `unreal-mcp`.*

### 2. What is already done (do not re-run unless regressing)

| Phase | Result |
|-------|--------|
| 0–2 | UE 5.8 + MCP + Grok connected |
| 3 | Batches A/B/C — meta-tools, scene read, spawn/focus/remove cube ([screenshots](images/)) |
| 4 | Daily startup/shutdown workflow adopted |
| 5 | `AGENTS.md`, `/grok-ue-mcp` skill, custom `GrokUEMCPTools` plugin (**20 toolsets**) |
| 6 | Cursor IDE re-confirmed Phase 3 results (no new capability; see Phase 6) |
| 7 | **In progress** — read-only probes on Logs, EditorApp, ActorTools (see Phase 7) |

### GrokProjectTools — what it is (no editor window)

There is **no Unreal Editor panel or menu** for GrokProjectTools. It is a **custom Python MCP toolset** registered at startup by `Plugins/GrokUEMCPTools/Content/Python/init_unreal.py`. Grok and Cursor reach it only through MCP:

```
call_tool(
  toolset_name: "grok_ue_mcp.toolsets.project_tools.GrokProjectTools",
  tool_name: "health_check",   # or get_session_info
  arguments: {}
)
```

| Tool | What it does |
|------|----------------|
| `health_check` | Returns `GrokUE_MCP: custom toolset healthy` — confirms the plugin loaded |
| `get_session_info` | Returns project name, project dir, content dir, current level path |

To add more project tools, edit `project_tools.py`, restart the editor, then `ModelContextProtocol.RefreshTools` and re-handshake MCP clients.

### 3. Where to work next

| Goal | Start here |
|------|------------|
| Daily Grok + UE work | `AGENTS.md` + `/grok-ue-mcp` |
| Add project MCP tools | `Plugins/GrokUEMCPTools/Content/Python/grok_ue_mcp/toolsets/project_tools.py` → editor restart → `ModelContextProtocol.RefreshTools` |
| Custom tool authoring rules | `@unreal.ustruct()` for struct returns — **not** `@dataclass` (see Phase 5 hitch below) |
| Gameplay / content | `Content/` (blank today) |
| CI / headless MCP | `Docs/PLAN.md` Phase 5 — `-ModelContextProtocolStartServer` (not started) |
| **Phase 7 — expand coverage** | **`Docs/PHASE7_PROGRESS.md`** — checkpoint after each probe; do not re-run completed batches |

### 4. Key repo paths

```
F:\git\GrokUE_MCP\
├── AGENTS.md                          # Agent conventions — read first
├── .grok/config.toml                  # unreal-mcp → http://127.0.0.1:8000/mcp
├── .grok/skills/grok-ue-mcp/          # /grok-ue-mcp skill
├── Plugins/GrokUEMCPTools/            # Custom Python MCP toolset
├── Docs/NOTES.md                      # This file — test results + handoff
└── Docs/PLAN.md                       # Full integration plan
```

### 5. If something breaks

1. `Saved/Logs/GrokUE_MCP.log` — search `LogPython: Error` or `LogModelContextProtocol`
2. Editor restart → re-handshake **all** MCP clients (`/mcps` → `r` in Grok; restart IDE Grok session too)
3. Log hitch in this file using template in `Docs/PLAN.md`

---

## Phase Summary

| Phase | Status | Date | Notes |
|-------|--------|------|-------|
| 0 — Environment verification | **Pass** | 2026-06-20 | UE 5.8 opens project; Grok runs from repo root |
| 1 — Enable Unreal MCP | **Pass** | 2026-06-20 | Plugin enabled; auto-start on port 8000 |
| 2 — Connect Grok | **Pass** | 2026-06-20 | `unreal-mcp` shows **ready** in `/mcps` |
| 3 — First connection tests | **Pass** | 2026-06-20 | Batches A/B/C verified — spawn, focus, remove `GrokTestCube` end-to-end |
| 4 — Repeatable workflow | **Pass** | 2026-06-20 | Daily startup/shutdown checklist adopted |
| 5 — Grow capabilities | **Pass** | 2026-06-20 | 20 toolsets; `health_check` live-verified from fresh Grok session |
| 6 — Multi-client regression | **Pass** | 2026-06-20 | Cursor IDE agent: read + write tests; `grok mcp doctor` healthy |
| 7 — Expand toolset coverage | **In progress** | 2026-06-20 | Batches F–U; `CaptureViewport` workaround; resume `PHASE7_PROGRESS.md` |

---

## Phase 7 — Expand Toolset Coverage (In Progress)

**Goal:** Document what Epic's 19 shipped toolsets can do in this blank project, so repo readers (Grok, Cursor, humans) know what is possible without re-probing.

**Workflow:** One MCP call at a time → record result in this section → update `Docs/PHASE7_PROGRESS.md` queue → commit incrementally.

### Batch F — EditorApp read-only (verified 2026-06-20)

| # | Tool | Result |
|---|------|--------|
| F1 | `GetCameraTransform` | **Pass** — viewport camera pose returned |
| F2 | `IsPIERunning` | **Pass** — `false` |
| F3 | `GetContentBrowserPath` | **Pass** — `/Game` |
| F4 | `GetVisibleActors` | **Pass** — 63 actors in viewport frustum (includes PlayerStart, Landscape, lights) |

### Batch G — LogsToolset read-only (verified 2026-06-20)

| # | Tool | Arguments | Result |
|---|------|-----------|--------|
| G1 | `GetLogCategories` | `filter: "ModelContextProtocol"` | **Pass** — `LogModelContextProtocol`, `LogModelContextProtocolToolHashMapping` |
| G2 | `GetLogEntries` | `category: LogModelContextProtocol`, `pattern: "Starting MCP server"`, `maxEntries: 5` | **Pass** — confirms port 8000 bind line |

**Quirk:** `GetLogEntries` schema marks `pattern` as required (use `""` to match all).

### Batch H — ActorTools read-only (verified 2026-06-20)

Test actor: `PlayerStart` — refPath `/Temp/Untitled_1.Untitled_1:PersistentLevel.PlayerStart_UAID_F02F74551BF5599B01_1153002503`

| # | Tool | Result |
|---|------|--------|
| H1 | `get_label` | **Pass** — `PlayerStart` |
| H2 | `get_actor_transform` | **Pass** — (-200, 0, 92), yaw 180° |
| H3 | `get_tags` | **Pass** — `[]` |
| H4 | `get_components` | **Pass** — CollisionCapsule, Sprite, Sprite2, Arrow |
| H5 | `get_actor_bounds` | **Pass** — valid world-space AABB |

### Batch I — Editor imaging read-only (verified 2026-06-20)

| # | Tool | Result |
|---|------|--------|
| I1 | `CaptureAssetImage` `/Engine/BasicShapes/Cube` | **Pass** — returns `image/png` base64 thumbnail (omit payload from docs) |

### Batch J — Editor utilities (verified 2026-06-20)

| # | Tool | Result |
|---|------|--------|
| J1 | `SearchCVars` `name: r.Shadow` | **Pass** — JSON string of matching cvars (`help` + `value`) |

### Batch K — AssetTools read-only (verified 2026-06-20)

**Tool catalog (21 tools):** `find_assets`, `list_folders`, `get_asset_class`, `get_plugin_content_paths`, `load_asset`, `exists`, `read_file`/`write_file`, `create_folder`, `move`, `duplicate`, `delete`, `save_assets`, metadata/registry helpers, dependency queries.

| # | Tool | Result |
|---|------|--------|
| K1 | `get_plugin_content_paths` | **Pass** — `["/GrokUEMCPTools/"]` |
| K2 | `list_folders` `/Game` | **Pass** — `/Game/Collections/`, `/Game/Developers/` (blank project) |
| K3 | `get_asset_class` `/Engine/BasicShapes/Cube` | **Pass** — `StaticMesh` |
| K4 | `find_assets` `folder_path: ""`, `name: ""` | **Pass** — 2000+ asset paths (engine/plugin content: Niagara, Water, PCG, etc.); not limited to `/Game`. Use `folder_path: "/Game"` to scope. |

### Batch L — ObjectTools read-only (verified 2026-06-20)

**Tool catalog (6 tools):** `search_subclasses`, `get_class`, `list_properties`, `get_properties`, `set_properties`, `reset_properties`.

| # | Tool | Result |
|---|------|--------|
| L1 | `search_subclasses` base `Actor`, filter `PlayerStart` | **Pass** — `PlayerStart`, `PlayerStartPIE` |
| L2 | `get_properties` PlayerStart, `properties: ["bHidden"]` | **Pass** — `{"bHidden": false}` (JSON string) |

### Batch M — BlueprintTools (verified 2026-06-20)

**Tool catalog (40+ tools):** graph DSL (`read_graph_dsl`/`write_graph_dsl`), node graph editing, variables, functions/events, `create`, `compile_blueprint`, etc. **No `/Game` Blueprint assets yet** — graph-level probes deferred.

| # | Tool | Result |
|---|------|--------|
| M1 | `get_graph_dsl_docs` | **Pass** — returns S-expression DSL grammar for `write_graph_dsl` |

### Batch N — CaptureViewport (2026-06-20)

| # | Tool | Result |
|---|------|--------|
| N1 | `CaptureViewport` `{}` or `{"bShowUI": false}` | **Fail** — `captureTransform` needs a default value (optional in schema; binding rejects empty args) |
| N2 | `CaptureViewport` with `captureTransform` from `GetCameraTransform` only | **Fail** — `annotations` also needs a default value |
| N3 | `CaptureViewport` with `captureTransform` + minimal `annotations` + `bShowUI: false` | **Pass** — returns `image/png` base64 viewport capture (omit payload from docs) |

**Workaround:** Call `GetCameraTransform` first, then pass both `captureTransform` and `annotations` explicitly. Minimal annotations that work: `gridSpacing: 0`, `gridExtent: 0`, `gridHeight: 0`, `maxLabelDistance: 0`, `classFilter: null`, `maxLabels: 0`.

### Batch O — ProgrammaticToolset (verified 2026-06-20)

| # | Tool | Result |
|---|------|--------|
| O1 | `get_execution_environment` | **Pass** — Python sandbox; `execute_tool()`; modules: json, math, re, time, datetime, copy |
| O2 | `execute_tool_script` batch `health_check` + `get_current_level` | **Pass** — single round-trip returns both values |

### Batch P — PrimitiveTools (catalog 2026-06-20)

**Tool catalog (4 tools, all write):** `add_cube`, `add_sphere`, `add_cylinder`, `add_cone` — attach engine basic-shape StaticMeshComponents to an actor. No read-only probes; write tests deferred.

### Batch Q — StaticMeshTools (verified 2026-06-20)

**Tool catalog (16 tools):** LOD queries/edits, Nanite toggle, collision gen/remove, material slots, bounds, `import_file`.

| # | Tool | Result |
|---|------|--------|
| Q1 | `get_lod_count` mesh `/Engine/BasicShapes/Cube.Cube` | **Pass** — `1` LOD |
| Q2 | `is_nanite_enabled` Engine Cube | **Pass** — `false` |
| Q3 | `get_bounds` Engine Cube | **Pass** — min (-50,-50,-50), max (50,50,50), `isValid: true` |
| Q4 | `get_material_slots` Engine Cube | **Pass** — `["WorldGridMaterial"]` |

**Note:** Static mesh `mesh.refPath` must include asset name (e.g. `.Cube`), not folder path alone.

### Batch R — MaterialTools (catalog 2026-06-20)

**Tool catalog (22 tools):** material/function/MPC creation, expression graph editing (add/delete/connect/layout), parameter groups, `recompile`, `get_referencing_materials`. All graph probes need a `/Game` Material asset — deferred.

### Batch S — TextureTools (catalog 2026-06-20)

**Tool catalog (2 tools):** `get_size` (read), `import_file` (write). Read probe deferred.

### Batch T — DataTableTools (catalog 2026-06-20)

**Tool catalog (10 tools):** `search_row_structs`, `create`, `import_file`, `get_schema`, `list_rows`, `add_rows`, `remove_rows`, `rename_rows`, `get_rows`, `set_rows`. No `/Game` DataTable yet — deferred.

### Batch U — AgentSkillToolset (verified 2026-06-20)

**Tool catalog (4 tools):** `ListSkills`, `GetSkills`, `CreateSkill`, `UpdateSkill`.

| # | Tool | Result |
|---|------|--------|
| U1 | `ListSkills` | **Pass** — 4 built-in EditorToolset Python skills (BlueprintBasics, DefaultOutdoorLighting, MaterialBasics, UnrealSkillBestPractices) |

**Next in queue:** see `Docs/PHASE7_PROGRESS.md`.

---

## Phase 6 — Cursor IDE Re-confirmation

**Goal:** Confirm Cursor IDE agents can drive the same MCP bridge as Grok TUI. This re-ran Phase 3 Batches B/C plus `get_session_info` — **no new tools or workflows** beyond what Phases 2–5 already verified.

**Client:** Cursor Composer with `unreal-mcp` at `http://127.0.0.1:8000/mcp`.  
**Outcome:** All pass. User confirmed cube spawn/focus/remove in viewport. Existing Phase 3 screenshots remain the visual reference.

### Session startup (Cursor)

| Step | Action |
|------|--------|
| 1 | Open `GrokUE_MCP.uproject` — confirm Output Log → `Starting MCP server on port 8000` |
| 2 | Open this repo in Cursor — ensure `unreal-mcp` MCP server is configured |
| 3 | After editor restart → restart Cursor Grok session (session IDs invalidate) |
| 4 | Health check → `GrokProjectTools.health_check` |

### Batch D — Read-only (verified 2026-06-20)

| # | Tool | Arguments | Pass criteria | Result |
|---|------|-----------|---------------|--------|
| D1 | `list_toolsets` | `{}` | 20 toolsets including `GrokProjectTools` | **Pass** |
| D2 | `GrokProjectTools.health_check` | `{}` | `GrokUE_MCP: custom toolset healthy` | **Pass** |
| D3 | `GrokProjectTools.get_session_info` | `{}` | Project name, dirs, level path | **Pass** — `GrokUE_MCP`, `F:/Git/GrokUE_MCP/`, `/Temp/Untitled_1` |
| D4 | `describe_toolset` | `GrokProjectTools` | 2 tools with JSON schemas | **Pass** — `health_check`, `get_session_info` |
| D5 | `SceneTools.get_current_level` | `{}` | Level asset path | **Pass** — `/Temp/Untitled_1` |
| D6 | `SceneTools.find_actors` | `name/tag/collision_channels` empty filter | Actor list (default level) | **Pass** — 131 actors; `PlayerStart`, `DirectionalLight`, `Landscape`, etc. |
| D7 | `EditorAppToolset.GetSelectedActors` | `{}` | Array (may be empty) | **Pass** — `[]` |

### Batch E — Light write regression (verified 2026-06-20)

Re-ran Phase 3 Batch C end-to-end from Cursor. Verify in UE viewport/Outliner after C1.

| # | Tool | Arguments | Pass criteria | Result |
|---|------|-----------|---------------|--------|
| E1 | `SceneTools.add_to_scene_from_asset` | `/Engine/BasicShapes/Cube`, `GrokTestCube`, origin | Returns `refPath`; cube in Outliner | **Pass** — `StaticMeshActor_UAID_D8BBC1098290B8E602_1152976759` |
| E2 | `EditorAppToolset.FocusOnActors` | actor `refPath` from E1 | Camera frames cube | **Pass** — `null` return (void tool) |
| E3 | `SceneTools.remove_from_scene` | actor `refPath` from E1 | `true`; actor gone | **Pass** — `find_actors` name filter `GrokTestCube` → `[]` |

### CLI health (verified 2026-06-20)

```powershell
cd F:\git\GrokUE_MCP
grok mcp doctor unreal-mcp
```

**Result:** `Found 1 healthy, 0 failing` — handshake OK, 3 meta-tools discovered.

### Takeaway for repo readers

| Client | How to connect | Verified |
|--------|----------------|----------|
| Grok TUI | `grok` from repo root → `/mcps` → `unreal-mcp` | Phases 2–5 |
| Cursor IDE | MCP server config → `unreal-mcp` at `http://127.0.0.1:8000/mcp` | Phase 6 |
| MCP Inspector | `npx @modelcontextprotocol/inspector` | Phase 1 (optional) |

Both Grok TUI and Cursor use the same 3 meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`) and the same 20 toolsets. **One MCP call at a time** applies to all clients.

---

## Phase 2 — Grok Connected (Verified)

Grok sees the project-scoped MCP server and reports it as ready.

![Grok /mcps showing unreal-mcp ready](images/phase2-mcps-ready.jpg)

*Grok TUI → `/mcps` → Local (1) → `unreal-mcp [ready]`*

### Config in use

- **Project config:** `.grok/config.toml` → `http://127.0.0.1:8000/mcp`
- **UE plugins enabled in `.uproject`:** `ModelContextProtocol`, `MCPClientToolset`, `EditorToolset`

### UE Output Log confirmation

From `Saved/Logs/GrokUE_MCP.log`:

```
LogModelContextProtocol: Tool search enabled: registered 3 meta-tools (1 toolsets discoverable via list_toolsets)
LogModelContextProtocol: Starting MCP server on port 8000
LogModelContextProtocol: Session initialized: ...
LogModelContextProtocol: Running tool: 'list_toolsets'
```

**Startup order used:** Unreal Editor first → Grok second. Matches the plan.

---

## Phase 3 — Test Plan

Tests are ordered **read-only first**, then light writes. Issue **one tool call at a time** — Epic serializes on the game thread.

### Batch A — Connectivity (verified)

These work with only the base MCP + Toolset Registry stack. Verified via Grok session and UE Output Log.

![Batch A — MCP meta-tools invoked from Grok](images/phase3-batch-a-meta-tools.png)

*UE Output Log (`LogModelContextProtocol`) showing `list_toolsets`, `describe_toolset`, and `call_tool` → `ListSkills` executed successfully.*

| # | Prompt to Grok | MCP path | Pass criteria | Result |
|---|----------------|----------|---------------|--------|
| A1 | "What MCP tools do you have from the unreal-mcp server?" | — | Lists 3 meta-tools: `list_toolsets`, `describe_toolset`, `call_tool` | **Pass** |
| A2 | "Use the Unreal MCP to list available toolsets." | `list_toolsets` | Returns at least one toolset name + description | **Pass** — `ToolsetRegistry.AgentSkillToolset` (pre-restart) |
| A3 | "Describe the AgentSkill toolset." | `describe_toolset` | Returns tool names + input schemas | **Pass** — 4 tools (`ListSkills`, `GetSkills`, `CreateSkill`, `UpdateSkill`) |
| A4 | "List all AgentSkills in this project." | `call_tool` → `ListSkills` | Returns `{}` (empty project) or a skill map | **Pass** — `{"returnValue": {}}` |

### Editor restart — EditorToolset loaded (verified)

After enabling `EditorToolset` in `.uproject` and restarting the editor, the MCP server re-registered toolsets progressively as Python modules loaded.

![Editor restart — toolsets registering in Output Log](images/phase3-editor-restart-toolsets.png)

*Log shows count climbing from 1 → **19 toolsets discoverable via list_toolsets**.*

**Registered toolsets** (from `Saved/Logs/GrokUE_MCP.log`, 2026-06-21):

| # | Toolset | Category |
|---|---------|----------|
| 1 | `ToolsetRegistry.AgentSkillToolset` | Skills |
| 2 | `EditorToolset.EditorAppToolset` | Editor / viewport |
| 3 | `EditorToolset.LogsToolset` | Logs |
| 4 | `editor_toolset.toolsets.actor.ActorTools` | Actors |
| 5 | `editor_toolset.toolsets.asset.AssetTools` | Assets |
| 6 | `editor_toolset.toolsets.blueprint.BlueprintTools` | Blueprints |
| 7 | `editor_toolset.toolsets.curve_table.CurveTableTools` | Data |
| 8 | `editor_toolset.toolsets.data_asset.DataAssetTools` | Data |
| 9 | `editor_toolset.toolsets.data_table.DataTableTools` | Data |
| 10 | `editor_toolset.toolsets.material.MaterialTools` | Materials |
| 11 | `editor_toolset.toolsets.material_instance.MaterialInstanceTools` | Materials |
| 12 | `editor_toolset.toolsets.object.ObjectTools` | Objects |
| 13 | `editor_toolset.toolsets.primitive.PrimitiveTools` | Primitives |
| 14 | `editor_toolset.toolsets.scene.SceneTools` | **Scene / actors** |
| 15 | `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools` | Meshes |
| 16 | `editor_toolset.toolsets.static_mesh.StaticMeshTools` | Meshes |
| 17 | `editor_toolset.toolsets.string_table.StringTableTools` | Localization |
| 18 | `editor_toolset.toolsets.programmatic.ProgrammaticToolset` | Scripting |
| 19 | `editor_toolset.toolsets.texture.TextureTools` | Textures |

**Prerequisite for Batch B:** met. After any editor restart, press `r` in Grok `/mcps` to re-handshake (stale sessions return `Unknown session id`).

### Batch B — Scene inspection (verified)

| # | Prompt to Grok | Expected toolset / tool | Pass criteria | Result |
|---|----------------|-------------------------|---------------|--------|
| B1 | "List all MCP toolsets again — how many are there now?" | `list_toolsets` | ~19 toolsets including `SceneTools`, `ActorTools`, `PrimitiveTools` | **Pass** — 19 toolsets |
| B2 | "What actors are in the current level?" | `SceneTools.find_actors` | Returns actor labels (PlayerStart, floor, lighting, etc.) | **Pass** — 131 actors; key labels include `PlayerStart`, `DirectionalLight`, `SkyLight`, `StaticMeshActor`, `Landscape` |
| B3 | "What is the path of the currently loaded level?" | `SceneTools.get_current_level` | Returns level asset path | **Pass** — `/Temp/Untitled_1` (default untitled level) |

**B2 call shape:** `find_actors` rejects `{}`; pass `{"name": "", "tag": "", "collision_channels": []}` to list all actors.

### Batch C — Light write (verified)

Run only after Batch B passes. Verify in the UE viewport after each step.

![C1 — GrokTestCube spawned at world origin](images/phase3-c1-groktestcube-spawned.jpg)

*Outliner shows `GrokTestCube` (StaticMeshActor); cube selected at origin with transform gizmo. Status bar: 139 actors (1 selected).*

| # | Prompt to Grok | Expected toolset / tool | Pass criteria | Result |
|---|----------------|-------------------------|---------------|--------|
| C1 | "Spawn a static mesh cube at the world origin named GrokTestCube." | `SceneTools.add_to_scene_from_asset` with `/Engine/BasicShapes/Cube` | Cube visible at (0,0,0) in outliner/viewport | **Pass** — cube in outliner + viewport (screenshot above) |
| C2 | "Focus the viewport on GrokTestCube." | `EditorAppToolset.FocusOnActors` (via programmatic or direct call) | Camera frames the new actor | **Pass** — camera reframed on cube (screenshot below) |
| C3 | "Remove GrokTestCube from the scene." | `SceneTools.remove_from_scene` | Actor gone from level | **Pass** — cube removed from outliner/viewport (screenshot below) |

![C2 — Viewport focused on GrokTestCube](images/phase3-c2-focus-on-groktestcube.jpg)

*Camera zoomed to cube at origin; `GrokTestCube` selected in Outliner. Status bar: 139 actors (1 selected).*

![C3 — GrokTestCube removed from level](images/phase3-c3-groktestcube-removed.jpg)

*No cube in viewport; `GrokTestCube` absent from Outliner. Level back to default actors (PlayerStart, Landscape, Lighting).*

### Suggested session flow

1. Open `GrokUE_MCP.uproject` → confirm MCP auto-started (Output Log).
2. Run Batch A prompts in Grok (health check).
3. If Batch A passes, run Batch B.
4. If B2 returns actors, run C1 → verify in editor → C2 → C3 (cleanup).

---

## Phase 4 — Repeatable Workflow (Adopted)

Canonical reference: [PLAN.md § Phase 4](PLAN.md#phase-4--establish-a-repeatable-workflow).

### Session startup (do this every time)

| Step | Action | Notes |
|------|--------|-------|
| 1 | Open `GrokUE_MCP.uproject` | UE 5.8 editor |
| 2 | Confirm MCP auto-started | Output Log → `Starting MCP server on port 8000` |
| 3 | `cd F:\git\GrokUE_MCP` | Repo root (canonical path) |
| 4 | Run `grok` | Project-scoped `.grok/config.toml` loads `unreal-mcp` |
| 5 | `/mcps` → verify `unreal-mcp` **ready** | After editor restart: press **`r`** to re-handshake |
| 6 | Health check (read-only) | Prompt: *"What MCP tools do you have from the unreal-mcp server?"* — expect 3 meta-tools; or call `list_toolsets` → expect **20 toolsets** (19 shipped + `GrokProjectTools`) |

**Health check verified (2026-06-20):** `list_toolsets` returned 19 shipped toolsets. After `GrokUEMCPTools` plugin loads, expect **20** including `grok_ue_mcp.toolsets.project_tools.GrokProjectTools`.

**Startup order:** Unreal Editor first → Grok second.

### Session shutdown

1. Close Grok normally.
2. Save and close Unreal Editor (MCP server stops with the editor).

### Quick health prompts (read-only)

Use these anytime to confirm the bridge without modifying the level:

| Prompt | Expected |
|--------|----------|
| "What MCP tools do you have from the unreal-mcp server?" | `list_toolsets`, `describe_toolset`, `call_tool` |
| "Use the Unreal MCP to list available toolsets." | 20 toolsets (with custom plugin) |
| `GrokProjectTools.health_check` | `GrokUE_MCP: custom toolset healthy` |
| "What is the path of the currently loaded level?" | Level asset path (e.g. `/Temp/Untitled_1`) |

Full write tests (spawn/focus/remove) live in Phase 3 Batch C — run only when you need to re-verify editor manipulation.

### Optional — in-editor Terminal

Not required for daily use. See PLAN.md § 4.3 if you want Grok inside the UE Terminal plugin (single-window workflow).

### Constraints (carry forward)

- **One MCP tool call at a time** — Epic serializes on the game thread.
- **`find_actors`** requires `{"name": "", "tag": "", "collision_channels": []}` (empty `{}` fails).
- **Editor restart** invalidates MCP session IDs → `/mcps` → `r` in Grok.

---

## Phase 5 — Grow Capabilities (In Progress)

| Milestone | Status | Location |
|-----------|--------|----------|
| **AGENTS.md** | Done | Repo root — agent conventions for Grok + UE MCP |
| **Grok skill** | Done | `.grok/skills/grok-ue-mcp/` — invoke via `/grok-ue-mcp` |
| **Custom Python toolset** | **Pass** | `Plugins/GrokUEMCPTools/` — registered after `ustruct` fix + editor restart (screenshot below) |
| **CI / headless** | Not started | `-ModelContextProtocolStartServer` CLI flag (advanced) |

### Custom plugin: GrokUEMCPTools

Enabled in `GrokUE_MCP.uproject`. Python entry: `Plugins/GrokUEMCPTools/Content/Python/init_unreal.py`.

**Toolset:** `grok_ue_mcp.toolsets.project_tools.GrokProjectTools`

| Tool | Purpose |
|------|---------|
| `health_check` | Confirms project toolset is registered |
| `get_session_info` | Returns project name, dirs, current level path |

### Verify after editor restart (required)

New plugins need a full editor restart (not just `RefreshTools` on first enable):

1. Restart Unreal Editor (or close/reopen `GrokUE_MCP.uproject`).
2. Output Log → look for `Registering Toolset grok_ue_mcp.toolsets.project_tools.GrokProjectTools`.
3. Re-handshake **every** MCP client connected to UE (editor restart invalidates session IDs):
   - Grok TUI → `/mcps` → **`r`**
   - Cursor / other IDE agents → restart Grok session or reconnect `unreal-mcp`
4. `list_toolsets` → **20** toolsets.
5. `call_tool` → `GrokProjectTools.health_check` → `GrokUE_MCP: custom toolset healthy`.

![Phase 5 — custom toolset registered in Output Log](images/phase5-custom-toolset-registered.jpg)

*Output Log after successful reload: `Registering Toolset grok_ue_mcp.toolsets.project_tools.GrokProjectTools` among 20 toolsets. No `LogPython: Error` from `init_unreal.py`.*

**Verified (2026-06-20):** Log confirms registration; fresh Grok session `health_check` returned `GrokUE_MCP: custom toolset healthy` (screenshot above).

If the toolset is missing after restart, run `ModelContextProtocol.RefreshTools` in the UE console and re-handshake all MCP clients.

**If `init_unreal.py` failed on startup** (Python traceback in Output Log), fix the `.py` files and **restart the editor** — `RefreshTools` does not re-run `init_unreal.py`.

### Hitch: custom toolset failed to register (2026-06-20)

**Symptom:** Plugin mounts (`LogPluginManager: Mounting Project plugin GrokUEMCPTools`) but toolset never appears; `list_toolsets` stays at 19.

**Log (`Saved/Logs/GrokUE_MCP.log`):**

```
LogPython: Error: Failed to create return property (GrokSessionInfo) for function 'get_session_info'
Exception: generate_class: Failed to generate an Unreal class for the Python type 'GrokProjectTools'
```

**Cause:** `get_session_info` returned a plain Python `@dataclass`. MCP tool return types must be **`@unreal.ustruct()`** classes extending `unreal.StructBase` with `unreal.uproperty()` fields — not stdlib `dataclasses`.

**Fix:** Rewrote `GrokSessionInfo` as `@unreal.ustruct()`; populate via `info = GrokSessionInfo(); info.project_name = ...`.

**Authoring rule for future tools:** See Epic's `toolset_registry/tests/demo_toolset.py` in the UE 5.8 install for the canonical `ustruct` / `tool_call` pattern.

---

## Findings & Open Questions

| # | Question | Answer so far |
|---|----------|-------------|
| 1 | Does Unreal MCP enable cleanly on UE 5.8? | **Yes** — plugin enables; server binds port 8000 |
| 2 | Port 8000 conflict? | **No** — server started without bind errors |
| 3 | Does Grok `search_tool` / `use_tool` work with Epic meta-tools? | **Yes** — `list_toolsets`, `describe_toolset`, `call_tool` invoked successfully from Grok session |
| 4 | Firewall blocking localhost? | **No evidence** — HTTP handshake and tool calls succeed |
| 5 | Canonical project path? | **`F:\git\GrokUE_MCP`** (working copy for this integration test) |

### Discovery: toolsets are plugin-scoped

**Before EditorToolset** — only one toolset registered:

```
LogModelContextProtocol: ... (1 toolsets discoverable via list_toolsets)
LogToolsetRegistry: Registering Toolset ToolsetRegistry.AgentSkillToolset
```

**After EditorToolset + restart** — nineteen toolsets, including scene/actor/primitive tools. Registration is staggered: MCP server starts early (1 toolset), then Python toolsets load as `init_unreal.py` runs (~4 s after startup).

`MCPClientToolset` is a different plugin — an adapter for connecting *outbound* to external MCP servers, not the source of scene tools.

### Session hygiene after editor restart

Editor restarts invalidate MCP session IDs. If Grok reports `Unknown session id`, press `r` in `/mcps` or restart the Grok session. UE will log a new `Session initialized: <id>` line.

---

## Hitch Reports

| Date | Issue | Resolution |
|------|-------|------------|
| 2026-06-20 | `CaptureViewport` — `{}` rejected; optional `captureTransform` and `annotations` lack binding defaults | Pass both explicitly from `GetCameraTransform` + minimal annotations; see Batch N |
| 2026-06-20 | `GrokProjectTools` — dataclass return type broke `@unreal.uclass()` generation | Use `@unreal.ustruct()`; restart editor after fix |

Use the template in [PLAN.md](PLAN.md) for additional failures.

---

## Changelog (this file)

| Date | Change |
|------|--------|
| 2026-06-20 | Phase 7 — StaticMesh read probes, CaptureViewport workaround, Material/Texture/DataTable/AgentSkill catalogs |
| 2026-06-20 | Phase 7 — Batches J–O (Asset/Object/Blueprint/Programmatic); `CaptureViewport` hitch |
| 2026-06-20 | **Phase 7 started** — `PHASE7_PROGRESS.md` checkpoint; Batches F–I; GrokProjectTools FAQ in handoff |
| 2026-06-20 | **Phase 6 pass** — Cursor IDE regression (Batches D/E); `get_session_info` verified; multi-client table |
| 2026-06-20 | Handoff section + `health_check` Grok session screenshot; integration marked complete |
| 2026-06-20 | Phase 5 custom toolset **pass** — screenshot + log confirm 20 toolsets after ustruct fix |
| 2026-06-20 | Hitch fix — `GrokSessionInfo` must be `@unreal.ustruct()`, not `@dataclass`; documented in Phase 5 |
| 2026-06-20 | Phase 5 started — `AGENTS.md`, `/grok-ue-mcp` skill, `GrokUEMCPTools` plugin scaffolded |
| 2026-06-20 | **Phase 4 pass** — adopted startup/shutdown checklist; health check verified (19 toolsets) |
| 2026-06-20 | **Phase 3 complete** — Batch C pass; C3 screenshot (`phase3-c3-groktestcube-removed.jpg`); Phase 4 ready |
| 2026-06-20 | C2 pass + screenshot (`phase3-c2-focus-on-groktestcube.jpg`); C3 `remove_from_scene` returned true |
| 2026-06-20 | C1 pass + screenshot (`phase3-c1-groktestcube-spawned.jpg`); C2 `FocusOnActors` invoked |
| 2026-06-20 | Batch B pass (B2/B3); C1 `GrokTestCube` spawned via MCP; documented `find_actors` empty-arg quirk |
| 2026-06-20 | Batch B1 pass — `list_toolsets` returns 19 toolsets (SceneTools, ActorTools, PrimitiveTools confirmed) |
| 2026-06-20 | Batch A screenshot + restart log screenshot; confirmed 19 toolsets after EditorToolset reload |
| 2026-06-20 | Created NOTES.md; documented Phase 2 pass + Phase 3 Batch A results; added EditorToolset to `.uproject`; screenshot added |