"""Pydit - A toolkit for data wrangling, specifically designed for Internal Auditors

"""

from .functions import *  # noqa: F403, F401
from .statistics import *  # noqa: F403, F401
from .logger import setup_logging
from .logger import start_logging_info
from .logger import start_logging_debug

__version__ = "0.1.10"
