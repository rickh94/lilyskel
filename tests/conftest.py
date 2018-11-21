"""Global pytest fixtures."""
import sys

import re
import shutil
import subprocess
from pathlib import Path
import pytest
from jinja2 import Environment, PackageLoader
from tinydb import TinyDB
from lilyskel import lynames
from lilyskel import info


here = Path(__file__)
basedir = here.parents[1]
srcdir = Path(basedir, 'lilyskel')


@pytest.fixture(scope='module')
def livedb(tmpdir_factory):
    """A live database with data."""
    tmpdir_ = tmpdir_factory.mktemp('livedb')
    shutil.copy2(Path(basedir, 'tests', 'test_db.json'), Path(tmpdir_))
    return TinyDB(Path(tmpdir_, 'test_db.json'))


@pytest.fixture(scope='module')
def defaultdb(tmpdir_factory):
    tmpdir_ = tmpdir_factory.mktemp('defaultdb')
    shutil.copy(Path(srcdir, 'default_db.json'), Path(tmpdir_))
    return TinyDB(Path(tmpdir_, 'default_db.json'))


@pytest.fixture
def prompt_commands():
    with Path(basedir, 'tests', 'lilyskel_command.txt').open('r') as commandfile:
        return [line.strip() for line in commandfile.readlines()]


@pytest.fixture
def good_beethoven(lily_version):
    with Path(basedir, 'tests', 'good_beethoven_5.yaml').open('r') as beethoven_file:
        beethoven_data = beethoven_file.read()

    correct_data = beethoven_data.replace('2.18.2', lily_version)
    return correct_data


@pytest.fixture
def lily_version():
    ly_vers = subprocess.run(['lilypond', '--version'],
                          stdout=subprocess.PIPE)
    matchvers = re.search(r'LilyPond ([^\n]*)',
                          ly_vers.stdout.decode(sys.stdout.encoding))
    return matchvers.group(1)


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
def piano():
    """A piano instrument."""
    return lynames.Instrument('Piano', abbr='Pno.', transposition=None,
                              keyboard=True, midi='acoustic grand',
                              family='percussion', mutopianame='Piano')


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
                               license='Creative Commons Attribution 4.0',
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


@pytest.fixture
def jinja_env():
    """Defines a jinja environment loading the default templates."""
    return Environment(
        loader=PackageLoader('lilyskel', 'templates')
    )


@pytest.fixture
def mov_one_all():
    """Populated first movement."""
    return info.Movement(num=1,
                         tempo='Allegro',
                         time='4/4',
                         key=('a', 'major'))


@pytest.fixture
def mov_one_empty():
    """Empty first movement."""
    return info.Movement(num=1)


@pytest.fixture
def mov_two():
    """Two movement."""
    return info.Movement(num=2,
                         tempo='Largo',
                         key=('a', 'minor'),
                         time='3/4'
                         )


@pytest.fixture
def mov_three():
    """Third movement"""
    return info.Movement(num=3,
                         tempo='Vivace',
                         key=('a', 'major'),
                         time='2/4'
                         )


@pytest.fixture
def mov_four():
    """fourth movement"""
    return info.Movement(num=4,
                         tempo='Adagio',
                         key=('d', 'major')
                         )


@pytest.fixture
def mov_five():
    """blank movement"""
    return info.Movement(num=5)


@pytest.fixture
def mov_six():
    """blank movement"""
    return info.Movement(num=6)


@pytest.fixture
def three_movs(mov_one_all, mov_two, mov_three):
    """Three movements."""
    return [mov_one_all, mov_two, mov_three]


@pytest.fixture
def piece1(headers1, three_movs, instrument_list1):
    """A piece with minimal headers."""
    return info.Piece.init_version(language='english',
                                   headers=headers1,
                                   movements=three_movs,
                                   instruments=instrument_list1
                                   )


@pytest.fixture
def six_movs(mov_one_empty, mov_two, mov_three, mov_four, mov_five, mov_six):
    """List of six movements."""
    return [mov_one_empty, mov_two, mov_three, mov_four, mov_five, mov_six]


@pytest.fixture
def piece2(headers2, six_movs, instrument_list1):
    """A piece with more complete headers."""
    return info.Piece.init_version(language='english',
                                   headers=headers2,
                                   opus='Op. 15',
                                   movements=six_movs,
                                   instruments=instrument_list1
                                   )
