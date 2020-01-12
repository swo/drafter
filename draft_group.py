import argparse, os, os.path, shutil, sys, re
from datetime import date


class DraftGroup:
    def __init__(self, source, drafts):
        self.source = source
        self.drafts = drafts
        self.latest_draft = sorted(self.drafts, key=lambda x: (x.date, x.version))[-1]
        self.next_draft_basename = self.latest_draft.next_draft_basename()
        self.new_draft_is_required = self.source.hash != self.latest_draft.hash
