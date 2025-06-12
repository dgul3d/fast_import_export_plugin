import bpy
from .preset_manager import get_preset_items
from .preset_manager import get_preset_tree

def update_preset_items(self, context):
    return get_preset_items()

class FASTIO_OT_button(bpy.types.Operator):
    bl_idname = "export.button"
    bl_label = "Export"
    bl_description = ""
    bl_options = {"REGISTER"}



    @classmethod
    def poll(cls, context):
        result = (context.selected_objects != []) and scene_property_exists("export_path") and scene_property_exists("export_preset")
        return result
    
    @classmethod
    def description(cls, context, properties):
        if (context.selected_objects == []):
            return "Select objects for export"
        elif scene_property_exists("export_preset") is False:
            return "Create the fbx export preset"
        elif scene_property_exists("export_path") is False:
            return "Choose an export path"
        else:
            return f"Export selected using preset {bpy.data.scenes['Scene']['export_preset']}"

    def execute(self, context):
        try:
            export_preset_name = bpy.data.scenes['Scene']["export_preset"]
        except AttributeError:
            self.report({'ERROR'}, "Preset not found or invalid.") 
            return {'CANCELLED'}
        try:
            export_path = bpy.data.scenes['Scene']['export_path']
        except KeyError:
            self.report({'ERROR'}, "Export path not set.") 
            return {'CANCELLED'}
        else:
            preset_tree = get_preset_tree()
            if export_preset_name not in preset_tree:
                self.report({'ERROR'}, f"Selected preset '{export_preset_name}' not found. Please select a valid preset.")
                return {'CANCELLED'}

            preset_operator = preset_tree[export_preset_name]["preset_operator"]
            arguments = preset_tree[export_preset_name]["kwargs"]
            arguments["filepath"] = export_path
            
            try:
                eval(f"bpy.ops.{preset_operator.split('.')[-2]}.{preset_operator.split('.')[-1]}(**{arguments})")
            except Exception as e:
                self.report({'ERROR'}, f"Export failed: {e}")
                return {'CANCELLED'}

        return {"FINISHED"}

class FASTIO_OT_settings(bpy.types.Operator):
    bl_idname = "export.settings"
    bl_label = "Export"
    bl_description = "Select an Export Preset"
    bl_options = {"REGISTER", "UNDO"}
    preset_name: bpy.props.EnumProperty(
        items=update_preset_items,
        name="Export Preset",
        description="Select an export preset",
    )

    def execute(self, context):
        bpy.data.scenes['Scene']["export_preset"] = self.preset_name
        return {"FINISHED"}

    def invoke(self, context, event):
        if not get_preset_items(): 
            self.report({'INFO'}, "No export presets found. Please save an export preset in Blender first (File > Export > FBX > Operator Presets > New).")
            return {'CANCELLED'}
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