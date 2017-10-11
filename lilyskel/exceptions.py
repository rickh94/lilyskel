"""Custom exceptions for lilyskel."""


class DataNotFoundError(KeyError):
    """Raised when the data is not found in the database."""
    pass


class MissingInstrumentError(KeyError):
    """Raised when one of an ensemble's instruments is not in the database."""
    pass


class MutopiaError(AttributeError):
    """Raised when a desired mutopia value is not in their lists."""
    pass
