from .draft_file import File
import argparse, os, os.path, shutil, sys, re
from datetime import date


class DraftGroup:
    """A source file and its associated draft files"""

    def __init__(self, source, drafts):
        self.source = source
        self.drafts = drafts

        if len(self.drafts) == 0:
            self.latest_draft = None
            self.next_draft_basename = f"{date.today().isoformat()}_{self.source.basename}"
        else:
            self.latest_draft = sorted(self.drafts, key=lambda x: (x.date, x.version))[-1]
            self.next_draft_basename = self.latest_draft.next_draft_basename()

    def __repr__(self):
        drafts_repr = ", ".join([repr(x) for x in self.drafts])
        return f"DraftGroup({repr(self.source)}, [{drafts_repr}])"

    def drafts_up_to_date(self):
        if len(self.drafts) == 0:
            raise RuntimeError(f"Draft group {repr(self)} has no drafts")
        else:
            return self.source.identical_contents_to(self.latest_draft)

    def update_src_dest(self, drafts_dir):
        return (self.source.path, os.path.join(drafts_dir, self.next_draft_basename))

def group_files(sources, drafts):
    """Figure out which draft files go with which source files"""
    return [DraftGroup(source, [draft for draft in drafts if draft.is_draft_of(source)]) for source in sources]

def find_groups(source_dir, drafts_dir):
    # check that the directories exist
    if not os.path.isdir(source_dir):
        raise RuntimeError(f"Source folder '{source_dir}' does not exist")

    if not os.path.isdir(drafts_dir):
        raise RuntimeError(f"Destination folder '{drafts_dir}' does not exist")

    # get the source and draft files
    sources = [File(x.name) for x in os.scandir(source_dir) if x.is_file()]
    drafts = [File(os.path.join(drafts_dir, x.name)) for x in os.scandir(drafts_dir) if x.is_file()]
    return group_files(sources, drafts)
