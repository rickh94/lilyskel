"""Tests for LyName and it's child classes."""
import unittest
from unittest import mock
import pytest
from tinydb import TinyDB
from lyskel import lynames
from lyskel import exceptions
# pylint: disable=protected-access


class TestRomanNumeral(object):
    """Tests my roman_numberal function."""
    def test_one_thru_ten(self):
        """Tests that one through ten are correct."""
        assert lynames._roman_numeral(1) == 'I'
        assert lynames._roman_numeral(2) == 'II'
        assert lynames._roman_numeral(3) == 'III'
        assert lynames._roman_numeral(4) == 'IV'
        assert lynames._roman_numeral(5) == 'V'
        assert lynames._roman_numeral(6) == 'VI'
        assert lynames._roman_numeral(7) == 'VII'
        assert lynames._roman_numeral(8) == 'VIII'
        assert lynames._roman_numeral(9) == 'IX'
        assert lynames._roman_numeral(10) == 'X'

    def test_eleven_thru_twenty(self):
        """Tests eleven through twenty roman numerals."""
        assert lynames._roman_numeral(11) == 'XI'
        assert lynames._roman_numeral(12) == 'XII'
        assert lynames._roman_numeral(13) == 'XIII'
        assert lynames._roman_numeral(14) == 'XIV'
        assert lynames._roman_numeral(15) == 'XV'
        assert lynames._roman_numeral(16) == 'XVI'
        assert lynames._roman_numeral(17) == 'XVII'
        assert lynames._roman_numeral(18) == 'XVIII'
        assert lynames._roman_numeral(19) == 'XIX'
        assert lynames._roman_numeral(20) == 'XX'

    def test_twenty_one_thru_thirty(self):
        """Tests twenty one through thirty roman numerals."""
        assert lynames._roman_numeral(21) == 'XXI'
        assert lynames._roman_numeral(22) == 'XXII'
        assert lynames._roman_numeral(23) == 'XXIII'
        assert lynames._roman_numeral(24) == 'XXIV'
        assert lynames._roman_numeral(25) == 'XXV'
        assert lynames._roman_numeral(26) == 'XXVI'
        assert lynames._roman_numeral(27) == 'XXVII'
        assert lynames._roman_numeral(28) == 'XXVIII'
        assert lynames._roman_numeral(29) == 'XXIX'
        assert lynames._roman_numeral(30) == 'XXX'

    def test_large_numbers(self):
        """Test some arbitrary large numbers."""
        assert lynames._roman_numeral(40) == 'IL'
        assert lynames._roman_numeral(43) == 'ILIII'
        assert lynames._roman_numeral(50) == 'L'
        assert lynames._roman_numeral(59) == 'LIX'
        assert lynames._roman_numeral(78) == 'LXXVIII'
        assert lynames._roman_numeral(89) == 'LXXXIX'

    def test_errors(self):
        with pytest.raises(TypeError,
                           message="Expecting TypeError for non-int value",
                           match=r"num.*int"):
            lynames._roman_numeral('hi')

        with pytest.raises(ValueError, message="Expecting ValueError for > 89",
                           match=r".*1 and 89"):
            lynames._roman_numeral(90)

        with pytest.raises(ValueError, message="Expecting ValueError for < 1",
                           match=r".*1 and 89"):
            lynames._roman_numeral(0)


class TestLyName():
    """Test the LyName class methods."""
    def test_init(self):
        """Test normalization of name input."""
        test1 = lynames.LyName('TEST name ')
        assert test1.name == 'test_name'
        assert test1.number is None

        test2 = lynames.LyName('  another_test-name')
        assert test2.name == 'another_test_name'
        assert test2.number is None

    def test_movement(self):
        """Tests file_name and var_name methods and related exceptions."""
        testlyname1 = lynames.LyName('global')
        testlyname2 = lynames.LyName('test')
        testlyname2.number = 2
        testlyname2._numword = 'two'

        # test file_name
        assert testlyname1.file_name(1) == 'global_1'
        assert testlyname1.file_name(2) == 'global_2'
        assert testlyname2.file_name(1) == 'test2_1'

        # test var_name
        assert testlyname1.var_name(2) == 'global_second_mov'
        assert testlyname1.var_name(31) == 'global_thirty_first_mov'
        assert testlyname2.var_name(2) == 'test_two_second_mov'

        # test exceptions
        with pytest.raises(TypeError,
                           message="Expect TypeError if form no specified.",
                           match=".*'form'.*"):
            testlyname1._movement(1)

        with pytest.raises(TypeError,
                           message=("Expect TypeError "
                                    "if 'mov_num' is not an int"),
                           match=".*integer"):
            testlyname1._movement('10', form='word')

        with pytest.raises(ValueError,
                           message=("Expect ValueError if form is not one of "
                                    "'ord', 'word', 'num'."),
                           match=".*'form'.*'word'"):
            testlyname1._movement(10, form='fail')


