"""Tests for LyName and it's child classes."""
from unittest import mock
import pytest
from tinydb import TinyDB, Query
from lyskel import lynames
from lyskel import exceptions
# pylint: disable=protected-access,no-self-use


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
        """Test that invalid input raises an exception."""
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
        assert test1.name == 'test_name', "name should be normalized"
        assert test1.number is None, "Number should be None if not specified"

        test2 = lynames.LyName('  another_test-name')
        assert test2.name == 'another_test_name', "name should be normalized"
        assert test2.number is None, "Number should be None if not specified"

    def test_movement(self):
        """Tests file_name and var_name methods and related exceptions."""
        testlyname1 = lynames.LyName('global')
        testlyname2 = lynames.LyName('test')
        testlyname2.number = 2
        testlyname2._numword = 'two'

        # test file_name
        assert testlyname1.file_name(1) == 'global_1', "should append number"
        assert testlyname1.file_name(2) == 'global_2', "should append number"
        assert testlyname2.file_name(1) == 'test2_1', "should append number"

        # test var_name
        assert testlyname1.var_name(2) == 'global_second_mov',\
            "should append number words"
        assert testlyname1.var_name(31) == 'global_thirty_first_mov',\
            "should append number words"
        assert testlyname2.var_name(2) == 'test_two_second_mov',\
            "should append number words"

        # test exceptions
        with pytest.raises(TypeError,
                           message="Expect TypeError if form no specified.",
                           match=".*'form'.*"):
            testlyname1._movement(1)  # pylint: disable=missing-kwoa

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
                                            clef='bass', midi='violoncello',
                                            family='strings')


@pytest.fixture(scope='module')
def test_ins3():
    """A third test instrument."""
    return lynames.Instrument('Clarinet in Bb', abbr='Cl.', clef='treble',
                              transposition='Bb', keyboard=False,
                              midi='clarinet', family='woodwinds')


@pytest.fixture
def mockdb():
    """A mocked database."""
    mock_db = mock.MagicMock(spec=TinyDB)
    mock_table = mock.MagicMock()
    mock_db.table.return_value = mock_table
    mock_table.get.return_value = {
        'name': 'flute',
        'abbr': 'Fl.',
        'clef': 'treble',
        'transposition': None,
        'keyboard': False,
        'midi': 'flute',
        'family': 'woodwinds'
    }
    return mock_db


class TestInstrument():
    """
    Test the Instrument Class.
    Some of this is really more like integration tests.
    """
    # pylint: disable=redefined-outer-name
    def test_numbered_name(self, test_ins, test_ins2):
        """Test the numbered name class method."""
        assert test_ins.name == 'violin', "name should be normalized"
        assert test_ins.number == 1, "number should be as specified"
        assert test_ins._numword == 'one', "numword should be generated"
        assert test_ins._roman == 'I', "roman numeral should be generated"
        assert test_ins.abbr == '', "should be default"
        assert test_ins.clef == 'treble', "should be default"
        assert test_ins.transposition is None, "should be default"
        assert test_ins.keyboard is False, "should be default"
        assert test_ins.midi is None, "should be default"
        assert test_ins.family is None, "should be default"

        assert test_ins2.name == 'violoncello', "name should be normalized"
        assert test_ins2.number == 2, "number should be as specified"
        assert test_ins2._numword == 'two', "numword should be generated"
        assert test_ins2._roman == 'II', "roman numeral should be generated"
        assert test_ins2.abbr == 'Vc.', "should be as specified"
        assert test_ins2.clef == 'bass', "should be as specified"
        assert test_ins2.transposition is None, "should be default"
        assert test_ins2.keyboard is False, "should be default"
        assert test_ins2.midi == 'violoncello', "should be as specified"
        assert test_ins2.family == 'strings', "should be as specified"

    def test_init_with_attribs(self, test_ins3):
        """
        Test direct initialization with transposition and normalization of the
        name.
        """
        as_specified = "should be as specified"
        assert test_ins3.name == 'clarinet_in_bb', "name should be normalized"
        assert test_ins3.number is None, "Should be none unless specified"
        assert test_ins3.abbr == 'Cl.', as_specified
        assert test_ins3.clef == 'treble', as_specified
        assert test_ins3.transposition == 'Bb', as_specified
        assert test_ins3.keyboard is False, as_specified
        assert test_ins3.midi == 'clarinet', as_specified
        assert test_ins3.family == 'woodwinds', as_specified

    def test_part_name(self, test_ins, test_ins2, test_ins3):
        """Tests the part_name method."""
        assert test_ins.part_name() == 'Violin I', "should be pretty"
        assert test_ins2.part_name() == 'Violoncello II', "should be pretty"
        assert test_ins3.part_name() == 'Clarinet', "should be pretty"
        assert test_ins3.part_name(key=True) == 'Clarinet in Bb',\
            "should have key in name"

    def test_load_from_db(self, mockdb, livedb):
        """Tests loading an object from tinydb."""
        assert lynames.Instrument.load_from_db('flute', mockdb) ==\
            lynames.Instrument(
                'flute',
                abbr='Fl.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='flute',
                family='woodwinds'
            ), "should load all attributes from database"

        # make sure it still works with numbers
        assert lynames.Instrument.load_from_db('flute', mockdb, number=2) ==\
            lynames.Instrument.numbered_name(
                'flute',
                number=2,
                abbr='Fl.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='flute',
                family='woodwinds'
            ), "should load all attributes from database and have numbers"

        assert lynames.Instrument.load_from_db('violin', livedb) ==\
            lynames.Instrument(
                'violin',
                abbr='Vln.',
                clef='treble',
                transposition=None,
                keyboard=False,
                midi='violin',
                family='strings'
            ), "Should load correctly from actual default database."

        # if not found, it should raise DataNotFoundError.
        failtable = mock.MagicMock()
        mockdb.table.return_value = failtable
        failtable.get.return_value = None
        # if not found, 'get' from the table will return none.
        with pytest.raises(exceptions.DataNotFoundError,
                           message=("expect DataNotFoundError if "
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
             'midi': None,
             'family': None
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
             'midi': 'violoncello',
             'family': 'strings'
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
             'midi': 'clarinet',
             'family': 'woodwinds'
             }
        )


