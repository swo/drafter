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
    f = File("2019-01-05_file.txt")
    assert f.is_draft
    assert f.name == "file.txt"
    assert f.date == "2019-01-05"
    assert f.version == 1

def test_draft_parsing_version():
    f = File("drafts/2019-01-05_foo-v2.docx")
    assert f.name == "foo.docx"
    assert f.date == "2019-01-05"
    assert f.version == 2

def test_not_draft():
    assert not File("drafts/foo.docx").is_draft

def test_hash(tempdir):
    path1 = write_file(tempdir, "source.txt", "same file contents")
    path2 = write_file(tempdir, "draft.txt", "same file contents")
    file1 = File(path1)
    file2 = File(path2)

    assert file1.identical_contents_to(file2)

def test_hash_no(tempdir):
    path1 = write_file(tempdir, "source.txt", "same file contents")
    path2 = write_file(tempdir, "draft.txt", "different file contents")
    file1 = File(path1)
    file2 = File(path2)

    assert not file1.identical_contents_to(file2)

def test_match():
    assert File("2019-01-01_foo.docx").is_draft_of(File("foo.docx"))

def test_match_bad():
    assert not File("2019-01-01_foo.docx").is_draft_of(File("bar.docx"))
