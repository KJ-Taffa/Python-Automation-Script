#!/usr/bin/env python3
"""
sort_backup.py

Scan a source directory, create a timestamped backup (zip) of the whole source,
and then organize files into type-based subdirectories under a "sorted" folder.

Usage:
    python sort_backup.py [--source PATH] [--mode move|copy] [--no-recursive] [--dry-run]

Defaults:
    source = current working directory
    mode = move (use 'copy' to keep originals)
    recursive = True
"""

import argparse
import os
import shutil
import sys
from datetime import datetime

EXT_MAP = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt", ".rtf"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "video": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"},
    "archives": {".zip", ".tar", ".gz", ".tgz", ".bz2", ".7z", ".rar"},
    "code": {".py", ".js", ".java", ".c", ".cpp", ".h", ".cs", ".rb", ".go", ".rs", ".php", ".html", ".css"},
}

DEFAULT_CATEGORY = "others"
SORTED_DIRNAME = "sorted"
BACKUPS_DIRNAME = "backups"

def category_for_ext(ext: str) -> str:
    ext = ext.lower()
    for cat, exts in EXT_MAP.items():
        if ext in exts:
            return cat
    return DEFAULT_CATEGORY

def safe_move_or_copy(src_path, dst_dir, mode, dry_run=False):
    os.makedirs(dst_dir, exist_ok=True)
    name = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, name)
    base, ext = os.path.splitext(name)
    counter = 1
    while os.path.exists(dst_path):
        dst_path = os.path.join(dst_dir, f"{base}_{counter}{ext}")
        counter += 1
    if dry_run:
        print(f"[DRY] {mode} {src_path} -> {dst_path}")
        return dst_path
    if mode == "move":
        return shutil.move(src_path, dst_path)
    else:
        shutil.copy2(src_path, dst_path)
        return dst_path

def create_backup_zip(source_dir, backups_dir):
    os.makedirs(backups_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.join(backups_dir, f"backup_{ts}")
    # shutil.make_archive will add .zip
    archive_path = shutil.make_archive(base_name, 'zip', root_dir=source_dir)
    return archive_path

def parse_args():
    p = argparse.ArgumentParser(description="Backup and sort files by type.")
    p.add_argument("--source", "-s", default=".", help="Source directory to process (default: current dir)")
    p.add_argument("--mode", "-m", choices=("move", "copy"), default="move", help="Move files (default) or copy")
    p.add_argument("--no-recursive", action="store_true", help="Do not scan subdirectories")
    p.add_argument("--dry-run", action="store_true", help="Show actions without performing them")
    return p.parse_args()

def main():
    args = parse_args()
    source = os.path.abspath(args.source)
    if not os.path.isdir(source):
        print("Source is not a directory:", source)
        sys.exit(1)

    parent = os.path.dirname(source)
    backups_dir = os.path.join(parent, BACKUPS_DIRNAME)
    sorted_dir = os.path.join(source, SORTED_DIRNAME)

    # Create backup of the entire source directory (placed beside the source in "backups/")
    print("Creating backup...")
    backup_zip = create_backup_zip(source, backups_dir)
    print("Backup created:", backup_zip)

    # Walk files and sort
    print("Scanning and sorting files...")
    moved = 0
    copied = 0
    skipped = 0

    for root, dirs, files in os.walk(source):
        # Optionally skip subdirectories by preventing walk from descending
        if args.no_recursive and root != source:
            continue

        # Skip the backups folder and sorted folder inside the source to avoid moving them
        if os.path.abspath(root).startswith(os.path.abspath(backups_dir)):
            continue
        if os.path.abspath(root).startswith(os.path.abspath(sorted_dir)):
            continue

        for fname in files:
            fpath = os.path.join(root, fname)
            # Skip the backup archive we just created if placed under the source parent but not inside source.
            # Also skip the script itself if located inside source.
            if os.path.abspath(fpath) == os.path.abspath(backup_zip):
                skipped += 1
                continue

            # Skip if file is inside backups dir or sorted dir
            if os.path.commonpath([fpath, backups_dir]) == os.path.abspath(backups_dir):
                skipped += 1
                continue
            if os.path.commonpath([fpath, sorted_dir]) == os.path.abspath(sorted_dir):
                skipped += 1
                continue

            # Determine category by extension
            _, ext = os.path.splitext(fname)
            cat = category_for_ext(ext)
            target_dir = os.path.join(sorted_dir, cat)

            try:
                dst = safe_move_or_copy(fpath, target_dir, args.mode, dry_run=args.dry_run)
                if args.dry_run:
                    # counts not incremented for dry run
                    pass
                else:
                    if args.mode == "move":
                        moved += 1
                    else:
                        copied += 1
            except Exception as e:
                print("Error processing", fpath, "->", e)
                skipped += 1

    print("Done.")
    if not args.dry_run:
        print(f"Moved: {moved}  Copied: {copied}  Skipped: {skipped}")
        print("Sorted files live in:", sorted_dir)
        print("Backups live in:", backups_dir)
    else:
        print("Dry run finished. No files were changed.")

if __name__ == "__main__":
    main()