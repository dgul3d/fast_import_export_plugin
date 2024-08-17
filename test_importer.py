import json
from pprint import pprint
filename = "presets.json"
def get_json(file_path):
    try:
        with open(file_path) as file:
            data = json.load(file)
    except FileNotFoundError:
        return "File not found"
    except json.JSONDecodeError:
        return "Invalid JSON format"
    return data

def get_preset_values(preset_identifier):
    for filetype, directions in get_json(filename).items():
        for direction, tools in directions.items():
            for tool, presets in tools.items():
                for preset_name, preset_info in presets.items():
                    if '_'.join([filetype, direction, tool, preset_name]) == preset_identifier:
                        return preset_info.get("values", "")
                    
def get_preset(filetype, direction, tool, preset):
    return dict(get_json(filename)[filetype][direction][tool][preset])

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


if __name__ == "__main__":
    data = get_preset_tree("export")