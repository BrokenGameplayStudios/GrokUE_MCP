# GrokUE_MCP

A blank **Unreal Engine 5.8** Blueprint project and integration workspace for connecting **[Grok](https://x.ai)** to **Unreal Editor** via the **Model Context Protocol (MCP)**.

This repo is not a game prototype. It exists to document, test, and stabilize a repeatable workflow where Grok can inspect and manipulate the editor through natural language — spawning actors, querying the scene, driving Blueprint tooling, and eventually project-specific automation.

**Maintained by:** [Broken Gameplay Studios](https://github.com/BrokenGameplayStudios)

---

## Recent Updates

| Date | Update |
|------|--------|
| **2026-06-20** | Initial scaffold committed: blank UE 5.8 project (`GrokUE_MCP.uproject`), standard `Config/`, integration plan in `Docs/PLAN.md`, and project-scoped Grok MCP config (`.grok/config.toml` → `http://127.0.0.1:8000/mcp`). MCP plugin not yet enabled in editor. |
| **2026-06-20** | Repository created. Blank UE project built locally at `F:\UEDEV\GrokUE_MCP`, copied into `F:\git\GrokUE_MCP` for version control. |

*Add new rows at the top of this table as the project progresses.*

---

## Current State

| Area | Status |
|------|--------|
| **Integration phase** | Phase 0 — scaffolded, MCP not yet connected |
| **Unreal project** | Blank Blueprint template, UE 5.8, opened once at creation |
| **MCP server** | Not configured — Epic **Unreal MCP** plugin not yet enabled |
| **Grok config** | Project-scoped `.grok/config.toml` templated for `unreal-mcp` HTTP endpoint |
| **Next step** | Open project in UE 5.8 → enable Unreal MCP → verify Grok connection (see `Docs/PLAN.md`) |

### What works today

- Project opens as a standard blank UE 5.8 Blueprint project.
- Repo is ready for commit/push with sensible UE `.gitignore` rules.
- Integration roadmap and hitch-report template are written.

### What does not work yet

- Grok cannot control the editor — the MCP bridge has not been brought up.
- No custom toolsets, plugins, or gameplay content.

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
│   └── PLAN.md           # Full integration plan, phases, troubleshooting
├── .grok/
│   └── config.toml       # Project-scoped Grok MCP server config
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
| [README.md](README.md) | Project overview, current state, changelog (this file) |

---

## Reporting Issues

When something fails during setup, use the **Hitch Report** template in `Docs/PLAN.md` and paste it into your Grok session. Include `LogModelContextProtocol` lines from the UE Output Log and output from `grok mcp doctor unreal-mcp`.

---

## License

TBD — add license terms when the project scope stabilizes.