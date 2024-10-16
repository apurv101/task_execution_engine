import os
import argparse
from pathlib import Path
import sys

try:
    import pathspec
except ImportError:
    print("The 'pathspec' library is required to run this script.")
    print("Please install it using: pip install pathspec")
    sys.exit(1)

# Code from print_tree.py
def load_gitignore(gitignore_path):
    if not gitignore_path.is_file():
        return None

    with gitignore_path.open('r') as f:
        patterns = f.read().splitlines()

    spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    return spec

def print_tree(startpath, root_path, spec=None, prefix="", file_handle=None, visited=None):
    if visited is None:
        visited = set()

    real_path = startpath.resolve()
    if real_path in visited:
        line = prefix + "└── [Symbolic Link to " + str(real_path) + "]"
        print(line)
        if file_handle:
            file_handle.write(line + "\n")
        return
    visited.add(real_path)

    try:
        entries = sorted(startpath.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        line = prefix + "└── [Permission Denied]"
        print(line)
        if file_handle:
            file_handle.write(line + "\n")
        return

    # Exclude specific directories and files
    exclude = [
        ".git",
        "prompt_context.txt",
        "directory_structure.txt",
        "context_creator.py",
        "venv",
    ]
    entries = [e for e in entries if e.name not in exclude]
    
    if spec:
        entries = [e for e in entries if not spec.match_file(str(e.relative_to(root_path)))]

    entries_count = len(entries)
    for index, entry in enumerate(entries):
        is_last = index == entries_count - 1
        connector = "└── " if is_last else "├── "
        line = prefix + connector + entry.name

        print(line)
        if file_handle:
            file_handle.write(line + "\n")

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_tree(entry, root_path, spec, prefix + extension, file_handle, visited)

def concatenate_files(input_files, output_file):
    try:
        with open(output_file, 'a') as outfile:
            outfile.write("\n\n--- File Contents Below ---\n\n")
            for file_name in input_files:
                with open(file_name, 'r') as infile:
                    outfile.write(f"{file_name} -->\n")
                    outfile.write(infile.read())
                    outfile.write("\n\n")
                    outfile.write("---This file ends here---\n\n")
        print(f"All files concatenated successfully into {output_file}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Step 1: Print the directory tree and save it to the output file
    startpath = Path(os.getcwd()).resolve()
    output_file = 'prompt_context.txt'
    gitignore_path = startpath / ".gitignore"

    spec = load_gitignore(gitignore_path)

    header = str(startpath)
    print(header)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(header + "\n")
            print_tree(startpath, startpath, spec=spec, file_handle=f)
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")
        sys.exit(1)

    # Step 2: Concatenate file contents into the same output file
    input_files = [
        # 'action_history.py',
        # 'actions_test.txt',
        # 'context_creator.py',
        # 'llm_interface.py',
        # 'new_llm_interface.py',
        # 'new_prompt_test.txt',
        # 'new_test_action_interface.py',
        # 'readme.md',
        # 'requirements.txt',
        'sample_prompts.py',
        # 'test_action_interface.py',
        # 'test_tasks.py',
        # 'test_vision_system.py',
        # 'vision_system.py',
        'main_server.py',
        'vision_system_backend.py',
        'llm_interface_backend.py',
        'visualize.py',
        'action_executor.py',
    ]
    concatenate_files(input_files, output_file)

if __name__ == "__main__":
    main()