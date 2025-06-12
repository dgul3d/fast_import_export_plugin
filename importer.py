import os
import bpy
import json
import sys

addon_dir = os.path.dirname(os.path.abspath(__file__))
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

import preset_manager

filename = "presets.json"

def create_export_path_property():
    bpy.types.Scene.export_path = bpy.props.StringProperty(
        name="Export Path",
        default="",
        subtype='FILE_PATH',
    )

def get_json(file_path):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open(file_path) as file:
            data = json.load(file)
    except FileNotFoundError:
        return "File not found"
    except json.JSONDecodeError:
        return "Invalid JSON format"
    return data

def get_preset(filetype, direction, tool, preset):
    return dict(get_json(filename)[filetype][direction][tool][preset])

def get_preset_values(preset_identifier):
    for filetype, directions in get_json(filename).items():
        for direction, tools in directions.items():
            for tool, presets in tools.items():
                for preset_name, preset_info in presets.items():
                    if '_'.join([filetype, direction, tool, preset_name]) == preset_identifier:
                        return preset_info.get("values", "")
                    
def get_preset_tree(direction_type):
    presets_list = []
    for filetype, directions in get_json(filename).items():
        for direction, tools in directions.items():
            if direction == direction_type:
                for tool, presets in tools.items():
                    for preset_name, preset_info in presets.items():
                        identifier = '_'.join([filetype, direction, tool, preset_name])
                        name = preset_info.get('name', '')
                        description = preset_info.get('description', '')
                        presets_list.append((identifier, name, description))
    return presets_list


def import_file():
    from sys import argv
    argv = argv[argv.index("--") + 1:]
    bpy.context.preferences.view.show_splash = False
    for f in argv:
        ext = os.path.splitext(f)[1].lower()
        if ext == ".fbx":
            try:
                bpy.ops.import_scene.fbx(filepath=f, **get_preset_values("fbx_import_builtin_default"))
            except RuntimeError:
                if 'better_fbx' in [addon.module for addon in bpy.context.preferences.addons]:
                    bpy.ops.better_import.fbx(filepath=f, **get_preset_values("fbx_import_betterfbx_default"))
                else:
                    raise RuntimeError("Attempted to open ASCII FBX without Better Fbx Importer")   
        # else if ext == ".gltf" or ".glb"
        #     try:
        #         bpy.ops.import_scene.gltf(filepath=f, **get_preset(filetype="gltf"))
        else:           
            print("Extension %r is not known!" % ext)
        create_export_path_property()
        bpy.data.scenes['Scene']["export_path"] = str(argv[0])

        # Get the default export preset from addon preferences
        # Use the actual addon name "fast_export_import" instead of __package__
        addon_prefs = bpy.context.preferences.addons["fast_export_import"].preferences
        default_export_preset_name = addon_prefs.default_export_preset

        if default_export_preset_name: # Check if a default preset is selected
            bpy.data.scenes['Scene']["export_preset"] = default_export_preset_name
        else:
            # Fallback to the first FBX preset if no default is set in preferences
            fbx_export_presets = preset_manager.get_operator_presets(preset_type='export_scene.fbx')
            if fbx_export_presets:
                first_fbx_preset_name = fbx_export_presets[0]["preset_name"]
                bpy.data.scenes['Scene']["export_preset"] = f"Fbx: {first_fbx_preset_name}"
            else:
                print("No FBX export presets found and no default set in preferences.")


    if not argv:
        print("No files passed")

if __name__ == "__main__":
    import_file()