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
            self.new_draft_is_required = self.source.hash != self.latest_draft.hash

def group_files(sources, drafts):
    """Figure out which draft files go with which source files"""
    return [DraftGroup(source, [draft for draft in drafts if draft.is_draft_of(source)]) for source in sources]
