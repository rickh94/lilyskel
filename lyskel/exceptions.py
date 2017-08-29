"""Custom exceptions for lyskel."""


class InstrumentNotFoundError(KeyError):
    """Raised when the instrument is not found in the database."""
    pass
