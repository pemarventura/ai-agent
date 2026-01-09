import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(target_file):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')
        
        if not file_path.endswith(".py"):
            raise Exception(f'Error: "{file_path}" is not a Python file')
        
        command = ["python", target_file]

        if args:
            command = command.extend(args)

        complete_process_obj = subprocess.run(args=command, cwd=os.path.dirname(target_file) ,capture_output=True ,timeout=30, text=True)   

        output_string = ""

        if complete_process_obj.returncode != 0:
            output_string += f"Process exited with code {complete_process_obj.returncode}"
        
        if complete_process_obj.stdout == "" and complete_process_obj.stderr == "":
            output_string += " No output produced"
        else:
            output_string += F"STDOUT:{complete_process_obj.stdout}"
            output_string += F"STDERR:{complete_process_obj.stderr}"
        
        return output_string

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
