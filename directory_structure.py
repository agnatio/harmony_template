import os


def list_files(
    startpath,
    output_file,
    remove_objects=[
        "_delete/",
        "__pycache__",
        "alembic",
        "node_modules",
        ".pytest_cache",
    ],
    max_levels=None,
):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("./\n")  # Initial display for the root directory

        for root, dirs, files in os.walk(startpath):
            for obj in remove_objects:
                if obj in dirs:
                    dirs.remove(obj)

            level = root.replace(startpath, "").count(os.sep)

            # If max_levels is set, skip levels beyond it
            if max_levels is not None and level > max_levels:
                continue

            # Adjust the indentations using the new characters
            indent = " " * 4 * (level - 1) + "├── " if level > 0 else ""
            subindent = " " * 4 * level + "│   ├── "

            # Skip printing the root directory again
            if root != startpath:
                f.write("{}{}/\n".format(indent, os.path.basename(root)))

            for file in files:
                f.write("{}{}\n".format(subindent, file))


if __name__ == "__main__":
    remove_objects = [
        "venv",
        ".git",
        "node_modules",
        "__pycache__",
        "alembic",
        ".pytest_cache",
    ]
    output_file = "folders.txt"

    list_files(".", output_file, max_levels=3, remove_objects=remove_objects)
