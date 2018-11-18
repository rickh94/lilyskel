"""Tests for info classes."""
import re
import attr
import pytest
import requests
from unittest import mock

from lilyskel import info
from lilyskel import lynames
from lilyskel import exceptions
from lilyskel import db_interface


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

    def test_load_composer(self, bach, debussy, beethoven):
        """Test dumping and loading composers."""
        bachdict = bach.dump()
        debussydict = debussy.dump()
        beethovendict = beethoven.dump()
        newbach = info.Composer.load(bachdict)
        newdebussy = info.Composer.load(debussydict)
        newbeethoven = info.Composer.load(beethovendict)
        assert attr.asdict(bach) == attr.asdict(newbach)
        assert attr.asdict(debussy) == attr.asdict(newdebussy)
        assert attr.asdict(beethoven) == attr.asdict(newbeethoven)


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
                               license='Creative Commons Attribution-ShareAlike 4.0',
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


class TestHeaders():
    """Test methods and initialization."""
    def test_add_mutopia_headers(self, headers1, mutopiaheader1):
        """Test adding mutopia headers."""
        headers1.add_mutopia_headers(mutopiaheader1, guess_composer=True)
        assert 'Violin' in headers1.mutopiaheaders.instruments,\
            "instruments should have been loaded."
        assert 'Creative' in headers1.copyright,\
            "copyright info should have been overridden"

    def test_headers_load(self, headers1, mutopiaheader1, headers2):
        newheaders = headers1
        newheaders.add_mutopia_headers(mutopiaheader1, guess_composer=True)
        newheadersdict = newheaders.dump()
        assert newheadersdict['mutopiaheaders']['style'] == 'Baroque'
        instruments1 = [info.Instrument.load(ins) for ins
                       in newheadersdict['mutopiaheaders']['instrument_list']]
        newheaders_loaded = info.Headers.load(newheadersdict, instruments1)
        assert newheaders_loaded.title == newheaders.title
        assert newheaders_loaded.meter == newheaders.meter
        assert newheaders_loaded.copyright == newheaders.copyright
        assert newheaders_loaded.mutopiaheaders.source ==\
            newheaders.mutopiaheaders.source
        assert newheaders_loaded.mutopiaheaders.license ==\
            newheaders.mutopiaheaders.license
        headers2dict = headers2.dump()
        instruments2 = [info.Instrument.load(ins) for ins
                        in headers2dict['mutopiaheaders']['instrument_list']]
        headers2_loaded = info.Headers.load(headers2dict, instruments2)
        assert headers2_loaded.title == headers2.title
        assert headers2_loaded.meter == headers2.meter
        assert headers2_loaded.copyright == headers2.copyright
        assert headers2_loaded.mutopiaheaders.source == \
           headers2.mutopiaheaders.source
        assert headers2_loaded.mutopiaheaders.license == \
           headers2.mutopiaheaders.license


def test_movement_load(six_movs):
    """Test loading movements from a dict"""
    for mov in six_movs:
        mov_dict = mov.dump()
        new_mov = info.Movement.load(mov_dict)
        assert mov.num == new_mov.num, "movement numbers should match"
        assert mov.tempo == new_mov.tempo, "tempos should match"
        assert mov.time == new_mov.time, "time signatures should match"
        assert mov.key == new_mov.key, "keys should match"


def test_get_allowed_notes(monkeypatch):
    monkeypatch.setattr(info, 'ALLOWED_NOTES', None)
    # print(info.ALLOWED_NOTES)
    allowed_notes = info.get_allowed_notes()
    # print(allowed_notes)
    for note in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        assert note in allowed_notes
    assert 'bf' in allowed_notes
    assert 'ges' in allowed_notes
    assert 'fisis' in allowed_notes
    # test that the global variable is set and data is not downloaded again.
    with monkeypatch.context() as m:
        m.delattr("requests.sessions.Session.request")
        allowed_notes2 = info.get_allowed_notes()
        assert allowed_notes2


def test_get_allowed_modes(monkeypatch):
    monkeypatch.setattr(info, 'ALLOWED_MODES', None)
    allowed_modes = info.get_allowed_modes()
    assert 'major' in allowed_modes
    assert 'minor' in allowed_modes
    assert 'mixolydian' in allowed_modes
    # test that the global variable is set and data is not downloaded again.
    with monkeypatch.context() as m:
        m.delattr("requests.sessions.Session.request")
        allowed_modes2 = info.get_allowed_modes()
        assert allowed_modes2


class TestPiece:
    """Test piece methods."""
    def test_init_version(self, headers1, instrument_list1):
        """Test getting the version number from the system."""
        test = info.Piece.init_version(headers=headers1,
                                       language='english',
                                       instruments=instrument_list1)
        assert re.match(r'^2.1.*', test.version)

    def test_piece_dump(self, piece1, piece2):
        """Test dumping piece info."""
        piece1dump = piece1.dump()
        piece2dump = piece2.dump()
        assert "2.1" in piece1dump['version']
        assert piece1dump['movements'][0]['num'] == 1
        assert piece1dump['headers']['title'] == "Test Piece"
        assert piece1dump['instruments'][0]['name'] == "violin"
        assert piece2dump['headers']['composer']['name'] == "Claude Debussy"
        assert piece2dump['movements'][3]['tempo'] == "Adagio"
        assert piece2dump['opus'] == "Op. 15"
        assert piece2dump['headers']['dedication'] == "To my test functions"

    def test_piece_load(self, piece1, piece2):
        """Test loading piece info."""
        piece1dict = piece1.dump()
        piece2dict = piece2.dump()
        new_piece1 = info.Piece.load(piece1dict)
        new_piece2 = info.Piece.load(piece2dict)
        assert new_piece1.opus == piece1.opus
        assert new_piece1.version == piece1.version
        assert new_piece1.language == piece1.language
        assert new_piece1.headers.composer.name == piece1.headers.composer.name
        assert new_piece1.movements[1].tempo == piece1.movements[1].tempo
        assert new_piece1.movements[0].key == piece1.movements[0].key
        assert new_piece2.headers.meter == piece2.headers.meter
        assert new_piece2.headers.tagline == piece2.headers.tagline
        assert new_piece2.movements[0].num == piece2.movements[0].num
        assert new_piece2.headers.copyright == piece2.headers.copyright
        assert new_piece2.headers.mutopiaheaders.maintainer == \
           piece2.headers.mutopiaheaders.maintainer
