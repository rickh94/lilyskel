"""Global pytest fixtures."""
import shutil
from pathlib import Path
import pytest
from tinydb import TinyDB
from lyskel import lynames
from lyskel import info
# pylint: disable=redefined-outer-name


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
        """A set of tables."""
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


@pytest.fixture
def bach():
    """A composer instance with everything."""
    return info.Composer(name="Johann Sebastian Bach",
                         mutopianame="BachJS",
                         shortname="J.S. Bach")


@pytest.fixture
def mutopiaheader1(instrument_list1):
    """Some mutopia Headers."""
    return info.MutopiaHeaders(instrument_list=instrument_list1,
                               source='Breitkopf und Hartël',
                               style='Baroque',
                               maintainer='Rick Henry',
                               maintainerEmail='fredericmhenry@gmail.com',
                               date='1234',
                               license='cc4',
                               )


@pytest.fixture
def headers1(bach):
    """A headers instance."""
    return info.Headers(title='Test Piece',
                        composer=bach,
                        tagline='mytagline',
                        )


@pytest.fixture
def debussy():
    """A composer instance with shortname."""
    return info.Composer(name="Claude Debussy",
                         shortname="Claude Debussy")


@pytest.fixture
def headers2(debussy, mutopiaheader1):
    """A complete headers instance."""
    head = info.Headers(title='Test Piece',
                        composer=debussy,
                        dedication='To my test functions',
                        subtitle='A nonexistent piece',
                        tagline='mytagline',
                        )
    head.add_mutopia_headers(mutopiaheader1, guess_composer=True)
    return head


@pytest.fixture
def instrument_list1(test_ins, test_ins2, test_ins3, test_ins4):
    """A list of instruments."""
    return [test_ins, test_ins2, test_ins3, test_ins4]
