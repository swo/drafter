import argparse, os, os.path, shutil, sys, re
from datetime import date


class DraftGroup:
    def __init__(self, source, drafts):
        self.source = source
        self.drafts = drafts

    def next_draft_basename(self):
        return sorted(self.drafts, key=lambda x: (x.date, x.version))[-1].next_draft_basename()
