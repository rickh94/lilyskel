"""Classes for names of files and directories."""
import re
import attr
from num2words import num2words


def _normalize(name):
    """Clean up the names."""
    clean = re.sub(r'[-_\s]+', '_', name.strip())
    return clean.lower()


def _form_num(num, *, form):
    """Return either a number or a number word."""
    # TODO: add roman numeral option
    if form == 'num':
        return str(num)
    elif form == 'word':
        return _normalize(num2words(num))
    elif form == 'ord':
        return _normalize(num2words(num, ordinal=True))
    else:
        raise ValueError("'form' must be 'num', 'ord', or 'word'")


@attr.s
class LyName():
    """Common attributes/names"""
    name = attr.ib(convert=_normalize)
    _number = attr.ib(init=False)
    _numword = attr.ib(init=False)
    _roman = attr.ib(init=False)

    def _movement(self, mov_num, *, form):
        """
        Returns name and movement as number or word.
        Arguments:
            mov_num: an int that is the number of the movement.
            form: required keyword arg. 'num' for numeral, 'ord' for ordinal.
        """
        if not isinstance(mov_num, int):
            raise TypeError("'mov_num' must be an integer")
        try:
            full_name = self.name + '_' + self.numword
        except AttributeError:
            full_name = self.name

        num = _form_num(mov_num, form=form)
        if form == 'ord':
            num += '_mov'
        return self.name + '_' + num

    def file_name(self, mov_num):
        """Returns the filename form for a part + movement."""
        return self._movement(mov_num, form='num')

    def var_name(self, mov_num):
        """Returns the variable name for a part + movement."""
        return self._movement(mov_num, form='ord')




class Instrument(LyName):
    """Class for Instruments."""
    def part_name(self):
        """Returns the name for printing on a part."""

    @classmethod
    def numbered_name(cls, name, number):
        """Returns a numbered lyname class."""
        new_obj = cls(name)
        new_obj.number = number
        new_obj.numword = _normalize(num2words(number))
        new_obj.roman = _normalize(num2roman(number))
