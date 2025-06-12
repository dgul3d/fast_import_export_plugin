import bpy
import os
from .preset_manager import get_preset_items # Import get_preset_items

def get_export_preset_items_for_prefs(self, context):
    return get_preset_items(is_export=True)

def get_import_preset_items_for_prefs(self, context):
    return get_preset_items(is_export=False)

class AddFolderPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_export_preset: bpy.props.EnumProperty(
        items=get_export_preset_items_for_prefs,
        name="Default Export Preset",
        description="Select the default export preset to use when importing files",
    )

    default_import_preset: bpy.props.EnumProperty(
        items=get_import_preset_items_for_prefs,
        name="Default Import Preset",
        description="Select the default import preset to use when importing files",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_export_preset")
        layout.prop(self, "default_import_preset")
        row = layout.row()
        row.operator("ui.open_folder", text="Open Addon Folder")
        



class OpenFolderOperator(bpy.types.Operator):
    bl_idname = "ui.open_folder"
    bl_label = "Open Addon Folder"

    def execute(self, context):
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f'explorer.exe "{addon_dir}"')
        return {'FINISHED'}