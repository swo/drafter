from draft_file import *
from draft_group import *
from test_draft_file import tempdir, write_file
import pytest, tempfile, os.path
from datetime import date

def test_next_version_date(tempdir):
    source_path = write_file(tempdir, "source.txt", "source file contents")
    draft_names = ["2009-01-01_source.txt", "2000-01-01_source.txt", "2000-01-01_source-v2.txt"]
    draft_paths = [write_file(tempdir, x, "draft file contents") for x in draft_names]

    source = File(source_path)
    drafts = [File(x) for x in draft_paths]
    group = DraftGroup(source, drafts)
    assert group.next_draft_basename == date.today().isoformat() + "_source.txt"

def test_next_version_number(tempdir):
    source_path = write_file(tempdir, "source.txt", "source contents")
    draft_path = write_file(tempdir, date.today().isoformat() + "_source-v5.txt", "draft contents")
    new_path = date.today().isoformat() + "_source-v6.txt"

    group = DraftGroup(File(source_path), [File(draft_path)])
    assert group.next_draft_basename == new_path

def test_new_draft_no(tempdir):
    source_path = write_file(tempdir, "source.txt", "identical contents")
    draft_path = write_file(tempdir, "1918-04-14_source-v5.txt", "identical contents")
    group = DraftGroup(File(source_path), [File(draft_path)])

    assert not group.new_draft_is_required
