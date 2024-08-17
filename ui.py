import bpy
from .importer import get_preset_values
from .importer import get_preset_tree

class FASTIO_OT_button(bpy.types.Operator):
    bl_idname = "export.button"
    bl_label = "Export"
    bl_description = ""
    bl_options = {"REGISTER"}



    @classmethod
    def poll(cls, context):
        result = (context.selected_objects != []) and scene_property_exists("export_path") and scene_property_exists("export_preset")
        return result
    
    #TODO Add check if export_preset and export_path are set. Change bl_description depending on a case
    @classmethod
    def description(cls, context, properties):
        if (context.selected_objects == []):
            return "Select objects for export"
        elif not scene_property_exists("export_preset"):
            return "Select a preset"
        elif not scene_property_exists("export_path"):
            return "Choose an export path"
        else:
            return f"Export selected using preset {bpy.data.scenes['Scene']['export_preset']}"

    def execute(self, context):
        export_path = ""
        try:
            export_settings = get_preset_values(bpy.data.scenes['Scene']["export_preset"])
        except AttributeError:
            return "Preset not found"
        try:
            export_path = bpy.data.scenes['Scene']['export_path']
        except KeyError:
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', **export_settings)
        else:
            if bpy.data.scenes['Scene']["export_preset"].split("_")[0] == "fbx":
                if bpy.data.scenes['Scene']["export_preset"].split("_")[2] == "builtin":
                    bpy.ops.export_scene.fbx(filepath = export_path, **export_settings)
                elif bpy.data.scenes['Scene']["export_preset"].split("_")[2] == "betterfbx":
                    bpy.ops.better_export.fbx(filepath = export_path, **export_settings)
                else:
                    return "Preset not found"
        return {"FINISHED"}

class FASTIO_OT_settings(bpy.types.Operator):
    bl_idname = "export.settings"
    bl_label = "Export"
    bl_description = "Select an Export Preset"
    bl_options = {"REGISTER", "UNDO"}
    preset_items = get_preset_tree("export")

    preset_name: bpy.props.EnumProperty(
        items=preset_items,
        name="Export Preset",
        description="Select an export preset",
    )

    def execute(self, context):
        bpy.data.scenes['Scene']["export_preset"] = self.preset_name
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

def draw(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator(FASTIO_OT_button.bl_idname, icon = "EXPORT")
    row.operator(FASTIO_OT_settings.bl_idname, text = "" , icon = "PREFERENCES")

def scene_property_exists(preset_name: str):
    return bpy.data.scenes['Scene'].get(preset_name) is not None

def draw_button():
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)
def undraw_button():
    bpy.types.VIEW3D_HT_tool_header.remove(draw)