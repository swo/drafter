from draft_file import *
import pytest, tempfile, os, os.path

@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as tempdir:
        yield tempdir

def write_file(tempdir, name, contents):
    path = os.path.join(tempdir, name)
    with open(path, "w") as f:
        f.write(contents)

    return path

def test_draft_parsing(tempdir):
    path = write_file(tempdir, "2019-01-05_file.txt", "contents")

    x = File(path)
    assert x.is_draft
    assert x.name == "file.txt"
    assert x.date == "2019-01-05"
    assert x.version == 1
    assert x.exists

def test_draft_parsing_version():
    x = File("drafts/2019-01-05_foo-v2.docx")
    assert x.name == "foo.docx"
    assert x.date == "2019-01-05"
    assert x.version == 2
    assert not x.exists

def test_not_draft():
    assert not File("drafts/foo.docx").is_draft

def test_hash(tempdir):
    path1 = write_file(tempdir, "source.txt", "same file contents")
    path2 = write_file(tempdir, "draft.txt", "same file contents")

    assert File.digest_file(path1) == File.digest_file(path2)

def test_hash_no(tempdir):
    path1 = write_file(tempdir, "source.txt", "same file contents")
    path2 = write_file(tempdir, "draft.txt", "different file contents")

    assert File.digest_file(path1) != File.digest_file(path2)

def test_match():
    assert File("2019-01-01_foo.docx").is_draft_of(File("foo.docx"))

def test_match_bad():
    assert not File("2019-01-01_foo.docx").is_draft_of(File("bar.docx"))
