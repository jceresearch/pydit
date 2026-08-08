"""Pydit - A toolkit for data wrangling, specifically designed for Internal Auditors"""

from .logger import setup_logging, start_logging_debug, start_logging_info
from .statistics import *
from .wrangling import *

__version__ = "0.2.00"

__all__ = ["setup_logging", "start_logging_debug", "start_logging_info"]
