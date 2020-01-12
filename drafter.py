#!/usr/bin/env python3

from draft_file import File
from draft_group import DraftGroup, find_groups

import argparse, os.path, shutil

def infer_and_copy(source_dir, drafts_dir):
    groups = find_groups(source_dir, drafts_dir)
    nonempty_groups = [x for x in groups if len(x.drafts) > 0]
    up_to_date_groups = [x for x in nonempty_groups if x.drafts_up_to_date()]
    groups_to_update = [x for x in nonempty_groups if not x.drafts_up_to_date()]

    if len(nonempty_groups) == 0:
        sources = [x.source.basename for x in groups]
        raise RuntimeError(f"No draft files found for potential sources: {sources}")
    else:
        if len(up_to_date_groups) > 0:
            print("Up to date drafts:")
            for group in up_to_date_groups:
                draft_path = os.path.join(drafts_dir, group.latest_draft.path)
                print(f"  {group.source.path} == {draft_path}")

        if len(groups_to_update) == 0:
            print("All source files up to date")
        else:
            print("Drafts to update:")
            copies = [x.update_src_dest(drafts_dir) for x in groups_to_update]

            for src, dest in copies:
                print(f"  {src} -> {dest}")

                if os.path.exists(dest):
                    raise RuntimeError(f"Draft target {dest} exists")

            for src, dest in copies:
                shutil.copy(src, dest)

def copy_new_sources(sources, drafts_dir):
    groups = [DraftGroup(File(x), []) for x in sources]
    copies = [x.update_src_dest(drafts_dir) for x in groups]

    print("Drafts to initiate:")
    for src, dest in copies:
        print(f"  {src} -> {dest}")

        if os.path.exists(dest):
            raise RuntimeError(f"Draft target {dest} exists")

    for src, dest in copies:
        shutil.copy(src, dest)


if __name__ == "__main__":
    p = argparse.ArgumentParser("Copy dates files to a drafts/ folder")
    p.add_argument("files", nargs="*", help="New source files to set up")
    p.add_argument("-s", "--source_dir", default=".", help="Source file directory")
    p.add_argument("-d", "--drafts_dir", default="drafts", help="Destination directory")
    p.add_argument("-q", "--quiet", action="store_true", help="Don't show source and destination?")

    args = p.parse_args()

    if len(args.files) == 0:
        infer_and_copy(args.source_dir, args.drafts_dir)
    else:
        copy_new_sources(args.files, args.drafts_dir)
