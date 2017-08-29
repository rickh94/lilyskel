"""Classes for names of files and directories."""
import re
import attr
from num2words import num2words
from titlecase import titlecase
from tinydb import Query
from . import exceptions


def _normalize(name):
    """Clean up the names."""
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
        raise TypeError('num must be an int')
    if num > 89 or num < 1:
        raise NotImplementedError('Only supports numbers between 1 and 89')
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

    def file_name(self, mov_num):
        """Returns the filename form for a part + movement."""
        return self._movement(mov_num, form='num')

    def var_name(self, mov_num):
        """Returns the variable name for a part + movement."""
        return self._movement(mov_num, form='ord')


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
    """
    abbr = attr.ib(default='')
    clef = attr.ib(default='treble')
    transposition = attr.ib(default=None)
    keyboard = attr.ib(default=False)
    midi = attr.ib(default=None)

    def part_name(self):
        """Returns the name for printing on a part."""
        name = titlecase(' '.join(self.name.split('_')))
        # _roman is only needed if self was initialized with a number.
        try:
            name += ' ' + self._roman
        except (AttributeError, TypeError):
            pass
        if 'In' in name:
            name.replace('In', 'in')
        return name

    @classmethod
    def numbered_name(cls, name, number, *, abbr='', clef='treble',
                      transposition=None, keyboard=False, midi=None):
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
                      midi=midi)
        new_obj.number = number
        new_obj._numword = _form_num(number, form='word')
        new_obj._roman = _form_num(number, form='roman')
        return new_obj

    # TODO: needs test
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
        Ins = Query()
        # get an object matching name from the db.
        ins_table = db.table('instruments')
        data = ins_table.get(Ins.name == name)
        if data is None:
            raise exceptions.InstrumentNotFoundError(
                "'{name}' is not in the 'instruments' table.".format(name=name)
            )
        if number is not None:
            new_obj = cls.numbered_name(name, number)
        else:
            new_obj = cls(name)

        for key, val in data.items():
            setattr(new_obj, key, val)
        return new_obj

    # TODO: needs test
    def add_to_db(self, db):
        """
        Serializes the Instrument and adds it to the supplied database in the
        'instruments' table.

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
