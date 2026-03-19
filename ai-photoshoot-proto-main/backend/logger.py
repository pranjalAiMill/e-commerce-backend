# """
# Shared logging configuration for Image-to-Text API.
# Use get_logger(__name__) in each module for INFO-level structured logs.
# """
# import logging
# import sys

# _DATE_FMT = "%Y-%m-%d %H:%M:%S"
# _LOG_FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# _configured = False


# def configure_logging(level: int = logging.INFO) -> None:
#     """Configure app-wide logging. Idempotent."""
#     global _configured
#     if _configured:
#         return
#     logging.basicConfig(
#         level=level,
#         format=_LOG_FMT,
#         datefmt=_DATE_FMT,
#         stream=sys.stdout,
#         force=True,
#     )
#     _configured = True


# def get_logger(name: str) -> logging.Logger:
#     """Return a logger for the given module. Ensures logging is configured."""
#     configure_logging()
#     return logging.getLogger(name)

"""
Shared logging configuration for VTO Backend.
Use get_logger(__name__) in each module for structured logs.
"""
import logging
import sys

_DATE_FMT = "%Y-%m-%d %H:%M:%S"
_LOG_FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure app-wide logging — fully compatible with uvicorn's reloader.
    Works correctly in both the main process and the child worker process.
    """
    # Get the root logger
    root_logger = logging.getLogger()

    # If our custom handler is already attached, do nothing
    for handler in root_logger.handlers:
        if getattr(handler, "_vto_custom", False):
            return

    # Remove ALL existing handlers (clears uvicorn's default handlers too)
    root_logger.handlers.clear()

    # Create our custom stdout handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=_LOG_FMT, datefmt=_DATE_FMT))
    handler._vto_custom = True  # Tag so we can detect it next time

    root_logger.setLevel(level)
    root_logger.addHandler(handler)

    # Silence noisy uvicorn access logs (keeps ERROR+ from uvicorn itself)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger. Ensures logging is configured first."""
    configure_logging()
    return logging.getLogger(name)