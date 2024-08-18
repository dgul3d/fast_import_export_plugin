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
        elif scene_property_exists("export_preset") is False:
            return "Select a preset"
        elif scene_property_exists("export_path") is False:
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

class FASTIO_OT_export_path(bpy.types.Operator):
    bl_idname = "export.export_path"
    bl_label = "Set Export Path"
    bl_description = "Open a file browser to set the export path"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.data.scenes['Scene']['export_path'] = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        if scene_property_exists('export_path'):
            self.filepath = bpy.data.scenes['Scene']['export_path']
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    filepath: bpy.props.StringProperty(subtype="DIR_PATH")

def draw(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator(FASTIO_OT_button.bl_idname, icon = "EXPORT")
    row.operator(FASTIO_OT_settings.bl_idname, text = "" , icon = "PREFERENCES")
    row.operator(FASTIO_OT_export_path.bl_idname, text = "" , icon = "FILE_FOLDER")

def scene_property_exists(property_name: str):
    if property_name in bpy.data.scenes['Scene'] and (bpy.data.scenes['Scene'].get(property_name) is not None):
        return True
    else:
        return False 

def draw_button():
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)
def undraw_button():
    bpy.types.VIEW3D_HT_tool_header.remove(draw)