#!/usr/bin/env python3

import draft_file, draft_group

import argparse, os, os.path, shutil, sys, re, hashlib
from datetime import date


if __name__ == "__main__":
    p = argparse.ArgumentParser("Copy dates files to a drafts/ folder")
    # p.add_argument("files", nargs="*", help="File(s) to copy")
    # p.add_argument("-f", "--force", action="store_true", help="Overwrite same-date files?")
    p.add_argument("-s", "--source_dir", default=".", help="Source file directory")
    p.add_argument("-d", "--drafts_dir", default="drafts", help="Destination directory")
    p.add_argument("-q", "--quiet", action="store_true", help="Don't show source and destination?")

    args = p.parse_args()

    # get the draft groups
    groups = draft_group.find_groups(args.source_dir, args.drafts_dir)

    print(groups)
    print([group.source.name for group in groups if group.new_draft_is_required])
    assert False
    

    # Infer files to read
    if len(args.files) == 0:
        files = infer_files_to_copy(os.getcwd(), args.directory)

        if len(files) == 0:
            raise RuntimeError("No candidate draft files found; specify manually")
        else:
            print("Candidate draft files found:")
            for x in files:
                print(" ", x)

            yn = input("Copy? [y/N] ").strip().lower()

            if yn == "y":
                args.files = files
            else:
                raise RuntimeError("Not copying")

    prefix = date.today().isoformat() + "_"
    dests = [os.path.join(args.directory, prefix + x) for x in args.files]

    if not args.quiet:
        for src, dest in zip(args.files, dests):
            print(f"{src} -> {dest}")

    conflicts = [x for x in dests if os.path.exists(x)]

    if len(conflicts) > 0 and not args.force:
        message = "Destination files already exist:\n" + "\n".join(["  " + x for x in conflicts])
        yn = input("Overwrite files? [y/N] ")

        if yn.strip().lower() != "y":
            raise RuntimeError("Destination files already exist")

    for src, dest in zip(args.files, dests):
        shutil.copy(src, dest)
