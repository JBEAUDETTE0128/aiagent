import os

def get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))
    valid_target = os.path.commonpath([working_directory_abs, target_directory]) == working_directory_abs
    
    
    if not valid_target:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    contents_list = []
    for item in os.listdir(target_directory):
        try:
            name = item
            size = os.path.getsize(os.path.join(target_directory, item))
            is_dir = os.path.isdir(os.path.join(target_directory, item))
            contents_list.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        except:
            return "Error: Invalid Value"
    final_list = '\n'.join(contents_list)
    return final_list