import os

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            raise Exception(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(target_file):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        
        contents = ""

        MAX_CHARS = 10000

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            contents += file_content_string

            # After reading the first MAX_CHARS...
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return contents

    except Exception as e:
        return str(e)