"""
Shared logging configuration for Image-to-Text API.
Use get_logger(__name__) in each module for INFO-level structured logs.
"""
import logging
import sys

_DATE_FMT = "%Y-%m-%d %H:%M:%S"
_LOG_FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

_configured = False


def configure_logging(level: int = logging.INFO) -> None:
    """Configure app-wide logging. Idempotent."""
    global _configured
    if _configured:
        return
    logging.basicConfig(
        level=level,
        format=_LOG_FMT,
        datefmt=_DATE_FMT,
        stream=sys.stdout,
        force=True,
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a logger for the given module. Ensures logging is configured."""
    configure_logging()
    return logging.getLogger(name)
