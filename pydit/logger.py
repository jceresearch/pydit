""" Module to provide support for logging with typical parameters """
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Optional, Dict

# ANSI escape codes, picked from library Colorama to avoid dependency

CSI = "\033["
OSC = "\033]"
BEL = "\a"


def code_to_chars(code):
    return CSI + str(code) + "m"


def set_title(title):
    return OSC + "2;" + title + BEL


def clear_screen(mode=2):
    return CSI + str(mode) + "J"


def clear_line(mode=2):
    return CSI + str(mode) + "K"


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + "A"

    def DOWN(self, n=1):
        return CSI + str(n) + "B"

    def FORWARD(self, n=1):
        return CSI + str(n) + "C"

    def BACK(self, n=1):
        return CSI + str(n) + "D"

    def POS(self, x=1, y=1):
        return CSI + str(y) + ";" + str(x) + "H"


class AnsiFore(AnsiCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 90
    LIGHTRED_EX = 91
    LIGHTGREEN_EX = 92
    LIGHTYELLOW_EX = 93
    LIGHTBLUE_EX = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX = 96
    LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX = 100
    LIGHTRED_EX = 101
    LIGHTGREEN_EX = 102
    LIGHTYELLOW_EX = 103
    LIGHTBLUE_EX = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX = 106
    LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(
        self, *args, colors: Optional[Dict[str, str]] = None, **kwargs
    ) -> None:
        """Initialize the formatter with specified format strings."""

        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record) -> str:
        """Format the specified record as text."""

        record.color = self.colors.get(record.levelname, "")
        record.reset = Style.RESET_ALL

        return super().format(record)


formatter_screen = ColoredFormatter(
    "{asctime} - {color} {levelname:8} {reset} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    colors={
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW + Back.BLACK,
        "ERROR": Fore.RED + Back.BLACK,
        "CRITICAL": Fore.RED + Back.WHITE + Style.BRIGHT,
    },
)


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
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level_screen)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s - %(message)s", "%Y-%m-%d %H:%M"
    )
    ch.setFormatter(formatter_screen)
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
