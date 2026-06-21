# MCP Tool Catalog (live snapshot)

**Source:** `list_toolsets` + `describe_toolset` on UE 5.8 editor with `GrokUEMCPTools` enabled (2026-06-21).  
**Total:** 20 toolsets · **260 tools** (3 meta + 257 toolset tools)

> Patches or plugins may add/rename tools. Re-run `describe_toolset` for the authoritative list in your session.

**Testing legend (from Phases 0–8):** ✅ verified · 🔶 partial probe · 📋 cataloged only · ❓ not run in this repo

---

## Meta (3)

| Tool | Tested |
|------|--------|
| `list_toolsets` | ✅ |
| `describe_toolset` | ✅ |
| `call_tool` | ✅ |

---

## SceneTools — `editor_toolset.toolsets.scene.SceneTools` (20)

| Tool | Tested |
|------|--------|
| `get_current_level` | ✅ |
| `load_level` | 📋 |
| `find_actors` | ✅ |
| `add_to_scene_from_asset` | ✅ |
| `add_to_scene_from_class` | 📋 |
| `remove_from_scene` | ✅ |
| `get_collision_channels` | 📋 |
| `get_folders` | 📋 |
| `get_actors_in_folder` | 📋 |
| `set_actor_folder` | 📋 |
| `rename_folder` | 📋 |
| `delete_folder` | 📋 |
| `trace_world` | 📋 |
| `merge_actors` | 📋 |
| `create_level_instance` | 📋 |
| `edit_level_instance` | 📋 |
| `commit_level_instance` | 📋 |
| `can_edit` | 📋 |
| `is_checked_out` | 📋 |
| `save_actor` | 📋 |

---

## ActorTools — `editor_toolset.toolsets.actor.ActorTools` (17)

| Tool | Tested |
|------|--------|
| `get_label` | ✅ |
| `set_label` | 📋 |
| `get_actor_transform` | ✅ |
| `set_actor_transform` | ✅ |
| `get_actor_bounds` | ✅ |
| `get_tags` | ✅ |
| `add_tag` | 📋 |
| `remove_tag` | 📋 |
| `has_tag` | 📋 |
| `look_at` | 📋 |
| `get_components` | ✅ |
| `add_component` | 📋 |
| `remove_component` | 📋 |
| `get_root_component` | 📋 |
| `get_parent_component` | 📋 |
| `set_parent_component` | 📋 |
| `get_component_actor` | 📋 |

---

## EditorAppToolset — `EditorToolset.EditorAppToolset` (21)

| Tool | Tested |
|------|--------|
| `GetSelectedActors` | ✅ |
| `SelectActors` | 📋 |
| `GetSelectedAssets` | 📋 |
| `SelectAssets` | 📋 |
| `FocusOnActors` | ✅ |
| `GetCameraTransform` | ✅ |
| `SetCameraTransform` | 📋 |
| `GetVisibleActors` | ✅ |
| `GetContentBrowserPath` | ✅ |
| `SetContentBrowserPath` | ✅ |
| `IsPIERunning` | ✅ |
| `StartPIE` | ❓ |
| `StopPIE` | ❓ |
| `CaptureViewport` | ✅ |
| `CaptureEditorImage` | 📋 |
| `CaptureAssetImage` | ✅ |
| `OpenEditorForAsset` | 📋 |
| `GetOpenAssets` | 📋 |
| `SearchCVars` | ✅ |
| `WorldPosToScreenCoords` | 📋 |
| `ScreenCoordsToWorld` | 📋 |

---

## LogsToolset — `EditorToolset.LogsToolset` (4)

| Tool | Tested |
|------|--------|
| `GetLogCategories` | ✅ |
| `GetLogEntries` | ✅ |
| `GetVerbosity` | 📋 |
| `SetVerbosity` | 📋 |

---

## AssetTools — `editor_toolset.toolsets.asset.AssetTools` (21)

| Tool | Tested |
|------|--------|
| `find_assets` | ✅ |
| `list_folders` | ✅ |
| `get_asset_class` | ✅ |
| `get_plugin_content_paths` | ✅ |
| `load_asset` | 📋 |
| `exists` | 📋 |
| `create_folder` | 📋 |
| `move` | ✅ |
| `duplicate` | 📋 |
| `delete` | 📋 |
| `save_assets` | ✅ |
| `is_dirty` | 📋 |
| `can_edit_asset` | 📋 |
| `is_checked_out` | 📋 |
| `get_metadata_tags` | 📋 |
| `update_metadata_tags` | 📋 |
| `get_asset_tags` | 📋 |
| `get_dependencies` | 📋 |
| `get_referencers` | 📋 |
| `read_file` | 📋 |
| `write_file` | 📋 |

---

## ObjectTools — `editor_toolset.toolsets.object.ObjectTools` (6)

