import os
import bpy
import json
import sys

addon_dir = os.path.dirname(os.path.abspath(__file__))
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

import preset_manager

def create_export_path_property():
    bpy.types.Scene.export_path = bpy.props.StringProperty(
        name="Export Path",
        default="",
        subtype='FILE_PATH',
    )

def import_file():
    from sys import argv
    argv = argv[argv.index("--") + 1:]
    bpy.context.preferences.view.show_splash = False
    for f in argv:
        ext = os.path.splitext(f)[1].lower()
        
        create_export_path_property()
        bpy.data.scenes['Scene']["export_path"] = str(argv[0])

        if ext == ".fbx":
            base_builtin_fbx_kwargs = {'filepath': f}
            base_better_fbx_kwargs = {
                'filepath': f,
                'files': [{'name': os.path.basename(f), 'path': f}]
            }

            addon_prefs = bpy.context.preferences.addons["fast_export_import"].preferences
            default_import_preset_name = addon_prefs.default_import_preset
            import_preset_tree = preset_manager.get_preset_tree(is_export=False)

            use_better_fbx_addon = 'better_fbx' in [addon.module for addon in bpy.context.preferences.addons]
            
            is_better_fbx_preset_selected_in_prefs = False
            
            selected_preset_kwargs = {}
            selected_preset_operator_id = None

            if default_import_preset_name and default_import_preset_name in import_preset_tree:
                selected_preset_info = import_preset_tree[default_import_preset_name]
                selected_preset_operator_id = selected_preset_info["preset_operator"]
                selected_preset_kwargs = selected_preset_info["kwargs"].copy()
                
                selected_preset_kwargs.pop('filepath', None)
                selected_preset_kwargs.pop('directory', None) 
                selected_preset_kwargs.pop('filter_glob', None)
                selected_preset_kwargs.pop('files', None)

                better_fbx_prefix = preset_manager.import_types.get('better_import.fbx', '')
                is_better_fbx_preset_selected_in_prefs = default_import_preset_name.startswith(better_fbx_prefix)
            
            if is_better_fbx_preset_selected_in_prefs:
                # Case 1: User explicitly selected a Better FBX preset in addon preferences.
                if use_better_fbx_addon:
                    # Combine base Better FBX kwargs with selected preset's specific kwargs
                    final_better_fbx_kwargs = base_better_fbx_kwargs.copy()
                    final_better_fbx_kwargs.update(selected_preset_kwargs)
                    try:
                        bpy.ops.better_import.fbx(**final_better_fbx_kwargs)
                        #print(f"Imported {f} using selected Better FBX preset: {default_import_preset_name}")
                    except Exception as e: 
                        raise RuntimeError(f"Failed to import FBX using selected Better FBX preset '{default_import_preset_name}': {e}")
                else:
                    # User selected Better FBX preset but addon is not enabled.
                    raise RuntimeError(f"Better FBX preset '{default_import_preset_name}' selected, but Better FBX Importer addon is not enabled.")
            else:
                # Case 2: No specific Better FBX preset selected, or a built-in preset is selected.
                # Try built-in FBX importer first.
                final_builtin_fbx_kwargs = base_builtin_fbx_kwargs.copy()
                # If the selected preset was a built-in one, apply its kwargs to the built-in importer
                if selected_preset_operator_id == 'import_scene.fbx':
                    final_builtin_fbx_kwargs.update(selected_preset_kwargs)

                try:
                    bpy.ops.import_scene.fbx(**final_builtin_fbx_kwargs)
                    #print(f"Imported {f} using built-in FBX importer.")
                except RuntimeError as e: # Built-in importer failed (e.g., ASCII FBX)
                    print(f"Built-in FBX import failed for {f}: {e}. Attempting Better FBX as fallback if enabled.")
                    if use_better_fbx_addon:
                        # For fallback, use the default Better FBX kwargs (no specific Better FBX preset was selected).
                        fallback_better_fbx_kwargs = base_better_fbx_kwargs.copy()
                        try:
                            bpy.ops.better_import.fbx(**fallback_better_fbx_kwargs)
                            print(f"Imported {f} using Better FBX (fallback).")
                        except Exception as e_better_fbx:
                            raise RuntimeError(f"Failed to import FBX with both built-in and Better FBX (fallback): {e_better_fbx}")
                    else:
                        # Built-in failed, and Better FBX is not enabled as a fallback.
                        raise RuntimeError(f"Failed to import FBX with built-in importer, and Better FBX is not enabled as a fallback: {e}")
        # Add other file types (e.g., glTF/GLB) here if needed.
        else:           
            print("Extension %r is not known!" % ext)

        # Handle export preset
        try:
            addon_prefs = bpy.context.preferences.addons["fast_export_import"].preferences
            default_export_preset_name = addon_prefs.default_export_preset
            if default_export_preset_name:
                bpy.data.scenes['Scene']["export_preset"] = default_export_preset_name
            else:
                fbx_export_presets = preset_manager.get_operator_presets(preset_type='export_scene.fbx')
                if fbx_export_presets:
                    first_fbx_preset_name = fbx_export_presets[0]["preset_name"]
                    bpy.data.scenes['Scene']["export_preset"] = f"Fbx: {first_fbx_preset_name}"
                else:
                    print("No FBX export presets found and no default set in preferences.")
        except KeyError:
            print("Fast Import Export addon preferences not found. Falling back to default FBX export preset search.")
            fbx_export_presets = preset_manager.get_operator_presets(preset_type='export_scene.fbx')
            if fbx_export_presets:
                first_fbx_preset_name = fbx_export_presets[0]["preset_name"]
                bpy.data.scenes['Scene']["export_preset"] = f"Fbx: {first_fbx_preset_name}"
            else:
                print("No FBX export presets found.")


    if not argv:
        print("No files passed")

if __name__ == "__main__":
    import_file()