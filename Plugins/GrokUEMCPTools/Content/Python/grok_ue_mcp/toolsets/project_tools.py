"""Project-specific MCP tools for GrokUE_MCP."""

from __future__ import annotations

import dataclasses
import os

import unreal
import toolset_registry


@dataclasses.dataclass
class GrokSessionInfo:
    """Snapshot of project and level context for Grok health checks."""

    project_name: str
    project_dir: str
    content_dir: str
    current_level: str


@unreal.uclass()
class GrokProjectTools(unreal.ToolsetDefinition):
    """GrokUE_MCP project tools for integration health checks and session context."""

    @toolset_registry.tool_call
    @staticmethod
    def health_check() -> str:
        """Returns a confirmation string when the GrokUE_MCP custom toolset is registered.

        Returns:
            A static health-check message.
        """
        return 'GrokUE_MCP: custom toolset healthy'

    @toolset_registry.tool_call
    @staticmethod
    def get_session_info() -> GrokSessionInfo:
        """Returns project directories and the currently loaded level path.

        Returns:
            Project name, project root, content directory, and current level path.
        """
        project_file = unreal.Paths.get_project_file_path()
        project_name = os.path.splitext(os.path.basename(project_file))[0]
        project_dir = os.path.dirname(project_file)
        content_dir = unreal.Paths.project_content_dir()

        les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        current_level = les.get_current_level() if les else None
        level_path = (
            current_level.get_outermost().get_name() if current_level else ''
        )

        return GrokSessionInfo(
            project_name=project_name,
            project_dir=project_dir,
            content_dir=content_dir,
            current_level=level_path,
        )