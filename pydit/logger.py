""" setup the logging features """
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


def setup_logging(
    logfile="./audit.log", level_screen=logging.DEBUG, level_file=logging.DEBUG
):
    """ Configure the logging both to screen and a file with sensible optional
    parameters:
    logfile= audit.log with rotation ever 50k and 5 backups
    level_screen= one of the logging.DEBUG, logging.ERROR values
    level_file= same
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

def setup_logging_info():
    return setup_logging(logfile="./audit.log", level_screen=logging.INFO, level_file=logging.INFO)
    