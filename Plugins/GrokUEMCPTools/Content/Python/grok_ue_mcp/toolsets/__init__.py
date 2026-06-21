from toolset_registry.registration import Registration

from grok_ue_mcp.toolsets import project_tools

_registration = Registration([
    project_tools.GrokProjectTools,
])