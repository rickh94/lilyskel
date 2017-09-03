"""Tests for info classes."""
import re
import pytest
from lyskel import info
from lyskel import lynames
from lyskel import exceptions
from lyskel import db_interface


@pytest.fixture
def bach():
    """A composer instance with everything."""
    return info.Composer(name="Johann Sebastian Bach",
                         mutopianame="BachJS",
                         shortname="J.S. Bach")


@pytest.fixture
def beethoven():
    """Bare minimum composer instance"""
    return info.Composer(name="Ludwig van Beethoven")


@pytest.fixture
def brahms():
    """A composer instance with mutopianame."""
    return info.Composer(name="Johannes Brahms",
                         mutopianame="BrahmsJ")


@pytest.fixture
def debussy():
    """A composer instance with shortname."""
    return info.Composer(name="Claude Debussy",
                         shortname="Claude Debussy")


@pytest.fixture
def anon():
    """A single word composer."""
    return info.Composer(name='Anonymous')


@pytest.fixture
def fakecomposer():
    """A nonexistent composer."""
    return info.Composer(name='Not A Real Composer_')


class TestComposer():
    """Test composer methods."""
    def test_get_short_name(self, bach, beethoven, brahms, debussy, anon):
        """Test generating or retrieving a composer short name."""
        assert bach.get_short_name() == "J.S. Bach",\
            "Should get the attribute."
        assert beethoven.get_short_name() == "L.v. Beethoven",\
            "Should generate a short name properly"
        assert brahms.get_short_name() == "J. Brahms",\
            "Should generate a short name properly"
        assert debussy.get_short_name() == "Claude Debussy",\
            "Manually setting the attribute should override the method."
        assert anon.get_short_name() == 'Anonymous',\
            "Single name composers should work properly"

    def test_mutopia_name(self, bach, beethoven, brahms, debussy, anon,
                          fakecomposer):
        """Test getting the mutopia name."""
        assert bach.get_mutopia_name() == "BachJS",\
            "Should return manual attribute."
        assert brahms.get_mutopia_name(guess=True) == "BrahmsJ",\
            "Should return manual attribute, even when told to guess."
        assert debussy.get_mutopia_name(guess=True) == "DebussyC",\
            "Should find one when missing."

        with pytest.raises(exceptions.MutopiaError,
                           match=".*composer.*",
                           message=("Expect MutopiaError if a matching "
                                    "composer is not found in mutopia's list")
                           ):
            fakecomposer.get_mutopia_name(guess=True)

        with pytest.raises(AttributeError,
                           match=".*mutopia name.*",
                           message=("Expect AttributeError if attribute is not"
                                    " set and guess is false.")):
            beethoven.get_mutopia_name()

        # this will set the attribute so it needs to run last
        assert beethoven.get_mutopia_name(guess=True) == "BeethovenLv",\
            "Should find one when missing."
        assert beethoven.get_mutopia_name(guess=False) == "BeethovenLv",\
            "After successfully guessing, attribute should be available."

    def test_load_from_db(self, bach, livedb):
        """Test loading from the database."""
        assert info.Composer.load_from_db(
            name='Johann Sebastian Bach', db=livedb) == bach,\
            "The loaded copy should be the same as the fixture copy."

    def test_add_to_db(self, beethoven, debussy, mockdb):
        """Test adding composers to the database."""
        beethoven.add_to_db(mockdb)
        comptable = mockdb.table('composers')
        assert db_interface.explore_table(
            comptable, search=('name', 'Ludwig van Beethoven'))

        debussy.add_to_db(mockdb)
        assert db_interface.explore_table(
            comptable, search=('name', 'Claude Debussy'))


@pytest.fixture
def mutopiaheader1(test_ins, test_ins2, test_ins3, test_ins4, bach):
    """Some mutopia Headers."""
    return info.MutopiaHeaders(instrument_list=[test_ins, test_ins2, test_ins3,
                                                test_ins4],
                               source='Breitkopf und Hartël',
                               style='Baroque',
                               maintainer='Rick Henry',
                               maintainerEmail='fredericmhenry@gmail.com',
                               date='1234',
                               license='cc4',
                               )


@pytest.fixture
def random_ens(test_ins, test_ins2, test_ins3, test_ins4):
    new_ens = lynames.Ensemble('random_ens')
    new_ens.add_instrument_from_obj(test_ins)
    new_ens.add_instrument_from_obj(test_ins2)
    new_ens.add_instrument_from_obj(test_ins3)
    new_ens.add_instrument_from_obj(test_ins4)
    return new_ens


@pytest.fixture
def mutopiaheader2(random_ens):
    """Some mutopia Headers from an ensemble object."""
    return info.MutopiaHeaders(instrument_list=random_ens,
                               source='Breitkopf und Hartël',
                               style='Baroque',
                               maintainer='Rick Henry',
                               maintainerEmail='fredericmhenry@gmail.com',
                               date='1234',
                               license='ccsa4',
                               )


def test_convert_instruments(mutopiaheader2, test_ins, test_ins2, test_ins3,
                             test_ins4):
    """Test that an instrument list was created from the ensemble object."""
    inslist = mutopiaheader2.instrument_list
    assert test_ins in inslist
    assert test_ins2 in inslist
    assert test_ins3 in inslist
    assert test_ins4 in inslist


def test_validate_mutopia_headers(mutopiaheader1):
    """Test validation of mutopia headers."""
    # these should not raise exceptions
    info._validate_mutopia_headers(None)
    info._validate_mutopia_headers(mutopiaheader1)

    with pytest.raises(TypeError, match='.*mutopiaheaders.*MutopiaHeaders.*',
                       message=('Expect TypeError if not none or a '
                                'MutopiaHeaders instance.')):
        info._validate_mutopia_headers('fail badly')


def test_validate_instruments(mutopiaheader1):
    """Test validation of instrument list."""
    with pytest.raises(TypeError, match='instruments.*list.*',
                       message=('Expect TypeError when not a list of '
                                'instruments')):
        mutopiaheader1.validate_instruments('instrument_list', 'not a list')
    with pytest.raises(TypeError, match='instruments.*list.*',
                       message=('Expect TypeError when not a list of '
                                'instruments')):
        mutopiaheader1.validate_instruments('instrument_list', ['not',
                                                                'an',
                                                                'instrument'])


def test_validate_composer(mutopiaheader1):
    """Test validation of composer."""


@pytest.fixture
def headers1(bach):
    """A headers instance."""
    return info.Headers(title='Test Piece',
                        composer=bach,
                        tagline='mytagline',
                        )


class TestHeaders():
    """Test methods and initialization."""
    def test_add_mutopia_headers(self, headers1, mutopiaheader1):
        """Test adding mutopia headers."""
        headers1.add_mutopia_headers(mutopiaheader1, guess_composer=True)
        assert 'Violin' in headers1.mutopiaheaders.instruments,\
            "instruments should have been loaded."
        assert 'Creative' in headers1.copyright,\
            "copyright info should have been overridden"


class TestPiece():
    """Test piece methods."""
    def test_init_version(self, headers1):
        """Test getting the version number from the system."""
        test = info.Piece.init_version(name='test1', headers=headers1,
                                       language='english')
        assert re.match(r'^2.1.*', test.version)
