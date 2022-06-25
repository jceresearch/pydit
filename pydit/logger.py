""" Module to provide support for logging with typical parameters """
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging(
    logfile="./audit.log", level_screen=logging.INFO, level_file=logging.INFO
):
    """Configure the logging both to screen and a file with sensible parameters

    By default it will generate an audit.log file with daily rotation kept 7 days.
    You can explore changing this to other kind of rotation/retention criteria.
    By default it will log at INFO level. I tried with DEBUG but some libraries
    start to log a lot of garbage (e.g. faker) and I had to settle on INFO.

    Parameters
    ----------
    logfile : str, optional, default "./audit.log"
        Path to the log file
    level_screen: int, optional, default logging.INFO
        Level of logging to screen
    level_file: int, optional, default logging.INFO
        Level of logging to file

    Returns
    -------
    logger : logging.Logger
        The logger object

    """

    log = logging.getLogger()
    log.handlers.clear()
    log.setLevel(logging.DEBUG)
    # This is size based rotating log
    # fh = RotatingFileHandler(logfile, maxBytes=50000, backupCount=7)
    # This is to keep last week daily log
    fh = TimedRotatingFileHandler(logfile, when="midnight", backupCount=7)

    fh.setLevel(level_file)
    ch = logging.StreamHandler()
    ch.setLevel(level_screen)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s - %(message)s", "%Y-%m-%d %H:%M"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.addHandler(ch)
    return log


def start_logging_info():
    "Wrapper  for setup_logging() to start logging at INFO level, with default parameters"
    logger = setup_logging(
        logfile="./audit.log", level_screen=logging.INFO, level_file=logging.INFO
    )
    logger.info("Logging started at INFO level")
    return logger


def start_logging_debug():
    "Wrapper for setup_logging() to start logging at DEBUG level, with default parameters"
    logger = setup_logging(
        logfile="./audit.log", level_screen=logging.DEBUG, level_file=logging.DEBUG
    )
    logger.info("Logging started at DEBUG level")
    return logger
