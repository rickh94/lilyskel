"""Tests for info classes."""
import pytest
from lyskel import info
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