@pytest.fixture
def violin1(livedb):
    """A violin 1 object."""
    return lynames.Instrument.load_from_db('violin', number=1, db=livedb)


@pytest.fixture
def violin2(livedb):
    """A violin 2 object."""
    return lynames.Instrument.load_from_db('violin', number=2, db=livedb)


@pytest.fixture
def viola(livedb):
    """A violin 2 object."""
    return lynames.Instrument.load_from_db('viola', db=livedb)


@pytest.fixture
def violoncello(livedb):
    """A violin 2 object."""
    return lynames.Instrument.load_from_db('violoncello', db=livedb)


class TestEnsemble():
    """Test the Ensemble Class."""
    # pylint: disable=redefined-outer-name
    def test_add_instrument(self, livedb, violin1):
        """Test adding an instrument."""
        test_ens = lynames.Ensemble('test_ensemble')
        test_ens.add_instrument(ins_name='violin', number=1, db=livedb)
        assert violin1 in test_ens.instruments, ("Should have loaded 'violin' "
                                                 "object from the database")

        test_ens.add_instrument(ins_name='glockenSPiel', number=1, abbr='Gl.',
                                clef='treble', keyboard=False,
                                midi='glockenspiel', family='PERCUSsion')
        glock = lynames.Instrument.numbered_name(name='glockenspiel', number=1,
                                                 abbr='Gl.', clef='treble',
                                                 keyboard=False,
                                                 midi='glockenspiel',
                                                 family='percussion')
        assert glock in test_ens.instruments, ("Should have created "
                                               "'glockenspiel' object from "
                                               "arguments and normalized it.")

    def test_load_from_db(self, livedb, monkeypatch, violin1, violin2,
                          viola, violoncello):
        """Test loading an ensemble from the database."""
        test_ens = lynames.Ensemble.load_from_db('STRING QUARTET', livedb)
        assert test_ens.name == 'string_quartet', "Name should be normalized"
        assert violin1 in test_ens.instruments, "should load violin 1"
        assert violin2 in test_ens.instruments, "should load violin 2"
        assert viola in test_ens.instruments, "should load viola"
        assert violoncello in test_ens.instruments, "should load violoncello"

        # pylint: disable=unused-argument
        def raises_data_not_found(*args, **kwargs):
            """Raises DataNotFoundError."""
            raise exceptions.DataNotFoundError('thing not found here')
        # pylint: enable=unused-argument

        monkeypatch.setattr("lyskel.lynames.Instrument.load_from_db",
                            raises_data_not_found)

        with pytest.raises(exceptions.MissingInstrumentError,
                           message=("Expect MissingInstrumentError if "
                                    "no instruments are found (i.e. "
                                    "Instrument.load_from_db raises "
                                    "DataNotFoundError)."),
                           match=(".*instrument.*string_quartet.*database"
                                  ".*thing not found here.*")):
            lynames.Ensemble.load_from_db('string_quartet', livedb)

    def test_add_to_db(self, livedb):
        """Test adding to the database."""
        wind_quartet = lynames.Ensemble('Wind Quartet')
        wind_quartet.add_instrument('flute', abbr='Fl.', midi='flute',
                                    family='woodwinds')
        wind_quartet.add_instrument('clarinet_in_bb', abbr='Cl.',
                                    midi='clarinet', transposition='Bb',
                                    family='woodwinds')
        wind_quartet.add_instrument('Oboe', abbr='Ob.',
                                    midi='oboe', family='woodwinds')
        wind_quartet.add_instrument('Bassoon', abbr='Bsn.',
                                    midi='bassoon', family='woodwinds')
        wind_quartet.add_to_db(livedb)
        Search = Query()
        ensembles = livedb.table('ensembles')
        instruments = livedb.table('instruments')
        assert ensembles.search(Search.name == 'wind_quartet'),\
            ("There should be an object in the database with the name "
             "wind_quartet (therefore search should return a list, which "
             "is implicitly true.")
        wq = ensembles.get(Search.name == 'wind_quartet')
        instrument_list = [
            {'name': 'flute', 'number': None},
            {'name': 'oboe', 'number': None},
            {'name': 'clarinet_in_bb', 'number': None},
            {'name': 'bassoon', 'number': None}
        ]
        for ins in instrument_list:
            assert ins in wq['instruments'], ("All instrument names should be "
                                              "represented in the db.")

        # all instruments should have been added to the database.
        assert instruments.search(Search.name == 'flute'),\
            "There should be a flute in the database now."
        assert instruments.search(Search.name == 'oboe'),\
            "There should be a oboe in the database now."
        assert instruments.search(Search.name == 'clarinet_in_bb'),\
            "There should be a clarinet_in_bb in the database now."
        assert instruments.search(Search.name == 'bassoon'),\
            "There should be a bassoon in the database now."

        wind_quartet_loaded = lynames.Ensemble.load_from_db('wind quartet',
                                                            livedb)

        assert wind_quartet_loaded == wind_quartet, ("The object loaded from "
                                                     "the database should be "
                                                     "the same as the one "
                                                     "that was added to it.")
