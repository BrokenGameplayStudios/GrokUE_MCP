---
name: grok-ue-mcp
description: >
  Drive GrokUE_MCP — the Unreal Engine 5.8 + Grok MCP integration project.
  Use when working in this repo with Unreal Editor, unreal-mcp, scene tools,
  spawning actors, viewport focus, custom GrokProjectTools, integration tests,
  or hitch debugging. Triggers: "unreal mcp", "GrokUE", "spawn in UE",
  "what actors", "list toolsets", "/grok-ue-mcp". Read AGENTS.md and Docs/NOTES.md first.
---

# GrokUE MCP Integration

**Handoff:** Phases 0–7 are complete. Read `Docs/NOTES.md` → **Handoff**; next work: `Docs/PHASE8_PLAN.md`. Run `GrokProjectTools.health_check` first.

You are working in **GrokUE_MCP** — a blank UE 5.8 project wired to Grok via Epic's built-in Unreal MCP plugin.

## Session startup (every time)

1. Confirm UE editor is open on `GrokUE_MCP.uproject` and MCP auto-started (port 8000).
2. Confirm `unreal-mcp` is **ready** in `/mcps` (press `r` after editor restarts).
3. Run a read-only health check: `list_toolsets` → expect **20** toolsets, or call `GrokProjectTools.health_check`.
4. Issue **one MCP tool call at a time**.

Full checklist: `Docs/NOTES.md` § Phase 4.

## MCP call pattern

```
list_toolsets → describe_toolset → call_tool
```

Example — list all actors:

```
call_tool(
  toolset_name: "editor_toolset.toolsets.scene.SceneTools",
  tool_name: "find_actors",
  arguments: {"name": "", "tag": "", "collision_channels": []}
)
```

Example — spawn test cube:

```
call_tool(
  toolset_name: "editor_toolset.toolsets.scene.SceneTools",
  tool_name: "add_to_scene_from_asset",
  arguments: {
    "asset_path": "/Engine/BasicShapes/Cube",
    "name": "GrokTestCube",
    "xform": {"location": {"x": 0, "y": 0, "z": 0}}
  }
)
```

## Common prompts

| Goal | Approach |
|------|----------|
| Health check | `list_toolsets` or `GrokProjectTools.health_check` |
| Actors in level | `SceneTools.find_actors` (empty filter args) |
| Current level | `SceneTools.get_current_level` |
| Selection | `EditorAppToolset.GetSelectedActors` |
| Focus viewport | `EditorAppToolset.FocusOnActors` with actor refPath |
| Screenshot | `EditorAppToolset.CaptureViewport` or ask user for editor screenshot |
| Remove actor | `SceneTools.remove_from_scene` with actor refPath |

## Write operations

After spawn/move/delete, **ask the user to confirm** in Outliner/viewport when the test plan requires visual verification. Reference `Docs/images/` for expected outcomes from Phase 3.

## Hitch playbook

If MCP fails:

1. Check UE Output Log for `LogModelContextProtocol` errors.
2. Run `grok mcp doctor unreal-mcp` from repo root.
3. If `Unknown session id` → `/mcps` → `r`.
4. If toolset missing after code change → UE console: `ModelContextProtocol.RefreshTools`.
5. Log findings in `Docs/NOTES.md` using the template in `Docs/PLAN.md`.

## References

- `AGENTS.md` — agent conventions (read first)
- `Docs/NOTES.md` — verified tests and screenshots
- `Docs/PLAN.md` — full integration plan
- `.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md` — quick toolset index