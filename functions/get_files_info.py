import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):

    try:        
        working_dir_abs = os.path.abspath(working_directory)
        
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        # Will be True or False
        valid_directory = os.path.isdir(target_dir)

        if not valid_directory:
            raise Exception(f'Error: "{directory}" is not a directory')
        
        # List of target dir contents
        target_dir_contents = os.listdir(target_dir)

        contents = []

        for content in target_dir_contents:

            path = f"{target_dir}/{content}"
            
            file_name = content
            
            file_size = str(os.path.getsize(path))

            is_dir = str(os.path.isdir(path))

            contents.append(f"- {file_name}: file_size:{file_size} bytes, is_dir={is_dir}")

        return "\n".join(contents)

    except Exception as e:
        return str(e)
    
    

    
    

    pass
