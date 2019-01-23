"""Tests db interaction functions."""
import os
from pathlib import Path
from unittest import mock

import pytest
from tinydb import TinyDB

from lilyskel import db_interface, exceptions

home = os.path.join(os.path.expanduser("~"))
here = Path(__file__)
basedir = here.parents[1]
srcdir = Path(basedir, "lilyskel")


@mock.patch("lilyskel.db_interface.os.makedirs")
@mock.patch("lilyskel.db_interface.Path.exists")
@mock.patch("lilyskel.db_interface.TinyDB")
def test_init_db(mock_db, mock_exists, mock_makedirs):
    """Test database initialization."""
    # test default no directories
    mock_exists.return_value = False
    db_interface.init_db(),
    mock_db.assert_called_once_with(
        Path(home, ".local", "share", "lilyskel", "db.json")
    )
    mock_makedirs.assert_called_once_with(Path(home, ".local", "share", "lilyskel"))

    # test without missing directories
    mock_makedirs.reset_mock()
    mock_db.reset_mock()
    mock_exists.return_value = True
    db_interface.init_db(),
    mock_db.assert_called_once_with(
        Path(home, ".local", "share", "lilyskel", "db.json")
    )
    mock_makedirs.assert_not_called()

    # test custom
    mock_makedirs.reset_mock()
    mock_db.reset_mock()
    mock_exists.return_value = False
    db_interface.init_db("/one/two/three.json"),
    mock_db.assert_called_once_with(Path("/one", "two", "three.json"))
    mock_makedirs.assert_called_once_with(Path("/one", "two"))


@mock.patch("lilyskel.db_interface.os.makedirs")
@mock.patch("lilyskel.db_interface.shutil")
def test_bootstrap_db(mock_shutil, mock_makedirs):
    """Tests bootstraping the database with the default."""
    # test default db path
    db_interface.bootstrap_db()
    mock_makedirs.assert_called_once_with(
        Path(home, ".local", "share", "lilyskel"), exist_ok=True
    )
    mock_shutil.copy2.assert_called_once_with(
        Path(srcdir, "default_db.json"),
        Path(home, ".local", "share", "lilyskel", "db.json"),
    )


def test_explore_db(monkeypatch, mockdb):
    """Test exploring a database."""
    ret_tables = db_interface.explore_db(mockdb)
    # A list with certain values is required, but the order is unimportant.
    assert isinstance(ret_tables, list)
    assert set(ret_tables) == set(["instruments", "ensembles"])

    with pytest.raises(ValueError):
        db_interface.explore_db("not a db")


@pytest.fixture
def mocktable():
    """A mocked table."""
    mock_table = mock.MagicMock()
    mock_table.all.return_value = [
        {"name": "violin", "transposition": None},
        {"name": "violoncello", "clef": "bass"},
        {"name": "clarinet_in_bb", "clef": "treble", "transposition": "bb"},
    ]
    return mock_table


@pytest.fixture
def livetable(livedb):
    """A live table with data."""
    return livedb.table("instruments")


def test_explore_table(mocktable, livetable):
    """
    Test exploring a database table.
    NOTE: some assertions use set.issubset() so that if additional matching
    items are added the tests will still pass.
    """
    assert {"violin", "violoncello", "clarinet_in_bb"} == set(
        db_interface.explore_table(mocktable)
    ), ("Without search terms " "it should return all " "names.")
    assert {"violin", "viola", "violoncello"}.issubset(
        set(db_interface.explore_table(livetable, search=("name", "vio")))
    ), "With search terms it should return matching subset."
    assert {"violoncello", "double_bass", "contrabass"}.issubset(
        set(db_interface.explore_table(livetable, search=("clef", "bass")))
    ), "With search terms it should return matching subset."
    assert {"violin", "viola", "violoncello", "double_bass", "contrabass"}.issubset(
        db_interface.explore_table(livetable, search=("family", "strings"))
    ), ("With search " "terms it should " "return matching " "subset.")
    assert (
        db_interface.explore_table(livetable, search=("name", "this is not the table"))
        == []
    ), ("If nothing matches " "return empty list.")
    assert (
        db_interface.explore_table(livetable, search=("not a field", "fail")) == []
    ), "If nothing matches return empty list."

    assert db_interface.explore_table(
        livetable, search=("name", "vio")
    ), "A search that finds something should be implicitly true"
    assert not db_interface.explore_table(
        livetable, search=("name", "not in the database")
    ), ("A search that returns nothing " "should be implicitly false.")

    with pytest.raises(TypeError, match=".*tuple.*"):
        db_interface.explore_table(livetable, search="hi")

    with pytest.raises(TypeError, match=".*tinydb.*"):
        db_interface.explore_table(123, search=("name", "test"))

    # test that it handles malformed data
    mocktable.search.return_value = [
        {"name": "hi"},
        {"fake": "table"},
        {"key": "value"},
        {"name": "test"},
    ]
    assert db_interface.explore_table(mocktable, search=("name", "test")) == [
        "hi",
        "test",
    ]


def test_load_name_from_table(livedb):
    """Test loading data from a table."""
    # mock test
    mock_db = mock.MagicMock(spec=TinyDB)
    mock_table = mock.MagicMock()
    mock_table.get.return_value = {"name": "test", "data": "test"}
    mock_db.table.return_value = mock_table

    assert db_interface.load_name_from_table("test", mock_db, "testtable") == {
        "name": "test",
        "data": "test",
    }

    # test returns none
    mock_table.get.return_value = None
    with pytest.raises(
        exceptions.DataNotFoundError, match="'test' is not in the 'testtable' table"
    ):
        db_interface.load_name_from_table("test", mock_db, "testtable")

    # live db tests
    assert set({"name": "violin", "clef": "treble"}).issubset(
        set(db_interface.load_name_from_table("violin", livedb, "instruments"))
    ), "Should be able to load an instrument correctly"
    assert set(
        {
            "name": "string_quartet",
            "instruments": [
                {"name": "violin", "number": 1},
                {"name": "violin", "number": 2},
                {"name": "viola", "number": None},
                {"name": "violoncello", "number": None},
            ],
        }
    ).issubset(
        db_interface.load_name_from_table("string_quartet", livedb, "ensembles")
    ), "Should be able to load an ensemble correctly."
