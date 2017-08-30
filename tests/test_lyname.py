"""Tests for LyName and it's child classes."""
import unittest
from unittest import mock
from tinydb import TinyDB
from lyskel import lynames
from lyskel import exceptions
# pylint: disable=protected-access


class TestRomanNumeral(unittest.TestCase):
    """Tests my roman_numberal function."""
    def test_one_thru_ten(self):
        """Tests that one through ten are correct."""
        self.assertEqual(lynames._roman_numeral(1), 'I')
        self.assertEqual(lynames._roman_numeral(2), 'II')
        self.assertEqual(lynames._roman_numeral(3), 'III')
        self.assertEqual(lynames._roman_numeral(4), 'IV')
        self.assertEqual(lynames._roman_numeral(5), 'V')
        self.assertEqual(lynames._roman_numeral(6), 'VI')
        self.assertEqual(lynames._roman_numeral(7), 'VII')
        self.assertEqual(lynames._roman_numeral(8), 'VIII')
        self.assertEqual(lynames._roman_numeral(9), 'IX')
        self.assertEqual(lynames._roman_numeral(10), 'X')

    def test_eleven_thru_twenty(self):
        """Tests eleven through twenty roman numerals."""
        self.assertEqual(lynames._roman_numeral(11), 'XI')
        self.assertEqual(lynames._roman_numeral(12), 'XII')
        self.assertEqual(lynames._roman_numeral(13), 'XIII')
        self.assertEqual(lynames._roman_numeral(14), 'XIV')
        self.assertEqual(lynames._roman_numeral(15), 'XV')
        self.assertEqual(lynames._roman_numeral(16), 'XVI')
        self.assertEqual(lynames._roman_numeral(17), 'XVII')
        self.assertEqual(lynames._roman_numeral(18), 'XVIII')
        self.assertEqual(lynames._roman_numeral(19), 'XIX')
        self.assertEqual(lynames._roman_numeral(20), 'XX')

    def test_twenty_one_thru_thirty(self):
        """Tests twenty one through thirty roman numerals."""
        self.assertEqual(lynames._roman_numeral(21), 'XXI')
        self.assertEqual(lynames._roman_numeral(22), 'XXII')
        self.assertEqual(lynames._roman_numeral(23), 'XXIII')
        self.assertEqual(lynames._roman_numeral(24), 'XXIV')
        self.assertEqual(lynames._roman_numeral(25), 'XXV')
        self.assertEqual(lynames._roman_numeral(26), 'XXVI')
        self.assertEqual(lynames._roman_numeral(27), 'XXVII')
        self.assertEqual(lynames._roman_numeral(28), 'XXVIII')
        self.assertEqual(lynames._roman_numeral(29), 'XXIX')
        self.assertEqual(lynames._roman_numeral(30), 'XXX')

    def test_large_numbers(self):
        """Test some arbitrary large numbers."""
        self.assertEqual(lynames._roman_numeral(40), 'IL')
        self.assertEqual(lynames._roman_numeral(43), 'ILIII')
        self.assertEqual(lynames._roman_numeral(50), 'L')
        self.assertEqual(lynames._roman_numeral(59), 'LIX')
        self.assertEqual(lynames._roman_numeral(78), 'LXXVIII')
        self.assertEqual(lynames._roman_numeral(89), 'LXXXIX')

    def test_errors(self):
        self.assertRaisesRegex(
            TypeError,
            'num.*int',
            lynames._roman_numeral,
            'hi'
        )
        self.assertRaisesRegex(
            ValueError,
            '.*1 and 89',
            lynames._roman_numeral,
            90
        )
        self.assertRaisesRegex(
            ValueError,
            '.*1 and 89',
            lynames._roman_numeral,
            0
        )


class TestLyName(unittest.TestCase):
    """Test the LyName class methods."""

    def test_init(self):
        """Test normalization of name input."""
        test1 = lynames.LyName('TEST name ')
        self.assertEqual(
            test1.name,
            'test_name'
        )

        test2 = lynames.LyName('  another_test-name')
        self.assertEqual(
            test2.name,
            'another_test_name'
        )

    def test_movement(self):
        """Test movement method for num and word."""
        testlyname = lynames.LyName('global')
        testlyname2 = lynames.LyName('test')
        testlyname2.number = 2
        testlyname2._numword = 'two'
        self.assertEqual(
            testlyname.file_name(1),
            'global_1'
        )

        self.assertEqual(
            testlyname.file_name(2),
            'global_2'
        )

        self.assertEqual(
            testlyname2.file_name(1),
            'test2_1'
        )

        self.assertEqual(
            testlyname.var_name(2),
            'global_second_mov'
        )

        self.assertEqual(
            testlyname.var_name(31),
            'global_thirty_first_mov'
        )

        self.assertEqual(
            testlyname2.var_name(2),
            'test_two_second_mov'
        )

        # test exceptions
        self.assertRaisesRegex(
            TypeError,
            ".*'form'.*",
            testlyname._movement,
            1
        )

        self.assertRaisesRegex(
            TypeError,
            '.*integer',
            testlyname._movement,
            '10',
            form='word'
        )

        self.assertRaisesRegex(
            ValueError,
            ".*'form'.*'word'",
            testlyname._movement,
            10,
            form='fail'
        )


