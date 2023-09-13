from typing import Optional

from logging import Formatter, Logger, StreamHandler, getLogger


def get_logger(level: str, prefix: Optional[str] = None) -> Logger:
    """Sets up logger object with console handler."""
    logger = getLogger()
    logger.setLevel(level)
    handler = StreamHandler()
    if prefix is not None:
        formatter = Formatter(f"[{prefix}] %(message)s")
        handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
