# Fast Import Export Plugin

Import FBX files in Blender by clicking on them, edit them, and save them in one click. Designed for Unity-Blender-Unity workflows.

![fast_import_export_usage](https://github.com/dgul3d/fast_import_export_plugin/assets/64034875/c59b2556-4cd6-4bc0-9fc4-36c181a58518)

### Installation

1.  Download this repository as a zip and install it via `Edit > Preferences > Add-ons > Install`.
2.  In the addon preferences, click `Open Addon Folder`.
3.  Change the `.fbx` file association to `blender_to_os.bat`. To do this, right-click any `.fbx` file, click `Properties`, and change the `Opens with` preference. Click on `more apps↓`, scroll down and select `Look for another app on this PC`. In the explorer window, navigate to your `fast_export_import` addon location and choose `blender_to_os.bat`. You can copy the path location from the explorer window opened in step 2.

    For convenience, this addon is provided with a `test_cube.fbx` file. Use it for setting the file association.
4.  Test the addon by opening `test_cube.fbx`. It should almost immediately open in a new Blender instance without a splash screen.

### Usage

This addon is designed for fast FBX file modification and greatly benefits workflows involving multiple software, such as the `Blender to Unity` pipeline.

You can open FBX files from Windows Explorer, the Unity Project window, or the Unity inspector (by double-clicking on a mesh field).

![ways_to_open_fbx](https://github.com/dgul3d/fast_import_export_plugin/assets/64034875/34b6a55c-314d-4ab6-8e53-b41af8759e33)

Edit imported objects, select those you want to export, and click the `Export` button at the top-left corner of the 3D view. The new FBX file containing the selected objects will overwrite the old one at its original location.

### Default Presets in Addon Properties

The addon now supports setting **default import and export presets** directly within its preferences. This allows you to define how FBX files are imported and exported without needing to re-select a preset every time.

To access these settings:
1. Go to `Edit > Preferences > Add-ons`.
2. Find "Fast Import Export" and expand its settings.
3. You will find dropdown menus for "Default Export Preset" and "Default Import Preset".

Choose your preferred presets here. If no default import preset is selected, or if the selected preset fails, the addon will intelligently fall back to a suitable import method.

![fast_import_export_settings](https://github.com/user-attachments/assets/570edb41-1b44-420f-b7ca-e75b2a5a3516)

#### Import

**ASCII FBX Support:**
The addon is now capable of opening **ASCII FBX files**. If the built-in Blender FBX importer fails to open an FBX file (which typically happens with ASCII FBX), the addon will automatically attempt to use the **Better FBX Importer** if it is installed and enabled in Blender. This ensures broader compatibility with various FBX file types. You can also explicitly set a Better FBX import preset as your default in the addon preferences.

#### Export
1. [Optional] Change save location by clicking on a `folder` button. Default value is the same as the original file location.
2. [Optional] Change export preset from the list of your operator presets by clicking on a `cog` button. Default value is set from the addon properties.
3. Click the `export` button.
   
![fast_import_export_process](https://github.com/user-attachments/assets/035c4fb3-b4c0-4586-a651-4114ac1051db)

### Limitations

* **Default Export Preset Assumptions:** The default export preset assumes no space transforms and no additional transform baking. In a `Blender to Unity` pipeline, this means you might need to manually rotate meshes or parent empties by 90 degrees on the X-axis in Blender for them to be positioned properly in Unity. This approach allows for free modification of the FBX file later and enables cascading multiple edits without introducing space transforms at each step.
* **Platform Support:** Mac and Linux support are not implemented yet. There are some Mac integration snippets in the corresponding folder if you want to explore using Automator.

### Technical Notes

This addon works by opening mesh file types with a custom script. It invokes `bpy.ops.import_scene.fbx()` (or `bpy.ops.better_import.fbx()` as fallback/default) at Blender's startup, passing the path to the file. The `path_to_file` is saved in a string-type scene custom property named `export_path`.

On `Export` button click, the mesh file is exported to `export_path`, which essentially overwrites it with a new version at the original location.

![image](https://github.com/dgul3d/fast_import_export_plugin/assets/64034875/6a03f4e6-0b2b-4778-bb7c-ee8a9a79f987)

Every opened FBX file invokes a separate Blender instance. This is intentional behavior and is meant to facilitate an "edit-save-and-forget" methodology. If the user is done editing and exports a new FBX file version, they can close Blender without saving the `.blend` file. If there's a need to change this file again, the user can re-import that file by simply opening it in Blender.

Note that if any heavy memory-demanding addons are installed, it will affect the speed at which each new Blender instance will be opened.
