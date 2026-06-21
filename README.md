# GrokUE_MCP

A blank **Unreal Engine 5.8** Blueprint project and integration workspace for connecting **[Grok](https://x.ai)** (and other MCP clients) to **Unreal Editor** via Epic's built-in **Model Context Protocol (MCP)** plugin.

This repo is not a game prototype. It exists to **prove, document, and stabilize** a workflow where an AI agent inspects and manipulates the editor through MCP — scene tools, asset pipelines, Blueprint authoring, custom project toolsets, and web-sourced mesh import.

**Maintained by:** [Broken Gameplay Studios](https://github.com/BrokenGameplayStudios)

---

## Integration status (2026-06-21)

| Area | Status |
|------|--------|
| **Phases 0–8** | **Complete** — see [Docs/NOTES.md](Docs/NOTES.md) |
| **Epic MCP toolsets** | **19** cataloged and probed (Phase 7) |
| **Custom toolset** | `GrokProjectTools` — **20 toolsets** total when plugin enabled |
| **Test level** | `/Game/Maps/L_Grok` (`EditorStartupMap` in `Config/DefaultEngine.ini`) |
| **Test assets** | `/Game/MCPTest/` — Phase 8 material, DataTable, Blueprint, Kenney meshes |
| **Next (optional)** | Phase 2 geo: DEM → heightmap → landscape (no Landscape MCP toolset yet) |

### What this project validated

The integration was run as **hands-off as practical**: the agent drove MCP tool calls from Grok/Cursor; the human mainly kept the editor open, confirmed viewport/PIE results, saved the level, and restarted the editor when required.

**All documentation under `Docs/` was written during the test** — phase plans, progress checkpoints, verified results, screenshots, and hitch notes are part of the deliverable, not a separate doc pass.

| Capability | Verified |
|------------|----------|
| MCP connect (HTTP `127.0.0.1:8000/mcp`) | Phases 2–3 |
| Meta-tools: `list_toolsets`, `describe_toolset`, `call_tool` | Phase 3 |
| Scene read/write (actors, spawn, focus, remove) | Phases 3, 7 |
| All 19 shipped Epic toolsets (read + selective write probes) | Phase 7 |
| Custom `GrokProjectTools` (`health_check`, `get_session_info`) | Phases 5–6 |
| Multi-client (Grok TUI + Cursor IDE) | Phase 6 |
| Integrated content pipeline (material → MI → DataTable → BP graph → PIE) | Phase 8 H1 |
| Web mesh import (`import_file` FBX/OBJ + Kenney scaler script) | Phase 8 H2 |
| `ProgrammaticToolset`, `AgentSkillToolset`, EditorApp (incl. viewport capture) | Phase 7 |

**Not exercised / deferred:** `StartPIE`/`StopPIE` automation, `SkeletalMeshTools` (no rigged asset), glTF/GLB import (rejected by `FbxFactory`), CI headless `-ModelContextProtocolStartServer`, real-world terrain pipeline.

---

## Human steps you still need

MCP covers editor automation, not full unattended operation. Expect to:

| When | You do |
|------|--------|
| **Every session** | Open `GrokUE_MCP.uproject` first; confirm Output Log shows MCP on port **8000**; launch Grok from repo root |
| **After editor restart** | Re-handshake MCP clients — Grok TUI: `/mcps` → **`r`**; Cursor: restart Grok session |
| **After custom plugin / Python toolset changes** | **Full editor restart** (first enable or `init_unreal.py` failure); then `ModelContextProtocol.RefreshTools` if needed |
| **Visual verification** | Confirm spawns in Outliner/viewport; **Ctrl+S** to save `L_Grok` (spawns live in `__ExternalActors__`, gitignored) |
| **PIE checks** | Press Play in editor (H1 prints DataTable strings — not automated via MCP in this pass) |

**Not tested in this repo:** whether MCP can restart the editor or replace a manual restart. That remains a possible follow-up; today, restarts are a human step.

---

## Quick start (returning session)

**Prerequisites:** Unreal Engine 5.8, [Grok CLI](https://x.ai) authenticated.

```powershell
cd F:\git\GrokUE_MCP
# 1. Open GrokUE_MCP.uproject in UE 5.8 (wait for MCP server on port 8000)
grok
# 2. In TUI: /mcps → unreal-mcp [ready]  (press r after any editor restart)
# 3. Load skill: /grok-ue-mcp
# 4. Health check via MCP: GrokProjectTools.health_check
```

New session checklist: [Docs/NOTES.md](Docs/NOTES.md) → **Handoff** · [AGENTS.md](AGENTS.md) · skill `.grok/skills/grok-ue-mcp/SKILL.md`

First-time setup (enable plugin, Grok config): [Docs/PLAN.md](Docs/PLAN.md) Phases 0–2.

---

## Architecture

```
Grok / Cursor  ──HTTP MCP──►  Unreal Editor (Unreal MCP plugin, port 8000)
                                    ├── 19 Epic Python toolsets
                                    └── GrokUEMCPTools → GrokProjectTools
```

- **Endpoint:** `http://127.0.0.1:8000/mcp` (project-scoped in `.grok/config.toml`)
- **Discovery:** `list_toolsets` → `describe_toolset` → `call_tool` (one tool call at a time on the game thread)
- **Epic docs:** [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US)

---

## Repository layout

```
GrokUE_MCP/
├── GrokUE_MCP.uproject      # UE 5.8; EditorToolset + GrokUEMCPTools enabled
├── Config/                  # DefaultEngine.ini → L_Grok startup map
├── Content/
│   ├── Maps/L_Grok          # Test level
│   └── MCPTest/             # Phase 7–8 test assets
├── Plugins/GrokUEMCPTools/  # Custom Python MCP toolsets
├── ImportedAssets/          # Downloaded meshes (gitignored); scripts/ tracked
│   └── scripts/scale_obj_to_ue_cm.py   # Kenney OBJ → UE-sized import
├── Docs/
│   ├── PLAN.md              # Full integration plan (Phases 0–8)
│   ├── NOTES.md             # Verified results, handoff, screenshots index
│   ├── PHASE7_PROGRESS.md   # Phase 7 archive
│   ├── PHASE8_PLAN.md       # Phase 8 plan + success criteria
│   ├── PHASE8_PROGRESS.md   # Current checkpoint — start here after pull
│   └── images/              # Regression / pass screenshots
├── .grok/
│   ├── config.toml          # unreal-mcp server URL
│   └── skills/grok-ue-mcp/  # Slash skill: /grok-ue-mcp
├── AGENTS.md                # Agent conventions (read first in Cursor)
└── README.md
```

`Saved/`, `Intermediate/`, `DerivedDataCache/`, `Binaries/`, and `Content/__ExternalActors__/` are gitignored.

---

## Documentation map

| Document | Purpose |
|----------|---------|
| [Docs/PHASE8_PROGRESS.md](Docs/PHASE8_PROGRESS.md) | **Resume here** — latest checkpoint, Kenney import recipe |
| [Docs/NOTES.md](Docs/NOTES.md) | Full test history, handoff, hitch screenshots |
| [Docs/PLAN.md](Docs/PLAN.md) | Original phased plan, troubleshooting, hitch template |
| [Docs/PHASE7_PROGRESS.md](Docs/PHASE7_PROGRESS.md) | Phase 7 toolset probe archive |
| [Docs/PHASE8_PLAN.md](Docs/PHASE8_PLAN.md) | Phase 8 goals and success criteria |
| [AGENTS.md](AGENTS.md) | MCP rules, one-call-at-a-time, health checks |

---

## Recent updates

| Date | Update |
|------|--------|
| **2026-06-21** | **Phase 8 complete** — H2 Kenney web import (`scale_obj_to_ue_cm.py`, `--kenney-ue`); final screenshot `Docs/images/phase8-h2-kenney-imports-final.jpg`. |
| **2026-06-20** | **Phase 8 H1** — material + DataTable + Blueprint `write_graph_dsl` + PIE prints. |
| **2026-06-20** | **Phase 7 complete** — all 19 Epic toolsets cataloged/probed; `L_Grok` + `/Game/MCPTest/`. |
| **2026-06-20** | **Phases 3–6** — scene tests, daily workflow, `GrokProjectTools`, Cursor multi-client. |
| **2026-06-20** | **Phases 0–2** — UE 5.8 scaffold, MCP plugin enabled, Grok connected. |

---

## Reporting issues

Use the **Hitch Report** template in [Docs/PLAN.md](Docs/PLAN.md). Include `LogModelContextProtocol` from the UE Output Log and `grok mcp doctor unreal-mcp` output.

---

## License

TBD — add license terms when the project scope stabilizes.