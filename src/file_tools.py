import os
import subprocess


def run_shell_command(command: str, dir: str):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=dir,
    )
    stdout, stderr = process.communicate()

    return stdout, stderr


def list_dir(dir_path: str):
    items = os.listdir(dir_path)
    if not items:
        return f"Directory '{dir_path}' is empty."

    result = f"Contents of directory '{dir_path}':\n"
    for item in items:
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            item_type = "Directory"
        else:
            item_type = "File"
        result += f"- {item} ({item_type})\n"

    return result.strip()


def edit_write_file(file_path: str, replace_content: str, new_content: str):
    if not os.path.exists(file_path) and replace_content == "":
        with open(file_path, "w") as f:
            f.write(new_content)
        return True
    elif os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
        if replace_content in content:
            updated_content = content.replace(replace_content, new_content)
            with open(file_path, "w") as f:
                f.write(updated_content)
            return True
    return False


def read_file(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return None
