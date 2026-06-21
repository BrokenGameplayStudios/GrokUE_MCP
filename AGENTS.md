# GrokUE_MCP — Agent Conventions

Instructions for AI agents (Grok, etc.) working in this Unreal Engine 5.8 project via MCP.

**Canonical repo path:** `F:\git\GrokUE_MCP`  
**MCP endpoint:** `http://127.0.0.1:8000/mcp` (project-scoped in `.grok/config.toml`)

---

## Before you touch the editor

1. **Unreal Editor must be running** with `GrokUE_MCP.uproject` open.
2. **MCP server must be listening** — Output Log should show `Starting MCP server on port 8000`.
3. **Grok must be launched from the repo root** so `.grok/config.toml` loads.
4. **Startup order:** UE first → Grok second.
5. After an **editor restart**, re-handshake MCP in Grok: `/mcps` → press **`r`**.

---

## MCP tool discovery (tool-search mode)

Epic's server exposes **3 meta-tools**, not a flat tool list:

| Meta-tool | Purpose |
|-----------|---------|
| `list_toolsets` | Names + descriptions of all toolsets |
| `describe_toolset` | Tool names and JSON schemas for one toolset |
| `call_tool` | Invoke a tool (`toolset_name`, `tool_name`, `arguments`) |

**Expected toolset count:** 19 shipped toolsets + 1 project toolset (`GrokUEMCPTools`) when the custom plugin is enabled = **20**.

Key toolsets for daily work:

| Toolset | Use for |
|---------|---------|
| `editor_toolset.toolsets.scene.SceneTools` | Level path, find/spawn/remove actors |
| `EditorToolset.EditorAppToolset` | Selection, viewport camera, capture screenshots |
| `editor_toolset.toolsets.actor.ActorTools` | Transforms, labels, components |
| `grok_ue_mcp.toolsets.project_tools.GrokProjectTools` | Project health checks (custom) |

---

## Execution rules

- **One MCP tool call at a time.** Epic serializes on the game thread; parallel calls can deadlock.
- **Read before write.** Prefer `find_actors`, `get_current_level`, `GetSelectedActors` before spawning or deleting.
- **Verify writes in the viewport.** After spawn/move/delete, ask the user to confirm in Outliner/viewport when visual confirmation matters.
- **Use actor `refPath` values** returned by prior tool calls when focusing, selecting, or removing actors.

### Known API quirks

- `SceneTools.find_actors` rejects `{}`. Pass:
  ```json
  {"name": "", "tag": "", "collision_channels": []}
  ```
- `add_to_scene_from_asset` requires `asset_path`, `name`, and `xform` (use `{"location": {"x": 0, "y": 0, "z": 0}}` for origin).
- `FocusOnActors` needs an array of actor refs: `{"actors": [{"refPath": "..."}]}`.

---

## Health checks (read-only)

Run these at session start without modifying the level:

1. *"What MCP tools do you have from the unreal-mcp server?"* → 3 meta-tools
2. `list_toolsets` → expect 20 toolsets (after custom plugin enabled)
3. `call_tool` → `GrokProjectTools.health_check` → `"GrokUE_MCP: custom toolset healthy"`
4. `SceneTools.get_current_level` → level asset path

Full integration test history: `Docs/NOTES.md` (Phase 3 Batches A/B/C).

---

## Custom toolset workflow

Python toolsets live in `Plugins/GrokUEMCPTools/Content/Python/`.

**Structured return types** must use `@unreal.ustruct()` + `unreal.StructBase` + `unreal.uproperty()` — not Python `@dataclass`. Plain dataclasses break `@unreal.uclass()` generation at editor startup (see `Docs/NOTES.md` Phase 5 hitch).

After editing toolset code:

1. If `init_unreal.py` failed (traceback in Output Log), **restart the editor** after fixing `.py` files.
2. Otherwise run `ModelContextProtocol.RefreshTools` in the UE console (` key).
3. Re-handshake Grok MCP (`/mcps` → `r`).
4. `list_toolsets` → confirm `grok_ue_mcp.toolsets.project_tools.GrokProjectTools` appears.

---

## Hitch reporting

If a tool call fails, capture:

- Which test/prompt failed
- Grok or MCP error text
- `LogModelContextProtocol` lines from UE Output Log
- `grok mcp doctor unreal-mcp` output

Template: `Docs/PLAN.md` → Hitch Reporting Template. Log results in `Docs/NOTES.md`.

---

## Documentation map

| File | Contents |
|------|----------|
| `Docs/PLAN.md` | Full integration plan, phases, troubleshooting |
| `Docs/NOTES.md` | Verified test results, screenshots, session workflow |
| `Docs/images/` | Phase screenshots for regression reference |
| `.grok/skills/grok-ue-mcp/SKILL.md` | Slash skill: `/grok-ue-mcp` |

---

## Project constraints

- **Blueprint-only** — no `Source/` module yet. Custom automation is Python toolsets, not C++.
- **Experimental APIs** — Unreal MCP and Toolset Registry may change between UE 5.8 patches.
- **Localhost only** — do not expose port 8000 beyond the dev machine.