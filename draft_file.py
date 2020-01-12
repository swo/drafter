import argparse, os, os.path, shutil, sys, re, hashlib
from datetime import date


class File:
    regex = re.compile("(?P<date>\\d{4}-\\d{2}-\\d{2})_(?P<prefix>[^.]+?)(-v(?P<version>\\d+))?\\.(?P<extension>.+)")

    def __init__(self, path):
        self.path = path
        self.basename = os.path.basename(self.path)

        m = self.regex.fullmatch(self.basename)
        self.is_draft = m is not None

        if self.is_draft:
            self.date = m.group("date")

            self.prefix = m.group("prefix")
            self.extension = m.group("extension")
            self.name = self.prefix + "." + self.extension

            if m.group("version") is None:
                self.version = 1
            else:
                self.version = int(m.group("version"))
        else:
            self.name = self.basename

    def identical_contents_to(self, other):
        return self.digest_file(self.path) == self.digest_file(other.path)

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

    def is_draft_of(self, source):
        return self.is_draft and not source.is_draft and self.name == source.name

    def next_draft_basename(self):
        today = date.today().isoformat()

        if self.date == today:
            # increment version
            return f"{today}_{self.prefix}-v{self.version + 1}.{self.extension}"
        else:
            # increment date only
            return f"{today}_{self.prefix}.{self.extension}"
