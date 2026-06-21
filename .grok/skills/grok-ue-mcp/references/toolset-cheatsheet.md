# Toolset cheatsheet (GrokUE_MCP)

## Meta-tools (top-level)

- `list_toolsets`
- `describe_toolset` — `{ "toolset_name": "..." }`
- `call_tool` — `{ "toolset_name", "tool_name", "arguments" }`

## Scene (`editor_toolset.toolsets.scene.SceneTools`)

| Tool | Notes |
|------|-------|
| `get_current_level` | No args |
| `find_actors` | Requires `name`, `tag`, `collision_channels` (use `""`, `""`, `[]` for all) |
| `add_to_scene_from_asset` | `asset_path`, `name`, `xform` |
| `remove_from_scene` | `actor.refPath` |

## Editor app (`EditorToolset.EditorAppToolset`)

| Tool | Notes |
|------|-------|
| `GetSelectedActors` | No args |
| `FocusOnActors` | `actors: [{ refPath }]` |
| `GetCameraTransform` | No args — Phase 7 verified |
| `GetVisibleActors` | No args — actors in viewport frustum |
| `GetContentBrowserPath` | No args — e.g. `/Game` |
| `IsPIERunning` | No args |
| `CaptureAssetImage` | `assetPath` — PNG base64; don't log payload |
| `CaptureViewport` | Optional annotations (large payload) |

## Logs (`EditorToolset.LogsToolset`)

| Tool | Notes |
|------|-------|
| `GetLogCategories` | `filter` substring |
| `GetLogEntries` | `pattern` required; `category`, `maxEntries` |

## Actor (`editor_toolset.toolsets.actor.ActorTools`)

| Tool | Notes |
|------|-------|
| `get_label` | `actor.refPath` |
| `get_actor_transform` | `actor.refPath` |
| `get_actor_bounds` | `actor.refPath` |
| `get_components` | `actor.refPath` |
| `get_tags` | `actor.refPath` |

## Custom (`grok_ue_mcp.toolsets.project_tools.GrokProjectTools`)

| Tool | Notes |
|------|-------|
| `health_check` | No args — confirms plugin loaded |
| `get_session_info` | No args — project name, dirs, level path |

## After editing custom tools

UE console: `ModelContextProtocol.RefreshTools` → Grok `/mcps` → `r`