| Tool | Tested |
|------|--------|
| `search_subclasses` | ✅ |
| `get_class` | 📋 |
| `list_properties` | 📋 |
| `get_properties` | ✅ |
| `set_properties` | ✅ |
| `reset_properties` | 📋 |

---

## BlueprintTools — `editor_toolset.toolsets.blueprint.BlueprintTools` (53)

| Tool | Tested |
|------|--------|
| `create` | ✅ |
| `compile_blueprint` | ✅ |
| `get_parent` | ✅ |
| `set_parent` | 📋 |
| `get_default_object` | 📋 |
| `list_graphs` | ✅ |
| `get_graph` | ✅ |
| `list_functions` | ✅ |
| `list_events` | ✅ |
| `add_function_graph` | 📋 |
| `remove_function_graph` | 📋 |
| `add_event` | 📋 |
| `add_event_dispatcher` | 📋 |
| `list_event_dispatchers` | 📋 |
| `add_function_param` | 📋 |
| `add_struct_function_param` | 📋 |
| `add_object_function_param` | 📋 |
| `remove_function_param` | 📋 |
| `add_variable` | ✅ |
| `add_struct_variable` | 📋 |
| `add_object_variable` | 📋 |
| `remove_variable` | 📋 |
| `list_variables` | 📋 |
| `get_variable_category` | 📋 |
| `set_variable_category` | 📋 |
| `get_variable_replication` | 📋 |
| `set_variable_replication` | 📋 |
| `set_variable_instance_editable` | 📋 |
| `get_graph_dsl_docs` | ✅ |
| `read_graph_dsl` | ✅ |
| `write_graph_dsl` | ✅ |
| `create_node` | 📋 |
| `delete_node` | 📋 |
| `add_node_pin` | 📋 |
| `remove_node_pin` | 📋 |
| `connect_pins` | 📋 |
| `break_pins` | 📋 |
| `get_pin_value` | 📋 |
| `set_pin_value` | 📋 |
| `set_node_position` | 📋 |
| `arrange_nodes` | 📋 |
| `retarget_node_class` | 📋 |
| `find_node_types` | 📋 |
| `find_node_categories` | 📋 |
| `get_node_type_pins` | 📋 |
| `find_nodes` | 📋 |
| `get_node_infos` | 📋 |
| `get_connected_subgraph` | 📋 |
| `list_component_events` | 📋 |
| `add_component_bound_event` | 📋 |
| `get_create_event_function` | 📋 |
| `set_create_event_function` | 📋 |
| `list_compatible_event_functions` | 📋 |

---

## StaticMeshTools — `editor_toolset.toolsets.static_mesh.StaticMeshTools` (16)

| Tool | Tested |
|------|--------|
| `import_file` | ✅ (FBX/OBJ only; glTF ❌) |
| `get_lod_count` | ✅ |
| `get_triangle_count` | ✅ |
| `get_vertex_count` | 📋 |
| `get_bounds` | ✅ |
| `get_material_slots` | ✅ |
| `get_material` | 📋 |
| `set_material` | ✅ |
| `get_lod_thresholds` | 📋 |
| `set_lod_thresholds` | 📋 |
| `generate_lods` | 📋 |
| `remove_lods` | 📋 |
| `is_nanite_enabled` | ✅ |
| `set_nanite_enabled` | 📋 |
| `generate_convex_collisions` | 📋 |
| `remove_collisions` | 📋 |

---

## SkeletalMeshTools — `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools` (22)

| Tool | Tested |
|------|--------|
| `import_file` | 📋 |
| `get_lod_count` | 📋 |
| `get_vertex_count` | 📋 |
| `get_section_count` | 📋 |
| `get_bounds` | 📋 |
| `get_skeleton` | 📋 |
| `get_bone_names` | 📋 |
| `get_bone_parent` | 📋 |
| `get_bone_children` | 📋 |
| `get_material_slots` | 📋 |
| `get_material` | 📋 |
| `set_material` | 📋 |
| `get_physics_asset` | 📋 |
| `assign_physics_asset` | 📋 |
| `get_morph_target_names` | 📋 |
| `get_socket_names` | 📋 |
| `add_socket` | 📋 |
| `remove_socket` | 📋 |
| `rename_socket` | 📋 |
| `get_socket_bone` | 📋 |
| `get_socket_transform` | 📋 |
| `set_socket_transform` | 📋 |

---

## MaterialTools — `editor_toolset.toolsets.material.MaterialTools` (22)

