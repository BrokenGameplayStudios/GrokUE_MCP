# GrokUE_MCP — Integration Notes

**Last updated:** 2026-06-20  
**Current phase:** 4 — Repeatable workflow (Phase 3 complete)

This file records what we verified, what failed, and answers to open questions from [PLAN.md](PLAN.md). Update it as each phase completes.

---

## Phase Summary

| Phase | Status | Date | Notes |
|-------|--------|------|-------|
| 0 — Environment verification | **Pass** | 2026-06-20 | UE 5.8 opens project; Grok runs from repo root |
| 1 — Enable Unreal MCP | **Pass** | 2026-06-20 | Plugin enabled; auto-start on port 8000 |
| 2 — Connect Grok | **Pass** | 2026-06-20 | `unreal-mcp` shows **ready** in `/mcps` |
| 3 — First connection tests | **Pass** | 2026-06-20 | Batches A/B/C verified — spawn, focus, remove `GrokTestCube` end-to-end |
| 4 — Repeatable workflow | **Ready** | 2026-06-20 | Adopt Phase 4 session checklist from `PLAN.md` |
| 5 — Grow capabilities | Not started | — | — |

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

None filed yet. Use the template in [PLAN.md](PLAN.md) if a test fails.

---

## Changelog (this file)

| Date | Change |
|------|--------|
| 2026-06-20 | **Phase 3 complete** — Batch C pass; C3 screenshot (`phase3-c3-groktestcube-removed.jpg`); Phase 4 ready |
| 2026-06-20 | C2 pass + screenshot (`phase3-c2-focus-on-groktestcube.jpg`); C3 `remove_from_scene` returned true |
| 2026-06-20 | C1 pass + screenshot (`phase3-c1-groktestcube-spawned.jpg`); C2 `FocusOnActors` invoked |
| 2026-06-20 | Batch B pass (B2/B3); C1 `GrokTestCube` spawned via MCP; documented `find_actors` empty-arg quirk |
| 2026-06-20 | Batch B1 pass — `list_toolsets` returns 19 toolsets (SceneTools, ActorTools, PrimitiveTools confirmed) |
| 2026-06-20 | Batch A screenshot + restart log screenshot; confirmed 19 toolsets after EditorToolset reload |
| 2026-06-20 | Created NOTES.md; documented Phase 2 pass + Phase 3 Batch A results; added EditorToolset to `.uproject`; screenshot added |