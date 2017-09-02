"""Classes for files and file info."""
import attr
from lyskel.lynames import Instrument, Ensemble
from lyskel import mutopia
from lyskel import exceptions
from lyskel import db_interface
# pylint: disable=too-few-public-methods,protected-access


@attr.s
class Composer():
    """Stores and formats information about a composer."""
    name = attr.ib(validator=attr.validators.instance_of(str))
    mutopianame = attr.ib(default=None)
    shortname = attr.ib(default=None)

    def get_short_name(self):
        # pylint: disable=no-member,unsubscriptable-object
        """Returns shortened composer name. Generates if not present."""
        if self.shortname is not None:
            return self.shortname
        sname = ''
        name_parts = self.name.split()
        lname = name_parts.pop()
        for part in name_parts:
            sname += part[0] + '.'

        # This prevents leading spaces on single name composers
        if sname:
            sname += ' '
        sname += lname
        self.shortname = sname
        return sname

        # pylint: enable=no-member,unsubscriptable-object

    def get_mutopia_name(self, guess=False):
        """
        Get the mutopia name for a composer.
        Arugments:
            guess: if True, a guess will be made at the mutopia name of a
            composer.
        """
        if self.mutopianame is not None:
            return self.mutopianame
        elif guess:
            mutopia_composers = mutopia._get_composers()
            # pylint: disable=no-member
            namelist = self.name.split()
            # pylint: enable=no-member
            lname = namelist.pop()
            # get first inital to check
            try:
                fletter = namelist[0][0]
            # protect against single name composers
            except IndexError:
                fletter = ''
            for comp in mutopia_composers:
                if lname in comp and fletter in comp:
                    self.mutopianame = comp
                    return comp
            # if it hasn't returned yet, nothing is there.
            raise exceptions.MutopiaError("No matching composer found.")
        else:
            raise AttributeError("No mutopia name defined.")

    @classmethod
    def load_from_db(cls, name, db):
        """
        Loads a composer from the database.

        Arguments:
            name: part or all of a composer's name
            db: a TinyDB instance
        """
        table = db.table('composers')
        name_parts = name.split(' ')
        lname = name_parts.pop()
        comps = db_interface.explore_table(table=table, search=('name', lname))
        if not isinstance(comps, list):
            comps = [comps]
        for item in comps:
            if name_parts[0] in item:
                print(item)
                data = db_interface.load_name_from_table(item, db=db,
                                                         tablename='composers')
                name = data['name']
                try:
                    mutopianame = data['mutopianame']
                except KeyError:
                    mutopianame = None
                try:
                    shortname = data['shortname']
                except KeyError:
                    shortname = None

        return cls(name=name, mutopianame=mutopianame, shortname=shortname)

    def add_to_db(self, db):
        """
        Serializes the Instrument and adds it to the supplied database in the
        'composers' table.
        This should only be called after load_from_db fails or the databse is
        otherwise checked so duplicates aren't added to the database.

        Arguments:
            db: a tinydb instance to insert into.
        """
        comp_table = db.table('composers')
        data = attr.asdict(self)
        comp_table.insert(data)


def _validate_mutopia_headers(headers):
    if headers is not None and not isinstance(headers, MutopiaHeaders):
        raise TypeError("mutopiaheaders is defined but not a MutopiaHeaders"
                        " object.")


@attr.s
class Headers():
    """Class for storing header info."""
    title = attr.ib()
    composer = attr.ib(default=Composer('Anonymous'),
                       validator=attr.validators.instance_of(Composer))
    dedication = attr.ib(default=None)
    subtitle = attr.ib(default=None)
    subsubtitle = attr.ib(default=None)
    poet = attr.ib(default=None)
    meter = attr.ib(default=None)
    arranger = attr.ib(default=None)
    tagline = attr.ib(default=None)
    copyright = attr.ib(default=None)
    mutopiaheaders = attr.ib(default=None)

    def add_mutopia_headers(self, mu_headers, guess_composer=False):
        """
        Add mutopia headers.
        Arguments:
            mu_headers: a MutopiaHeaders object
            guess_composer: Whether to guess at the mutopiacomposer if not set.
        """
        # pylint: disable=no-member
        mu_headers.composer = self.composer.mutopia_name(guess=guess_composer)
        # pylint: enable=no-member
        mutopia_instrument_names =\
            [instrument.mutopianame for
             instrument in mu_headers.instrument_list]
        instruments = ', '.join(mutopia_instrument_names)
        mu_headers.instruments = instruments


def validate_instruments(instruments):
    """Validates either a list of instruments or instance of Ensemble."""
    if isinstance(instruments, list):
        if isinstance(instruments[0], Instrument):
            pass
    elif isinstance(instruments, Ensemble):
        pass
    else:
        raise TypeError("'instruments' must be a list of instruments or an "
                        "Ensemble instance.")


def convert_ensemble(instruments):
    """Returns list of instruments for mutopia headers."""
    if isinstance(instruments, Ensemble):
        return instruments.instruments
    return instruments


def _validate_style(style):
    """Calls validate_mutopia with field 'style'"""
    return mutopia.validate_mutopia(data=style, field='style')


def _validate_composer(comp):
    """Calls validate_mutopia with field 'mutopiacomposer'"""
    return mutopia.validate_mutopia(data=comp, field='mutopiacomposer')


def _validate_license(license_):
    """Calls validate_mutopia with field 'license'"""
    return mutopia.validate_mutopia(data=license_, field='license')


@attr.s
class MutopiaHeaders():
    """
    The headers available for Mutopia project submissions. See www.mutopia.org
    for more details.
    """
    instrument_list = attr.ib(validator=validate_instruments,
                              convert=convert_ensemble)
    source = attr.ib(validator=attr.validators.instance_of(str))
    style = attr.ib(validator=_validate_style)
    composer = attr.ib(init=False, validator=_validate_composer)
    maintainer = attr.ib(default="Anonymous")
    maintainerEmail = attr.ib(default=None)
    maintainerWeb = attr.ib(default=None)
    mutopiatitle = attr.ib(default=None)
    mutopiapoet = attr.ib(default=None)
    mutopiaopus = attr.ib(default=None)
    date = attr.ib(default=None)
    moreinfo = attr.ib(default=None)


@attr.s
class Piece():
    """
    Info for the entire piece.
    """
    name = attr.ib()
    headers = attr.ib(validator=attr.validators.instance_of(Headers))
