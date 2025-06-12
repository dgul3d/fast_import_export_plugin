import bpy
import os
from .preset_manager import get_preset_items

def get_export_preset_items_for_prefs(self, context):
    return get_preset_items(is_export=True)

class AddFolderPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_export_preset: bpy.props.EnumProperty(
        items=get_export_preset_items_for_prefs,
        name="Default Export Preset",
        description="Select the default export preset to use when importing files",
    )

    def draw(self, context):
        layout = self.layout
        # layout.label(text="Addon Preferences")

        row = layout.row()
        # row.label(text="Addon Folder:")
        row.operator("ui.open_folder", text="Open Addon Folder")
        
        # Draw the new default export preset dropdown
        layout.prop(self, "default_export_preset")

class OpenFolderOperator(bpy.types.Operator):
    bl_idname = "ui.open_folder"
    bl_label = "Open Addon Folder"

    def execute(self, context):
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f'explorer.exe "{addon_dir}"')
        return {'FINISHED'}