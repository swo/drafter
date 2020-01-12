from draft_file import File
import argparse, os, os.path, shutil, sys, re
from datetime import date


class DraftGroup:
    """A source file and its associated draft files"""

    def __init__(self, source, drafts):
        self.source = source
        self.drafts = drafts

        if self.drafts == []:
            self.latest_draft = None
            self.next_draft_basename = f"{date.today().isoformat()}_{self.source.basename}"
            self.new_draft_is_required = True
        else:
            self.latest_draft = sorted(self.drafts, key=lambda x: (x.date, x.version))[-1]
            self.next_draft_basename = self.latest_draft.next_draft_basename()

    def new_draft_is_required(self):
        return not self.source.identical_contents_to(self.latest_draft)

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
    drafts = [File(x.name) for x in os.scandir(drafts_dir) if x.is_file()]
    return group_files(sources, drafts)
