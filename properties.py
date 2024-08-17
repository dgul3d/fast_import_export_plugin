import bpy
import os

class AddFolderPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        # layout.label(text="Addon Preferences")

        row = layout.row()
        # row.label(text="Addon Folder:")
        row.operator("ui.open_folder", text="Open Addon Folder")

class OpenFolderOperator(bpy.types.Operator):
    bl_idname = "ui.open_folder"
    bl_label = "Open Addon Folder"

    def execute(self, context):
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f'explorer.exe "{addon_dir}"')
        return {'FINISHED'}