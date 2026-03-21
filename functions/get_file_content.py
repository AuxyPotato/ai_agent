import os


def get_file_content(working_directory, file_path):
    if file_path is None:
        return f'Error: Cannot get "{file_path}" from "{working_directory}"'
    working_dir_abs = os.path.realpath(working_directory)
    target_file = os.path.realpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return (f'Error: Cannot read "{file_path}" as it is outside '
                f'the permitted working directory')
    elif not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, 'r') as f:
            max_chars = 10000
            file_content_string = f.read(max_chars)
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except FileNotFoundError:
        return f'Error: File "{file_path}" not found'
