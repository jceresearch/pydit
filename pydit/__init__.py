""" when importing pydit this script is run and imports the entirety"""

from .functions import *  # noqa: F403, F401
from .utils import *
from .filemanager import FileManager
from .logger import setup_logging

__version__ = "0.01.0"
