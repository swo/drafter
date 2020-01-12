import argparse, os, os.path, shutil, sys, re, hashlib
from datetime import date


class File:
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
        else:
            self.name = self.basename

        self.exists = os.path.isfile(self.path)
        if self.exists:
            self.hash = self.digest_file(self.path)

    @classmethod
    def parse_path(cls, path):
        date_name_match = cls.date_name_regex.fullmatch(path)
        version_match = re.fullmatch("(?P<prefix>.*)-v(?P<version>\\d+)\\.(?P<extension>.+)", date_name_match.group("name_and_version"))

        date = date_name_match.group("date")

        if version_match is None:
            name = date_name_match.group("name_and_version")
            version = 0
        else:
            name = version_match.group("prefix") + "." + version_match.group("extension")
            version = int(version_match.group("version"))

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

    def is_draft_of(self, other):
        return self.is_draft and not other.is_draft and self.name == other.name
