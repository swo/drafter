#!/usr/bin/env python3

import draft

import argparse, os, os.path, shutil, sys, re, hashlib
from datetime import date


class Draft:
    date_name_regex = re.compile("(?P<date>\\d{4}-\\d{2}-\\d{2})_(?P<name_and_version>.+)")

    def __init__(self, path):
        self.path = path
        self.basename = os.path.basename(self.path)
        self.is_draft = self.date_name_regex.fullmatch(self.basename) is not None

        if self.is_draft:
            path_parts = self.parse_path(self.basename)
            self.name = path_parts["name"]
            self.date = path_parts["date"]
            self.version = path_parts["version"]

            self.hash = self.digest_file(self.path)

    @classmethod
    def parse_path(cls, path):
        date_name_match = cls.date_name_regex.fullmatch(path)
        version_match = re.fullmatch("(?P<prefix>.*)-v(?P<version>\\d+)\.(?P<extension>.+)", date_name_match.group("name_and_version"))

        date = date_name_match.group("date")

        if version_match is None:
            name = date_name_match.group("name_and_version")
            version = None
        else:
            name = version_match.group("prefix") + "." + version_match.group("extension")
            version = version_match.group("version")

        return {"name": name, "date": date, "version": version}


    @staticmethod
    def digest_file(path):
        h = hashlib.md5()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(h.block_size)
                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()


def infer_files_to_copy(source_directory, draft_directory):
    """Look for filenames in common between source and draft directories"""
    source_names = set([x.name for x in os.scandir(source_directory)])

    drafts = [Draft(x.path) for x in os.scandir(draft_directory)]
    draft_names = set([x.name for x in drafts if x.is_draft])

    return source_names.intersection(draft_names)


if __name__ == "__main__":
    p = argparse.ArgumentParser("Copy dates files to a drafts/ folder")
    p.add_argument("files", nargs="*", help="File(s) to copy")
    p.add_argument("-f", "--force", action="store_true", help="Overwrite same-date files?")
    p.add_argument("-d", "--directory", default="drafts", help="Destination directory")
    p.add_argument("-q", "--quiet", action="store_true", help="Don't show source and destination?")

    args = p.parse_args()

    if not os.path.isdir(args.directory):
        raise RuntimeError(f"Destination folder '{args.directory}' does not exist")

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