class TestInstrument(unittest.TestCase):
    """
    Test the Instrument Class.
    Some of this is really more like integration tests.
    """
    def setUp(self):
        self.test_ins = lynames.Instrument.numbered_name('VioliN', 1)
        self.test_ins2 = lynames.Instrument.numbered_name('violoncello', 2,
                                                          abbr='Vc.',
                                                          clef='bass',
                                                          midi='violoncello')
        self.test_ins3 = lynames.Instrument('Clarinet in Bb', abbr='Cl.',
                                            clef='treble',
                                            transposition='Bb',
                                            keyboard=False,
                                            midi='clarinet'
                                            )

    def test_numbered_name(self):
        """Test the numbered name class method."""
        self.assertEqual(self.test_ins.name, 'violin')
        self.assertEqual(self.test_ins.number, 1)
        self.assertEqual(self.test_ins._numword, 'one')
        self.assertEqual(self.test_ins._roman, 'I')
        self.assertEqual(self.test_ins.abbr, '')
        self.assertEqual(self.test_ins.clef, 'treble')
        self.assertIsNone(self.test_ins.transposition)
        self.assertFalse(self.test_ins.keyboard)
        self.assertIsNone(self.test_ins.midi)

        self.assertEqual(self.test_ins2.name, 'violoncello')
        self.assertEqual(self.test_ins2.number, 2)
        self.assertEqual(self.test_ins2._numword, 'two')
        self.assertEqual(self.test_ins2._roman, 'II')
        self.assertEqual(self.test_ins2.abbr, 'Vc.')
        self.assertEqual(self.test_ins2.clef, 'bass')
        self.assertIsNone(self.test_ins2.transposition)
        self.assertFalse(self.test_ins2.keyboard)
        self.assertEqual(self.test_ins2.midi, 'violoncello')

    def test_init_with_attribs(self):
        """
        Test direct initialization with transposition and normalization of the
        name.
        """
        self.assertEqual(self.test_ins3.transposition, 'Bb')
        self.assertEqual(self.test_ins3.name, 'clarinet_in_bb')
        self.assertIsNone(self.test_ins3.number)

    def test_part_name(self):
        """Tests the part_name method."""
        self.assertEqual(self.test_ins.part_name(), 'Violin I')
        self.assertEqual(self.test_ins2.part_name(), 'Violoncello II')
        self.assertEqual(self.test_ins3.part_name(), 'Clarinet in Bb')

    def test_load_from_db(self):
        """Tests loading an object from tinydb."""
        # mock the db and table objects
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

        self.assertEqual(
            lynames.Instrument.load_from_db('flute', mock_db),
            lynames.Instrument(
                'flute',
                abbr='Fl.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='flute'
            )
        )

        # make sure it still works with numbers
        self.assertEqual(
            lynames.Instrument.load_from_db('flute', mock_db, number=2),
            lynames.Instrument.numbered_name(
                'flute',
                number=2,
                abbr='Fl.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='flute'
            )
        )

        # if not found, it should raise InstrumentNotFoundError.
        mock_table.get.return_value = None
        # if not found, 'get' from the table will return none.
        self.assertRaisesRegex(
            exceptions.InstrumentNotFoundError,
            '.*not in.*table',
            lynames.Instrument.load_from_db,
            'fail',
            mock_db
        )

    def test_add_to_db(self):
        """Tests adding an object to the database."""
        mock_db = mock.MagicMock()
        mock_table = mock.MagicMock()
        mock_db.table.return_value = mock_table

        self.test_ins.add_to_db(mock_db)
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
        self.test_ins2.add_to_db(mock_db)
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
        self.test_ins3.add_to_db(mock_db)
        mock_table.insert.assert_called_once_with(
            {'name': 'clarinet_in_bb',
             'abbr': 'Cl.',
             'clef': 'treble',
             'transposition': 'Bb',
             'keyboard': False,
             'midi': 'clarinet'
             }
        )
