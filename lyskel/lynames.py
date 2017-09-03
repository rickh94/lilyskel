"""Classes for names of files and directories."""
import re
import attr
from fuzzywuzzy import process
from num2words import num2words
from titlecase import titlecase
from lyskel import exceptions
from lyskel import mutopia
from lyskel.db_interface import load_name_from_table, explore_table


def _normalize(name):
    """Clean up the names."""
    if name is None:
        return None
    clean = re.sub(r'[-_\s]+', '_', name.strip())
    return clean.lower()


def _form_num(num, *, form):
    """Return either a number or a number word."""
    if form == 'num':
        return str(num)
    elif form == 'word':
        return _normalize(num2words(num))
    elif form == 'ord':
        return _normalize(num2words(num, ordinal=True))
    elif form == 'roman':
        return _roman_numeral(num)
    else:
        raise ValueError("'form' must be 'num', 'ord', or 'word'")


def _roman_numeral(num):
    """
    Take an int and return a roman numberal as standard ascii characters.

    Arguments:
        num: a number to convert. Must be between 1 and 89 (inclusive)
    """
    if not isinstance(num, int):
        raise TypeError("'num' must be an int")
    if num > 89 or num < 1:
        raise ValueError('Only supports numbers between 1 and 89')
    numeral_dict = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        5: 'V',
        6: 'VI',
        7: 'VII',
        8: 'VIII',
        9: 'IX',
        10: 'X'
    }
    # just a precaution. we will be depleting num_copy
    num_copy = num
    roman_numeral = ''
    if num >= 50:
        roman_numeral += 'L'
        num_copy -= 50
    elif 40 <= num < 50:
        roman_numeral += 'IL'
        num_copy -= 40

    while num_copy > 10:
        roman_numeral += 'X'
        num_copy -= 10

    if num_copy != 0:
        roman_numeral += numeral_dict.get(num_copy)

    return roman_numeral


@attr.s
class LyName():
    """Common attributes/names"""
    name = attr.ib(convert=_normalize)
    number = attr.ib(init=False, default=None)
    _numword = attr.ib(init=False, repr=False)
    _roman = attr.ib(init=False, repr=False)

    def _movement(self, mov_num, *, form):
        """
        Returns name and movement as number or word.
        Arguments:
            mov_num: an int that is the number of the movement.
            form: required keyword arg. 'num' for numeral, 'ord' for ordinal.
        """
        if not isinstance(mov_num, int):
            raise TypeError("'mov_num' must be an integer")
        # pdb.set_trace()
        if self.number is not None:
            if form == 'ord' or form == 'word':
                full_name = self.name + '_' + self._numword
            else:
                full_name = self.name + str(self.number)
        else:
            full_name = self.name

        num = _form_num(mov_num, form=form)
        if form == 'ord':
            num += '_mov'
        return full_name + '_' + num

    def mov_file_name(self, mov_num):
        """Returns the filename form for a part + movement."""
        return self._movement(mov_num, form='num') + '.ily'

    def part_file_name(self, prefix=''):
        """Returns a plain file name with a prefix prepended."""
        if prefix:
            name = str(prefix) + '_' + self.name
        else:
            name = self.name
        if self.number is not None:
            name += str(self.number)
        return name + '.ly'

    def dir_name(self):
        """Returns a directory name."""
        name = self.name
        if self.number is not None:
            name += str(self.number)
        return name

    def var_name(self, mov_num):
        """Returns the variable name for a part + movement."""
        return '\\' + self._movement(mov_num, form='ord')


