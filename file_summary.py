"""
file_summary.py
Recursively lists all files in the repository and prints a summary
of file count and sizes.
"""

import os
import sys


def format_size(num_bytes: int) -> str:
    """Convert a byte count to a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def list_files(root: str):
    """Walk *root* and yield (relative_path, size_in_bytes) for every file."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories (e.g. .git)
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for filename in sorted(filenames):
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root)
            size = os.path.getsize(full_path)
            yield rel_path, size


def main():
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning: {os.path.abspath(repo_path)}\n")

    files = list(list_files(repo_path))

    if not files:
        print("No files found.")
        return

    # Determine column width for alignment
    max_path_len = max(len(p) for p, _ in files)

    print(f"{'File':<{max_path_len}}  {'Size':>10}")
    print("-" * (max_path_len + 13))

    total_size = 0
    for rel_path, size in files:
        print(f"{rel_path:<{max_path_len}}  {format_size(size):>10}")
        total_size += size

    print("-" * (max_path_len + 13))
    print(f"\nTotal files : {len(files)}")
    print(f"Total size  : {format_size(total_size)}")


if __name__ == "__main__":
    main()
