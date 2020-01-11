from draft_file import *
import pytest, tempfile, os, os.path

good_name = "2019-01-05_foo.docx"

@pytest.fixture
def good_path():
    with tempfile.TemporaryDirectory() as tempdir:
        path = os.path.join(tempdir, good_name)

        with open(path, "w") as f:
            f.write("test\n")

        yield path


def test_draft_parsing(good_path):
    x = File(good_path)
    assert x.is_draft
    assert x.name == "foo.docx"
    assert x.date == "2019-01-05"
    assert x.version == 0
    assert x.exists

def test_draft_parsing_version():
    x = File("drafts/2019-01-05_foo-v2.docx")
    assert x.name == "foo.docx"
    assert x.date == "2019-01-05"
    assert x.version == 2
    assert not x.exists

def test_not_draft():
    assert not File("drafts/foo.docx").is_draft

def test_hash():
    msg = "foo"
    with tempfile.NamedTemporaryFile("w") as f1, tempfile.NamedTemporaryFile("w") as f2:
        f1.write(msg)
        f2.write(msg)

        assert File.digest_file(f1.name) == File.digest_file(f2.name)