@pytest.fixture(scope='module')
def test_ins():
    """A test instrument."""
    return lynames.Instrument.numbered_name('VioliN', 1)


@pytest.fixture(scope='module')
def test_ins2():
    """Another test instrument."""
    return lynames.Instrument.numbered_name('violoncello', 2, abbr='Vc.',
                                            clef='bass', midi='violoncello')


@pytest.fixture(scope='module')
def test_ins3():
    """A third test instrument."""
    return lynames.Instrument('Clarinet in Bb', abbr='Cl.', clef='treble',
                              transposition='Bb', keyboard=False,
                              midi='clarinet')


@pytest.fixture
def mockdb():
    mock_db = mock.MagicMock(spec=TinyDB)
    mock_table = mock.MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = {
        'name': 'flute',
        'abbr': 'Fl.',
        'clef': 'treble',
        'transposition': None,
        'keyboard': False,
        'midi': 'flute'
    }
    return mock_db


class TestInstrument():
    """
    Test the Instrument Class.
    Some of this is really more like integration tests.
    """
    def test_numbered_name(self, test_ins, test_ins2, test_ins3):
        """Test the numbered name class method."""
        assert test_ins.name == 'violin'
        assert test_ins.number == 1
        assert test_ins._numword == 'one'
        assert test_ins._roman == 'I'
        assert test_ins.abbr == ''
        assert test_ins.clef == 'treble'
        assert test_ins.transposition is None
        assert test_ins.keyboard is False
        assert test_ins.midi is None

        assert test_ins2.name == 'violoncello'
        assert test_ins2.number == 2
        assert test_ins2._numword == 'two'
        assert test_ins2._roman == 'II'
        assert test_ins2.abbr == 'Vc.'
        assert test_ins2.clef == 'bass'
        assert test_ins2.transposition is None
        assert test_ins2.keyboard is False
        assert test_ins2.midi == 'violoncello'

    def test_init_with_attribs(self, test_ins3):
        """
        Test direct initialization with transposition and normalization of the
        name.
        """
        assert test_ins3.name == 'clarinet_in_bb'
        assert test_ins3.number is None
        assert test_ins3.abbr == 'Cl.'
        assert test_ins3.clef == 'treble'
        assert test_ins3.transposition == 'Bb'
        assert test_ins3.keyboard is False
        assert test_ins3.midi == 'clarinet'

    def test_part_name(self, test_ins, test_ins2, test_ins3):
        """Tests the part_name method."""
        assert test_ins.part_name() == 'Violin I'
        assert test_ins2.part_name() == 'Violoncello II'
        assert test_ins3.part_name() == 'Clarinet'
        assert test_ins3.part_name(key=True) == 'Clarinet in Bb'

    def test_load_from_db(self, mockdb):
        """Tests loading an object from tinydb."""
        # mock the db and table objects

        assert lynames.Instrument.load_from_db('flute', mockdb) ==\
            lynames.Instrument(
                'flute',
                abbr='Fl.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='flute'
            )

        # make sure it still works with numbers
        assert lynames.Instrument.load_from_db('flute', mockdb, number=2) ==\
            lynames.Instrument.numbered_name(
                'flute',
                number=2,
                abbr='Fl.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='flute'
            )

        # if not found, it should raise InstrumentNotFoundError.
        failtable = mock.MagicMock()
        mockdb.table.return_value = failtable
        failtable.get.return_value = None
        # if not found, 'get' from the table will return none.
        with pytest.raises(exceptions.InstrumentNotFoundError,
                           message=("expect InstrumentNotFoundError if "
                                    "supplied instrument is not in supplied "
                                    "table."),
                           match='.*not in.*table'):
            lynames.Instrument.load_from_db('fail', mockdb)

    def test_add_to_db(self, test_ins, test_ins2, test_ins3):
        """Tests adding an object to the database."""
        mock_db = mock.MagicMock()
        mock_table = mock.MagicMock()
        mock_db.table.return_value = mock_table

        test_ins.add_to_db(mock_db)
        mock_table.insert.assert_called_once_with(
            {'name': 'violin',
             'abbr': '',
             'clef': 'treble',
             'transposition': None,
             'keyboard': False,
             'midi': None
             }
        )

        mock_table.reset_mock()
        test_ins2.add_to_db(mock_db)
        mock_table.insert.assert_called_once_with(
            {'name': 'violoncello',
             'abbr': 'Vc.',
             'clef': 'bass',
             'transposition': None,
             'keyboard': False,
             'midi': 'violoncello'
             }
        )

        mock_table.reset_mock()
        test_ins3.add_to_db(mock_db)
        mock_table.insert.assert_called_once_with(
            {'name': 'clarinet_in_bb',
             'abbr': 'Cl.',
             'clef': 'treble',
             'transposition': 'Bb',
             'keyboard': False,
             'midi': 'clarinet'
             }
        )
