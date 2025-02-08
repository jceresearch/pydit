""" File utilities for saving and loading files



"""

import logging
from datetime import datetime
from pathlib import Path

# pylint: disable=logging-fstring-interpolation
# pylint: disable=logging-not-lazy


logger = logging.getLogger(__name__)

def get_latest_modif_file_from_dir(folder_path, pattern="*"):
    """Returns the latest file from a folder, based on last modified date

    Uses Pathlib to search recursively and to get the last modified date
    using the stat() method


    Parameters
    ----------
    folder_path : str
        The folder path to search
    pattern : str, optional
        The pattern to search for, by default "*"

    Returns
    -------

    latest_file : pathlib.Path
        The latest file found
    latest_file_md : datetime.datetime
        The last modified date of the latest file as a bonus

    """
    list_of_files_recursive = Path(folder_path).rglob(pattern)
    if not list_of_files_recursive:
        raise ValueError(
            "No files found in folder: " + folder_path + " with pattern: " + pattern
        )

    latest_file = list_of_files_recursive[0]
    latest_file_md = 0
    for f in list_of_files_recursive:
        if f.stat().st_mtime > latest_file_md:
            latest_file_md = f.stat().st_mtime
            latest_file = f
    return latest_file, datetime.fromtimestamp(latest_file_md)
