import os

def generate_executable_bat(blender_work_path, blender_exe_path, addon_path, executable_bat_path):
    new_content = \
f"""\
@echo off
pushd "{blender_work_path}\\"
popd
"{blender_exe_path}" --python "{addon_path}\importer.py" -- %1
"""
    executable_bat_path = addon_path + "\\" + executable_bat_path
    # Check if the file already exists
    if os.path.exists(executable_bat_path):
        with open(executable_bat_path, 'r') as existing_file:
            existing_content = existing_file.read()
            
        # Compare existing content with new content
        if existing_content == new_content:
            return
    
    # Write new content to the file
    with open(executable_bat_path, 'w+') as file:
        file.write(new_content)
