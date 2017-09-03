"""Global pytest fixtures."""
import pytest
import shutil
from pathlib import Path
from tinydb import TinyDB
from lyskel import lynames


here = Path(__file__)
basedir = here.parents[1]
srcdir = Path(basedir, 'lyskel')


@pytest.fixture(scope='module')
def livedb(tmpdir_factory):
    """A live database with data."""
    tmpdir_ = tmpdir_factory.mktemp('livedb')
    shutil.copy2(Path(srcdir, 'default_db.json'), Path(tmpdir_))
    return TinyDB(Path(tmpdir_, 'default_db.json'))


@pytest.fixture
def mockdb(monkeypatch, tmpdir):
    """Returns a monkeypatched db."""
    test_db = TinyDB(Path(tmpdir, 'mockdb.json'))

    def mocktables():
        return {'instruments', '_default', 'ensembles'}

    monkeypatch.setattr(test_db, 'tables', mocktables)
    yield test_db


@pytest.fixture
def test_ins():
    """A test instrument."""
    return lynames.Instrument.numbered_name('VioliN', 1)


@pytest.fixture
def test_ins2():
    """Another test instrument."""
    return lynames.Instrument.numbered_name('violoncello', 2, abbr='Vc.',
                                            clef='bass', midi='violoncello',
                                            family='strings')


@pytest.fixture
def test_ins3():
    """A third test instrument."""
    return lynames.Instrument('Clarinet in Bb', abbr='Cl.', clef='treble',
                              transposition='Bb', keyboard=False,
                              midi='clarinet', family='woodwinds')


@pytest.fixture
def test_ins4():
    """A fourth test instrument."""
    return lynames.Instrument('Oboe', abbr='Ob.', clef='treble',
                              transposition=None, keyboard=False,
                              midi='oboe', family='woodwinds',
                              mutopianame='Oboe_')
