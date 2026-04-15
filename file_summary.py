#!/usr/bin/env python3
"""
file_summary.py

Recursively lists all files under a given directory (default: current script's
directory) and prints a summary table with file paths, sizes, and totals.
"""

import os
import sys


def human_readable_size(size_bytes: int) -> str:
    """Convert a byte count into a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def list_files(root_dir: str) -> list[tuple[str, int]]:
    """
    Walk *root_dir* recursively and return a list of (relative_path, size_bytes)
    tuples for every file found, sorted by relative path.
    """
    results = []
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0
            rel_path = os.path.relpath(full_path, root_dir)
            results.append((rel_path, size))
    results.sort(key=lambda x: x[0])
    return results


def print_summary(root_dir: str) -> None:
    """Print a formatted file listing and summary for *root_dir*."""
    files = list_files(root_dir)

    col_path  = 60
    col_size  = 12

    header = f"{'File Path':<{col_path}} {'Size':>{col_size}}"
    divider = "-" * len(header)

    print(f"\nFile summary for: {os.path.abspath(root_dir)}")
    print(divider)
    print(header)
    print(divider)

    total_bytes = 0
    for rel_path, size in files:
        total_bytes += size
        print(f"{rel_path:<{col_path}} {human_readable_size(size):>{col_size}}")

    print(divider)
    print(f"{'Total files:':<{col_path}} {len(files):>{col_size}}")
    print(f"{'Total size:':<{col_path}} {human_readable_size(total_bytes):>{col_size}}")
    print()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/workspace/repo"
    if not os.path.isdir(target):
        print(f"Error: '{target}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)
    print_summary(target)
