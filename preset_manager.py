#https://blenderartists.org/t/using-fbx-export-presets-when-exporting-from-a-script/1162914
import bpy
import os

export_types={"better_export.fbx": "Better Fbx: ",
              "export_scene.fbx" : "Fbx: ",
              "export_scene.gltf": "Gltf: ",
              "wm.obj_export": "Obj: ",
              "wm.ply_export": "Ply: ",
              "wm.usd_export": "USD: "}

import_types={"better_import.fbx": "Better Fbx: ",
              "import_scene.fbx" : "Fbx: ",
              "import_scene.gltf": "Gltf: ",
              "wm.obj_import": "Obj: ",
              "wm.ply_import": "Ply: ",
              "wm.usd_import": "USD: "}

def get_operator_presets(preset_type = 'export_scene.fbx'):
    preset_operator = 'bpy.ops.'+preset_type
    preset_type = 'operator\\'+preset_type
    preset_list = [] 
    if bpy.utils.preset_paths(preset_type) == []:
        return
    parent_path = bpy.utils.preset_paths(preset_type)[0]
    presets = os.listdir(parent_path)
    for preset in presets:
        if preset.endswith(".py"):
            preset_name = os.path.splitext(preset)[0]
            preset_filepath = os.path.join(parent_path,preset)
            
            class Container(object):
                __slots__ = ('__dict__',)

            op = Container()
            with open(preset_filepath, 'r') as file:
                # storing the values from the preset on the class
                for line in file.readlines()[3::]:
                    # import presets contain garbage lines
                    if "=" in line and line.startswith("op."):
                        exec(line, globals(), locals())

                # pass class dictionary to the operator
                kwargs = op.__dict__
                
            preset_list.append({"preset_name" : preset_name, "preset_parms": {"preset_operator" : preset_operator,"kwargs": kwargs}})
    return preset_list

def get_preset_tree(is_export=True):
    preset_tree = {}
    if is_export:
        preset_types = export_types
    else:
        preset_types = import_types
    for preset_type in preset_types:
        preset_list = get_operator_presets(preset_type)
        if preset_list:
            for preset in preset_list: 
                preset["preset_name"] = preset_types[preset_type]+preset["preset_name"]
                preset_tree[preset["preset_name"]] = preset["preset_parms"]
    return preset_tree

def get_preset_items(is_export=True):
    list_of_preset_names = list(get_preset_tree(is_export).keys())
    preset_items = [(name,name,name) for name in list_of_preset_names]
    return preset_items

if __name__ == "__main__":
    export_preset = "Fbx: FBX_Default"
    #print(get_preset_tree(is_export=False))
    print(get_preset_tree(True))