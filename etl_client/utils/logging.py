from logging import Logger, StreamHandler, getLogger


def get_logger(level: str) -> Logger:
    """Sets up logger object with console handler."""
    logger = getLogger()
    logger.setLevel(level)
    logger.addHandler(StreamHandler())
    return logger
