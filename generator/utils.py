import os

def get_directory_structure(path=".", ignore_dirs=["node_modules", ".git", "__pycache__"]):
    """Genera una estructura del directorio del proyecto."""
    tree = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root)
        if folder_name in ignore_dirs:
            continue
        tree += f"{indent}- {folder_name}/\n"
        sub_indent = "  " * (level + 1)
        for f in files:
            tree += f"{sub_indent}- {f}\n"
    return tree
