import os


def get_file_content(working_directory, file_path):
    if file_path is None:
        return f'Error: Cannot get "{file_path}" from "{working_directory}"'
    else:
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            with open(absolute_file_path, 'r') as f:
                max_chars = 10000
                file_content_string = f.read(max_chars)
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
                return file_content_string

        except FileNotFoundError:
            return f'Error: File "{file_path}" not found'
