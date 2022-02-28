""" Pytest suite for transform tools functions"""
import os
import sys

import pandas as pd


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import cleanup_column_names, setup_logging


logger = setup_logging()


def test_clean_column_names_1():
    """ testing the function for cleaning column names
    Basic cleanup and handling of duplicate resulting names
    """
    d = {
        "Col1!": [1, 2, 3],
        "Col2": [1, 2, 3],
        "col_   3": [1, 2, 3],
        "col3 ": [1, 2, 3],
        "col  3": [1, 2, 3],
    }
    df = pd.DataFrame(data=d)
    cleanup_column_names(df)
    print(df.columns)
    assert list(df.columns) == ["col1", "col2", "col_3", "col3", "col_3_2"]


def test_clean_column_names_2():
    """ testing the function for cleaning column names
    Case 2: Special characters
    """
    d = {
        "Col1!": [1, 2, 3],
        "Col2@": [1, 2, 3],
        "col3%": [1, 2, 3],
        "col4!": [1, 2, 3],
        "col5\n": [1, 2, 3],
    }
    df = pd.DataFrame(data=d)
    cleanup_column_names(df)
    print(df.columns)
    assert list(df.columns) == ["col1", "col2", "col3pc", "col4", "col5"]

