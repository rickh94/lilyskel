from pathlib import Path

import pytest

from lilyskel import yaml_interface


def test_read_write_piece(piece1, piece2, tmpdir):
    testfile1 = Path(tmpdir, "testfile1.yaml")
    testfile1a = Path(tmpdir, "testfile1a.yaml")
    testfile1b = Path(tmpdir, "testfile1b.yaml")
    testfile2 = Path(tmpdir, "testfile2.yaml")
    piece1data = piece1.dump()
    piece2data = piece2.dump()
    yaml_interface.write_config(testfile1, piece1)
    yaml_interface.write_config(testfile1a, piece1)
    piece1read = yaml_interface.read_config(testfile1)
    assert piece1read.dump() == piece1data, "data should be intact"
    piece1aread = yaml_interface.read_config(testfile1a)
    assert piece1read.dump() == piece1aread.dump(), "should be repeatable"
    yaml_interface.write_config(testfile1b, piece1read)
    with testfile1b.open("rb") as t1b:
        with testfile1.open("rb") as t1:
            assert (
                t1.read() == t1b.read()
            ), "reading and writing should produce the same file"
    yaml_interface.write_config(testfile2, piece2)
    piece2read = yaml_interface.read_config(testfile2)
    assert piece2read.dump() == piece2data, "other piece should work"


def test_empty_piece(tmpdir):
    testfile3 = Path(tmpdir, "testfile3.yaml")
    testfile3.open("w").close()
    with pytest.raises(ValueError):
        yaml_interface.read_config(testfile3)
