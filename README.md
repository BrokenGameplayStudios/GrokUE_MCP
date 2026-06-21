# GrokUE_MCP

A blank **Unreal Engine 5.8** Blueprint project and integration workspace for connecting **[Grok](https://x.ai)** to **Unreal Editor** via the **Model Context Protocol (MCP)**.

This repo is not a game prototype. It exists to document, test, and stabilize a repeatable workflow where Grok can inspect and manipulate the editor through natural language — spawning actors, querying the scene, driving Blueprint tooling, and eventually project-specific automation.

**Maintained by:** [Broken Gameplay Studios](https://github.com/BrokenGameplayStudios)

---

## Recent Updates

| Date | Update |
|------|--------|
| **2026-06-20** | **Phase 5 pass** — custom `GrokProjectTools` registered (20 toolsets); ustruct hitch documented. |
| **2026-06-20** | **Phase 5 started** — `AGENTS.md`, `/grok-ue-mcp` skill, `GrokUEMCPTools` custom MCP plugin. |
| **2026-06-20** | **Phase 4 pass** — repeatable startup/shutdown workflow adopted; health check documented in `Docs/NOTES.md`. |
| **2026-06-20** | **Phase 3 complete** — Batches A/B/C verified (spawn, focus, remove cube with screenshots). See `Docs/NOTES.md`. |
| **2026-06-20** | Phase 3 Batch A verified (screenshot); editor restart registers **19 toolsets** including `SceneTools`. Batch B scene tests ready. See `Docs/NOTES.md`. |
| **2026-06-20** | Phase 2–3 started: Unreal MCP connected; Grok `/mcps` shows `unreal-mcp [ready]`. Batch A meta-tool tests pass. `EditorToolset` enabled in `.uproject`. |
| **2026-06-20** | Initial scaffold committed: blank UE 5.8 project (`GrokUE_MCP.uproject`), standard `Config/`, integration plan in `Docs/PLAN.md`, and project-scoped Grok MCP config (`.grok/config.toml` → `http://127.0.0.1:8000/mcp`). MCP plugin not yet enabled in editor. |
| **2026-06-20** | Repository created. Blank UE project built locally at `F:\UEDEV\GrokUE_MCP`, copied into `F:\git\GrokUE_MCP` for version control. |

*Add new rows at the top of this table as the project progresses.*

---

## Current State

| Area | Status |
|------|--------|
| **Integration phase** | Phase 5 **complete** (CI/headless optional future work) |
| **Unreal project** | Blank Blueprint template, UE 5.8 |
| **MCP server** | Epic **Unreal MCP** enabled; auto-start on `http://127.0.0.1:8000/mcp` |
| **Grok config** | Project-scoped `.grok/config.toml`; `unreal-mcp` reports **ready** in `/mcps` |
| **Next step** | Use `/grok-ue-mcp` skill for daily sessions; extend `GrokProjectTools` as needed |

### What works today

- Grok connects to Unreal MCP over HTTP; meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`) respond.
- Scene inspection (`find_actors`, `get_current_level`) and light writes (spawn, focus viewport, remove actor) verified.
- Repeatable daily session workflow (startup, health check, shutdown) in `Docs/NOTES.md` § Phase 4.
- `AGENTS.md` agent conventions, `/grok-ue-mcp` project skill, custom `GrokProjectTools` MCP toolset (20 toolsets total).
- Read-only AgentSkill queries work (empty project returns no skills).

### What does not work yet

- No gameplay content.
- CI/headless MCP (`-ModelContextProtocolStartServer`) not explored.

---

## Quick Start

**Prerequisites:** Unreal Engine 5.8, [Grok CLI](https://x.ai) installed and authenticated.

1. Clone this repo and open `GrokUE_MCP.uproject` in the UE 5.8 editor.
2. Follow the phased setup in **[Docs/PLAN.md](Docs/PLAN.md)** — enable the Unreal MCP plugin, auto-start the server, then launch Grok from the project root.
3. Run the Phase 3 connection tests in the plan to confirm the bridge is live.

```powershell
cd F:\git\GrokUE_MCP
grok
# In the TUI: /mcps → confirm unreal-mcp is enabled
```

---

## Repository Layout

```
GrokUE_MCP/
├── GrokUE_MCP.uproject   # UE 5.8 project file
├── Config/               # Engine config (DefaultEngine, Input, etc.)
├── Content/              # Blank — no gameplay assets yet
├── Docs/
│   ├── PLAN.md           # Full integration plan, phases, troubleshooting
│   ├── NOTES.md          # Phase results, test batches, open questions
│   └── images/           # Screenshots for documentation
├── .grok/
│   ├── config.toml       # Project-scoped Grok MCP server config
│   └── skills/grok-ue-mcp/  # Project skill: /grok-ue-mcp
├── Plugins/GrokUEMCPTools/  # Custom Python MCP toolsets
├── AGENTS.md             # Grok agent conventions for this project
└── README.md             # This file
```

Generated UE folders (`Saved/`, `Intermediate/`, `DerivedDataCache/`, `Binaries/`) are gitignored and stay local.

---

## Architecture (Target)

```
Grok CLI  ──HTTP MCP──►  Unreal Editor (Unreal MCP plugin)
                              └── Toolset Registry → engine tools
```

Default endpoint: `http://127.0.0.1:8000/mcp`

Epic's built-in **Unreal MCP** plugin is the primary integration path. See [Epic's UE 5.8 documentation](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US). A community fallback (`chongdashu/unreal-mcp`) is documented in `Docs/PLAN.md` if the built-in plugin cannot be enabled.

**Startup order:** Unreal Editor first (MCP server must be listening), then Grok.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [Docs/PLAN.md](Docs/PLAN.md) | Step-by-step integration phases, test prompts, hitch-report template |
| [Docs/NOTES.md](Docs/NOTES.md) | Verified results, Phase 3 test batches, findings |
| [README.md](README.md) | Project overview, current state, changelog (this file) |

---

## Reporting Issues

When something fails during setup, use the **Hitch Report** template in `Docs/PLAN.md` and paste it into your Grok session. Include `LogModelContextProtocol` lines from the UE Output Log and output from `grok mcp doctor unreal-mcp`.

---

## License

TBD — add license terms when the project scope stabilizes.