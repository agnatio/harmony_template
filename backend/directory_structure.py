import os


def list_files(
    startpath,
    remove_objects=["_delete/", "__pycache__", "alembic", "node_modules"],
    max_levels=None,
):
    # Initial display for the root directory
    print("./")

    for root, dirs, files in os.walk(startpath):
        for obj in remove_objects:
            if obj in dirs:
                dirs.remove(obj)

        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        if "_delete" in dirs:
            dirs.remove("_delete")

        if "alembic" in dirs:
            dirs.remove("alembic")

        level = root.replace(startpath, "").count(os.sep)

        # If max_levels is set, skip levels beyond it
        if max_levels is not None and level > max_levels:
            continue

        # Adjust the indentations using the new characters
        indent = " " * 4 * (level - 1) + "├── " if level > 0 else ""
        subindent = " " * 4 * level + "│   ├── "

        # Skip printing the root directory again
        if root != startpath:
            print("{}{}/".format(indent, os.path.basename(root)))

        for f in files:
            print("{}{}".format(subindent, f))


if __name__ == "__main__":
    remove_objects = ["venv", ".git"]

    list_files(".", max_levels=3, remove_objects=remove_objects)
