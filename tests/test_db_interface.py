"""Tests db interaction functions."""
from pathlib import Path
import os
import shutil
import pytest
from unittest import mock
from tinydb import TinyDB
from lyskel import db_interface

home = os.path.join(os.path.expanduser('~'))
here = Path(__file__)
basedir = here.parents[1]
srcdir = Path(basedir, 'lyskel')


def test_is_path():
    """Test that it stays a Path object."""
    assert db_interface.pathify(Path('/tmp', 'test', 'dir')) ==\
        Path('/tmp', 'test', 'dir')


def test_is_str():
    """Test that we get a path object from a string."""
    assert db_interface.pathify('/tmp/test/dir') ==\
        Path('/tmp', 'test', 'dir')

    assert db_interface.pathify('c:/tmp/test/dir') ==\
        Path('c:/tmp', 'test', 'dir')


@mock.patch('lyskel.db_interface.os.makedirs')
@mock.patch('lyskel.db_interface.Path.exists')
@mock.patch('lyskel.db_interface.TinyDB')
def test_init_db(mock_db, mock_exists, mock_makedirs):
    """Test database initialization."""
    # test default no directories
    mock_exists.return_value = False
    db_interface.init_db(),
    mock_db.assert_called_once_with(
        Path(home, '.local', 'lyskel', 'db.json'))
    mock_makedirs.assert_called_once_with(
        Path(home, '.local', 'lyskel'))

    # test without missing directories
    mock_makedirs.reset_mock()
    mock_db.reset_mock()
    mock_exists.return_value = True
    db_interface.init_db(),
    mock_db.assert_called_once_with(
        Path(home, '.local', 'lyskel', 'db.json'))
    mock_makedirs.assert_not_called()

    # test custom
    mock_makedirs.reset_mock()
    mock_db.reset_mock()
    mock_exists.return_value = False
    db_interface.init_db('/one/two/three.json'),
    mock_db.assert_called_once_with(
        Path('/one', 'two', 'three.json'))
    mock_makedirs.assert_called_once_with(Path('/one', 'two'))


@mock.patch('lyskel.db_interface.os.makedirs')
@mock.patch('lyskel.db_interface.shutil')
def test_bootstrap_db(mock_shutil, mock_makedirs):
    """Tests bootstraping the database with the default."""
    # test default db path
    db_interface.bootstrap_db()
    mock_makedirs.assert_called_once_with(
        Path(home, '.local', 'lyskel'), exist_ok=True
    )
    mock_shutil.copy2.assert_called_once_with(
        Path(srcdir, 'default_db.json'),
        Path(home, '.local', 'lyskel', 'db.json')
    )


@pytest.fixture
def testdb(monkeypatch, tmpdir):
    """Returns a monkeypatched db."""
    test_db = TinyDB(Path(tmpdir, 'testdb.json'))

    def mocktables():
        return {'instruments', '_default', 'ensembles'}

    monkeypatch.setattr(test_db, 'tables', mocktables)
    yield test_db


def test_explore_db(monkeypatch, testdb):
    """Test exploring a database."""
    ret_tables = db_interface.explore_db(testdb)
    # A list with certain values is required, but the order is unimportant.
    assert isinstance(ret_tables, list)
    assert set(ret_tables) == set(['instruments', 'ensembles'])

    with pytest.raises(ValueError, message="expecting ValueError",
                       match="'db' must be a TinyDB instance"):
        db_interface.explore_db('not a db')


@pytest.fixture
def mocktable():
    mock_table = mock.MagicMock()
    mock_table.all.return_value = [
        {'name': 'violin', 'transposition': None},
        {'name': 'violoncello', 'clef': 'bass'},
        {'name': 'clarinet_in_bb', 'clef': 'treble', 'transposition': 'bb'}
    ]
    return mock_table


@pytest.fixture
def livedb(tmpdir):
    """A live database with data."""
    shutil.copy2(Path(srcdir, 'default_db.json'), Path(tmpdir))
    return TinyDB(Path(tmpdir, 'default_db.json'))


@pytest.fixture
def livetable(livedb):
    """A live table with data."""
    return livedb.table('instruments')


def test_explore_table(mocktable, livetable):
    """Test exploring a database table."""
    assert set(db_interface.explore_table(mocktable)) ==\
        set(['violin', 'violoncello', 'clarinet_in_bb'])
    assert set(db_interface.explore_table(livetable,
                                          search=('name', 'vio'))) ==\
        set(['violin', 'viola', 'violoncello'])
