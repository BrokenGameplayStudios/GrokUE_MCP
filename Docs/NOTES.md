# GrokUE_MCP — Integration Notes

**Last updated:** 2026-06-20  
**Current phase:** 3 — First Connection Tests (in progress)

This file records what we verified, what failed, and answers to open questions from [PLAN.md](PLAN.md). Update it as each phase completes.

---

## Phase Summary

| Phase | Status | Date | Notes |
|-------|--------|------|-------|
| 0 — Environment verification | **Pass** | 2026-06-20 | UE 5.8 opens project; Grok runs from repo root |
| 1 — Enable Unreal MCP | **Pass** | 2026-06-20 | Plugin enabled; auto-start on port 8000 |
| 2 — Connect Grok | **Pass** | 2026-06-20 | `unreal-mcp` shows **ready** in `/mcps` |
| 3 — First connection tests | **In progress** | 2026-06-20 | Meta-tools work; scene tools pending EditorToolset restart |
| 4 — Repeatable workflow | Not started | — | — |
| 5 — Grow capabilities | Not started | — | — |

---

## Phase 2 — Grok Connected (Verified)

Grok sees the project-scoped MCP server and reports it as ready.

![Grok /mcps showing unreal-mcp ready](images/phase2-mcps-ready.jpg)

*Grok TUI → `/mcps` → Local (1) → `unreal-mcp [ready]`*

### Config in use

- **Project config:** `.grok/config.toml` → `http://127.0.0.1:8000/mcp`
- **UE plugins enabled in `.uproject`:** `ModelContextProtocol`, `MCPClientToolset`, `EditorToolset` (added 2026-06-20; requires editor restart)

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

### Batch A — Connectivity (no extra plugins)

These work with only the base MCP + Toolset Registry stack.

| # | Prompt to Grok | MCP path | Pass criteria | Result |
|---|----------------|----------|---------------|--------|
| A1 | "What MCP tools do you have from the unreal-mcp server?" | — | Lists 3 meta-tools: `list_toolsets`, `describe_toolset`, `call_tool` | **Pass** |
| A2 | "Use the Unreal MCP to list available toolsets." | `list_toolsets` | Returns at least one toolset name + description | **Pass** — `ToolsetRegistry.AgentSkillToolset` |
| A3 | "Describe the AgentSkill toolset." | `describe_toolset` | Returns tool names + input schemas | **Pass** — 4 tools (`ListSkills`, `GetSkills`, `CreateSkill`, `UpdateSkill`) |
| A4 | "List all AgentSkills in this project." | `call_tool` → `ListSkills` | Returns `{}` (empty project) or a skill map | **Pass** — `{"returnValue": {}}` |

### Batch B — Scene inspection (requires EditorToolset)

**Prerequisite:** Enable **EditorToolset** plugin, restart editor, confirm log shows multiple toolsets registered. If toolsets are stale after restart, run in UE console:

```
ModelContextProtocol.RefreshTools
```

Then press `r` in Grok `/mcps` to refresh.

| # | Prompt to Grok | Expected toolset / tool | Pass criteria | Result |
|---|----------------|-------------------------|---------------|--------|
| B1 | "List all MCP toolsets again — how many are there now?" | `list_toolsets` | Multiple toolsets (e.g. `SceneTools`, `ActorTools`, `PrimitiveTools`) | **Pending** — editor restart needed |
| B2 | "What actors are in the current level?" | `SceneTools.find_actors` | Returns actor labels (PlayerStart, floor, lighting, etc.) | **Pending** |
| B3 | "What is the path of the currently loaded level?" | `SceneTools.get_current_level` | Returns level asset path | **Pending** |

### Batch C — Light write (requires EditorToolset)

Run only after Batch B passes. Verify in the UE viewport after each step.

| # | Prompt to Grok | Expected toolset / tool | Pass criteria | Result |
|---|----------------|-------------------------|---------------|--------|
| C1 | "Spawn a static mesh cube at the world origin named GrokTestCube." | `SceneTools.add_to_scene_from_asset` with `/Engine/BasicShapes/Cube` | Cube visible at (0,0,0) in outliner/viewport | **Pending** |
| C2 | "Focus the viewport on GrokTestCube." | `EditorAppToolset.FocusOnActors` (via programmatic or direct call) | Camera frames the new actor | **Pending** |
| C3 | "Remove GrokTestCube from the scene." | `SceneTools.remove_from_scene` | Actor gone from level | **Pending** |

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

On first connect, only **one** toolset was registered:

```
LogModelContextProtocol: ... (1 toolsets discoverable via list_toolsets)
LogToolsetRegistry: Registering Toolset ToolsetRegistry.AgentSkillToolset
```

Actor/scene/spawn tools live in the separate **EditorToolset** engine plugin (`SceneTools`, `ActorTools`, `PrimitiveTools`, etc.). It is **not** enabled by default. We added it to `GrokUE_MCP.uproject`; a full editor restart is required before Batch B/C tests.

`MCPClientToolset` is a different plugin — an adapter for connecting *outbound* to external MCP servers, not the source of scene tools.

---

## Hitch Reports

None filed yet. Use the template in [PLAN.md](PLAN.md) if a test fails.

---

## Changelog (this file)

| Date | Change |
|------|--------|
| 2026-06-20 | Created NOTES.md; documented Phase 2 pass + Phase 3 Batch A results; added EditorToolset to `.uproject`; screenshot added |