| Tool | Tested |
|------|--------|
| `create_material` | ✅ |
| `create_function` | ✅ |
| `create_parameter_collection` | 📋 |
| `list_expression_classes` | 📋 |
| `add_expression` | ✅ |
| `delete_expression` | 📋 |
| `get_expressions` | ✅ |
| `layout_expressions` | 📋 |
| `list_parameter_groups` | 📋 |
| `rename_parameter_group` | 📋 |
| `delete_parameter_group` | 📋 |
| `get_expression_input_names` | 📋 |
| `get_expression_output_names` | 📋 |
| `connect_expressions` | ✅ |
| `disconnect_expressions` | 📋 |
| `get_expression_inputs` | 📋 |
| `connect_to_output` | 📋 |
| `disconnect_from_output` | 📋 |
| `get_property_input` | 📋 |
| `delete_unused_expressions` | 📋 |
| `recompile` | ✅ |
| `get_referencing_materials` | 📋 |

---

## MaterialInstanceTools — `editor_toolset.toolsets.material_instance.MaterialInstanceTools` (13)

| Tool | Tested |
|------|--------|
| `create` | ✅ |
| `list_parameters` | ✅ |
| `get_scalar_parameter` | 📋 |
| `set_scalar_parameter` | ✅ |
| `get_vector_parameter` | 📋 |
| `set_vector_parameter` | 📋 |
| `get_texture_parameter` | 📋 |
| `set_texture_parameter` | 📋 |
| `get_static_switch_parameter` | 📋 |
| `set_static_switch_parameter` | 📋 |
| `set_parent` | 📋 |
| `clear_parameters` | 📋 |
| `set_parameter_override` | 📋 |

---

## TextureTools — `editor_toolset.toolsets.texture.TextureTools` (2)

| Tool | Tested |
|------|--------|
| `get_size` | ✅ |
| `import_file` | 📋 |

---

## DataTableTools — `editor_toolset.toolsets.data_table.DataTableTools` (10)

| Tool | Tested |
|------|--------|
| `search_row_structs` | ✅ |
| `create` | ✅ |
| `import_file` | 📋 |
| `get_schema` | ✅ |
| `list_rows` | ✅ |
| `add_rows` | ✅ |
| `remove_rows` | 📋 |
| `rename_rows` | 📋 |
| `get_rows` | ✅ |
| `set_rows` | ✅ |

---

## DataAssetTools — `editor_toolset.toolsets.data_asset.DataAssetTools` (1)

| Tool | Tested |
|------|--------|
| `create` | 🔶 (abstract bases won't save; use Blueprint `_C` subclass) |

---

## CurveTableTools — `editor_toolset.toolsets.curve_table.CurveTableTools` (9)

| Tool | Tested |
|------|--------|
| `create` | 📋 |
| `import_file` | 📋 |
| `list_rows` | ✅ |
| `add_row` | 📋 |
| `remove_row` | 📋 |
| `rename_row` | 📋 |
| `add_key` | ✅ |
| `set_keys` | 📋 |
| `get_keys` | ✅ |

---

## StringTableTools — `editor_toolset.toolsets.string_table.StringTableTools` (8)

| Tool | Tested |
|------|--------|
| `create` | ✅ |
| `import_file` | 📋 |
| `list_keys` | ✅ |
| `get_entry` | ✅ |
| `set_entry` | ✅ |
| `remove_entry` | 📋 |
| `get_namespace` | ✅ |
| `get_table_id` | ✅ |

---

## PrimitiveTools — `editor_toolset.toolsets.primitive.PrimitiveTools` (4)

| Tool | Tested |
|------|--------|
| `add_cube` | ✅ |
| `add_sphere` | 📋 |
| `add_cylinder` | 📋 |
| `add_cone` | 📋 |

---

## ProgrammaticToolset — `editor_toolset.toolsets.programmatic.ProgrammaticToolset` (2)

| Tool | Tested |
|------|--------|
| `get_execution_environment` | ✅ |
| `execute_tool_script` | ✅ |

---

## AgentSkillToolset — `ToolsetRegistry.AgentSkillToolset` (4)

| Tool | Tested |
|------|--------|
| `ListSkills` | ✅ |
| `GetSkills` | ✅ |
| `CreateSkill` | 📋 (needs user OK) |
| `UpdateSkill` | 📋 (needs user OK) |

---

## GrokProjectTools — `grok_ue_mcp.toolsets.project_tools.GrokProjectTools` (2)

| Tool | Tested |
|------|--------|
| `health_check` | ✅ |
| `get_session_info` | ✅ |

---

## Not present (checked 2026-06-21)

No **Landscape** toolset in `list_toolsets`. No MCP tool to restart or launch the editor.

---

## How to refresh

```text
call_tool → list_toolsets
call_tool → describe_toolset { "toolset_name": "..." }
```

See [CAPABILITIES.md](CAPABILITIES.md) for what we exercised end-to-end and [toolset-cheatsheet.md](../.grok/skills/grok-ue-mcp/references/toolset-cheatsheet.md) for argument notes on commonly used tools.