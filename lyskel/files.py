"""Classes for files and file info."""
import attr
from lyskel.lynames import Instrument, Ensemble
from lyskel import mutopia


@attr.s
class Composer():
    """Stores and formats information about a composer."""
    name = attr.ib()
    mutopianame = attr.ib(default=None)

    def mutopia_name(guess=False):
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
            namelist = name.split()
            lname = namelist[-1]
            for comp in mutopia_composers:
                if lname in comp:
                    self.mutopianame = comp
                    return comp
        else:
            raise AttributeError("No mutopia name defined.")


def _validate_mutopia_headers(headers):
    if headers is not None and not isinstance(headers, MutopiaHeaders):
        raise TypeError("mutopiaheaders is defined but not a MutopiaHeaders
                        " object.")


@attr.s
class Headers():
    """Class for storing header info."""
    dedication = attr.ib(default=None)
    title = attr.ib()
    subtitle = attr.ib(default=None)
    subsubtitle = attr.ib(default=None)
    poet = attr.ib(default=None)
    composer = attr.ib(Composer('Anonymous'))
    meter = attr.ib(default=None)
    arranger = attr.ib(default=None)
    tagline = attr.ib(default=None)
    copyright = attr.ib(default=None)
    mutopiaheaders = attr.ib(default=None,
                             validator=_validate_mutopia_headers)


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


def _validate_license(license):
    """Calls validate_mutopia with field 'license'"""
    return mutopia.validate_mutopia(data=license, field='license')


@attr.s
class MutopiaHeaders():
    """
    The headers available for Mutopia project submissions. See www.mutopia.org
    for more details.
    """
    instruments = attr.ib(validator=validate_instruments,
                          convert=convert_ensemble)
    source = attr.ib(validator=attr.validators.instance_of(str))
    style = attr.ib(validator=_validate_style)
    composer = attr.ib(init=False, validator=_validate_composer)
    maintainer = attr.ib(default=None)
    maintainerEmail = attr.ib(default=None)
    maintainerWeb = attr.ib(default=None)
    mutopiatitle = attr.ib(default=None)
    mutopiapoet = attr.ib(default=None)
    mutopiaopus = attr.ib(default=None)
    date = attr.ib(default=None)
    moreinfo = attr.ib(default=None)
