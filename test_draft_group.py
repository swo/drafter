from draft_file import *
from draft_group import *
import pytest
from datetime import date

def test_next_version_date():
    source = File("source.txt")
    drafts = [File(x) for x in ["2009-01-01_source.txt", "2000-01-01_source.txt", "2000-01-01_source-v2.txt"]]
    group = DraftGroup(source, drafts)
    assert group.next_draft_basename() == date.today().isoformat() + "_source.txt"

def test_next_version_number():
    draft_path = date.today().isoformat() + "_source-v5.txt"
    new_path = date.today().isoformat() + "_source-v6.txt"
    group = DraftGroup(File("source.txt"), [File(draft_path)])
    assert group.next_draft_basename() == new_path