@attr.s
class Instrument(LyName):
    """
    Class for Instruments.
    Inherits from LyName
    Additional Attributes:
        abbr: Short abbreviation for the instrument name.
        clef: The instrument's usual clef
        transposition: the key in which the instrument plays. Defaults to None
        for concert pitch.
        keyboard: (bool) specifies whether it is a keyboard instrument. (To
        know whether to create multiple staves.)
        midi: the corresponding midi instrument.
        family: the family of the instrument (e.g. woodwinds, strings, etc.)
        mutopianame: the name of the instrument as in mutopia
    """
    # pylint: disable=protected-access
    abbr = attr.ib(default='')
    clef = attr.ib(default='treble')
    transposition = attr.ib(default=None)
    keyboard = attr.ib(default=False)
    midi = attr.ib(default=None)
    family = attr.ib(default=None, convert=_normalize)
    mutopianame = attr.ib(default=None)

    def part_name(self, key=False):
        """
        Returns the name for printing on a part.
        Arguments:
            key: (bool) Specifies whether to include key/transposition in name.
        """
        # pylint: disable=no-member
        name = titlecase(' '.join(self.name.split('_')))
        # _roman is only needed if self was initialized with a number.
        try:
            name += ' ' + self._roman
        except (AttributeError, TypeError):
            pass
        if not key:
            if ' in ' in name:
                name = re.sub(' in .*', '', name)
        return name

    @classmethod
    def numbered_name(cls, name, number, *, abbr='', clef='treble',
                      transposition=None, keyboard=False, midi=None,
                      family=None):
        """
        Returns a numbered Instrument class. (e.g. Violin 1, Violin 2)

        Arguments:
            name: the name of the class.
            number: an int describing the number of the instrument (supports up
            to 89)
            *: optional attributes to set on instance. (See Instrument() for
            details). Must be keyword args.
        """
        new_obj = cls(name, abbr=abbr, clef=clef,
                      transposition=transposition, keyboard=keyboard,
                      midi=midi, family=family)
        new_obj.number = number
        new_obj._numword = _form_num(number, form='word')
        new_obj._roman = _form_num(number, form='roman')
        return new_obj

    @classmethod
    def load_from_db(cls, name, db, number=None):
        """
        Returns an instance with data from a tinydb database or raises an
        Exception.

        Arguments:
            name: the name of the instrument to retrieve.
            db: A tinydb database that has an instruments table.
            number: (optional) The number of the instrument in the ensemble.
            (e.g. Violin 1)
        """
        name = _normalize(name)
        data = load_name_from_table(name, db, 'instruments')
        if number is not None:
            new_obj = cls.numbered_name(name, number)
        else:
            new_obj = cls(name)

        for key, val in data.items():
            setattr(new_obj, key, val)
        return new_obj

    def add_to_db(self, db):
        """
        Serializes the Instrument and adds it to the supplied database in the
        'instruments' table.
        This should only be called after load_from_db fails or the databse is
        otherwise checked so duplicates aren't added to the database.

        Arguments:
            db: a tinydb instance to insert into.
        """
        ins_table = db.table('instruments')
        data = attr.asdict(self,
                           filter=attr.filters.exclude(
                               attr.fields(Instrument)._roman,
                               attr.fields(Instrument)._numword,
                               attr.fields(Instrument).number
                           ))
        ins_table.insert(data)

    def get_mutopia_name(self):
        """Gets the mutopia version of the Instrument's name."""
        if self.mutopianame is not None:
            return self.mutopianame
        instrs = mutopia._get_instruments()
        choice, _ = process.extractOne(self.name, instrs)
        self.mutopianame = choice
        return choice


@attr.s
class Ensemble():
    """A group of instruments."""
    name = attr.ib(convert=_normalize)
    instruments = attr.ib(default=None)

    def add_instrument(self, ins_name, *, db=None, number=None, abbr='',
                       clef='treble', keyboard=False, midi=None,
                       transposition=None, family=None):
        """
        Add an instrument to the ensemble.

        Arguments:
            ins_name: the name of the desired instrument.
            number: the number of the instrument. (see Instrument for details.)
            db: the database to load instruments from. (if the instrument is
            not present, it will cause DataNotFoundError.
        """
        if self.instruments is None:
            self.instruments = []
        # if a database is present, try to load from it.
        if db is not None:
            new_ins = Instrument.load_from_db(ins_name, db, number=number)
        elif number is not None:
            new_ins = Instrument.numbered_name(
                ins_name, number=number, abbr=abbr, clef=clef, midi=midi,
                keyboard=keyboard, transposition=transposition, family=family)
        else:
            new_ins = Instrument(ins_name, abbr=abbr, clef=clef, midi=midi,
                                 keyboard=keyboard, family=family)
        self.instruments.append(new_ins)

    @classmethod
    def load_from_db(cls, name, db):
        """
        Load ensemble and instruments from database.
        NOTE: This method enforces that if an ensemble is in the database, all
        of its instruments MUST be in the database. If they are not, it will
        fail to create.

        Arguments:
            name: the name of the ensemble
            db: a TinyDB object
        """
        name = _normalize(name)
        data = load_name_from_table(name, db, 'ensembles')
        new_ens = cls(name, instruments=[])
        try:
            for insdata in data['instruments']:
                new_ins = Instrument.load_from_db(name=insdata['name'],
                                                  db=db,
                                                  number=insdata['number'])
                new_ens.instruments.append(new_ins)
        except exceptions.DataNotFoundError as err:
            raise exceptions.MissingInstrumentError(
                "An instrument specified for {name} was not found in the "
                "database. This is not allowed. Details follow: {e}".format(
                    name=name, e=err))
        return new_ens

    def add_to_db(self, db):
        """
        Serializes the Ensemble and adds it to the supplied database in the
        'ensembles' table.
        This should only be called after load_from_db fails or the databse is
        otherwise checked so duplicates aren't added to the database.

        Arguments:
            db: a tinydb instance to insert into.
        """
        ens_table = db.table('ensembles')
        ins_table = db.table('instruments')
        data = {'name': self.name}
        data['instruments'] = []
        for instrument in self.instruments:
            # if the instrument isn't in the database
            if not explore_table(ins_table, search=('name', instrument.name)):
                instrument.add_to_db(db)
            data['instruments'].append(
                {'name': instrument.name, 'number': instrument.number})
        ens_table.insert(data)
