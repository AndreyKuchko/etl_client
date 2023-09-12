class CommandNotFound(Exception):
    """Exception for unknown command."""

    pass


class ProcessingError(Exception):
    """Exception during the data processing."""

    pass
