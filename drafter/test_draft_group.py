from draft_file import *
from draft_group import *
from test_draft_file import tempdir, write_file
import pytest, tempfile, os.path
from datetime import date

def test_repr():
    source = File("source.txt")
    draft_names = ["2009-01-01_source.txt", "2000-01-01_source.txt"]
    drafts = [File(x) for x in draft_names]
    group = DraftGroup(source, drafts)

    assert repr(group) == "DraftGroup(File('source.txt'), [File('2009-01-01_source.txt'), File('2000-01-01_source.txt')])"

def test_next_version_date():
    source = File("source.txt")
    draft_names = ["2009-01-01_source.txt", "2000-01-01_source.txt", "2000-01-01_source-v2.txt"]
    drafts = [File(x) for x in draft_names]

    group = DraftGroup(source, drafts)
    assert group.next_draft_basename == date.today().isoformat() + "_source.txt"

def test_next_version_number():
    draft_path = date.today().isoformat() + "_source-v5.txt"
    new_path = date.today().isoformat() + "_source-v6.txt"
    group = DraftGroup(File("source.txt"), [File(draft_path)])
    assert group.next_draft_basename == new_path

def test_next_version_no_drafts(tempdir):
    group = DraftGroup(File("source.txt"), [])
    assert group.next_draft_basename == date.today().isoformat() + "_source.txt"

def test_new_draft_no(tempdir):
    source_path = write_file(tempdir, "source.txt", "identical contents")
    draft_path = write_file(tempdir, "1918-04-14_source-v5.txt", "identical contents")
    group = DraftGroup(File(source_path), [File(draft_path)])

    assert not group.new_draft_is_required()

def test_grouping(tempdir):
    source_paths = [write_file(tempdir, x, "contents") for x in ["sourceA.txt", "sourceB.txt", "sourceC.txt"]]
    draft_paths = [write_file(tempdir, x, "contents") for x in ["2020-01-01_sourceA.txt", "1987-05-06_sourceB-v2.txt"]]
    sources = [File(x) for x in source_paths]
    drafts = [File(x) for x in draft_paths]

    groups = group_files(sources, drafts)
    group_dict = {group.source.basename: [x.basename for x in group.drafts] for group in groups}
    assert group_dict == {"sourceA.txt": ["2020-01-01_sourceA.txt"], "sourceB.txt": ["1987-05-06_sourceB-v2.txt"], "sourceC.txt": []}
