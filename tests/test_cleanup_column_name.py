""" Pytest suite for transform tools functions"""

import os
import sys
import pytest
import pandas as pd


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import cleanup_column_names, setup_logging


logger = setup_logging()


def test_clean_column_names_1():
    """testing the function for cleaning column names
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
    df = cleanup_column_names(df)
    print(df.columns)
    assert list(df.columns) == ["col1", "col2", "col_3", "col3", "col_3_2"]

    df2 = pd.DataFrame(data=d)
    res = cleanup_column_names(df2)
    assert list(df2.columns) == ["Col1!", "Col2", "col_   3", "col3 ", "col  3"]
    assert list(res.columns) == ["col1", "col2", "col_3", "col3", "col_3_2"]


def test_clean_column_names_2():
    """testing the function for cleaning column names
    Case 2: Special characters
    """
    d = {
        "Col1!:": [1, 2, 3],
        "Col2@": [1, 2, 3],
        "col3%": [1, 2, 3],
        "col4!\n(extra)": [1, 2, 3],
        "col5\n": [1, 2, 3],
        "(col6)": [1, 2, 3],
        "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddz": [1, 2, 3],
        1: [1, 2, 3],
        "maría josé-nuñez": [1, 2, 3],
        "col1$": [1, 2, 3],
    }
    df = pd.DataFrame(data=d)
    df = cleanup_column_names(df)
    print(df.columns)
    assert list(df.columns) == [
        "col1",
        "col2",
        "col3pc",
        "col4_extra",
        "col5",
        "col6",
        "aaaaaaaaaabbbbbbbbbbccccccccccdddddddddd",
        "1",
        "maria_jose_nunez",
        "col1usd",
    ]


def test_clean_column_names_list():
    """testing the function for cleaning column names
    Testing for list of strings instead of a dataframe
    """
    l = [
        "Col1!",
        "Col2@",
        "col3%",
        "col4!\n(extra)",
        "col5\n",
        "(col6)",
        "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddz",
        1,
    ]
    l = cleanup_column_names(l)
    assert l == [
        "col1",
        "col2",
        "col3pc",
        "col4_extra",
        "col5",
        "col6",
        "aaaaaaaaaabbbbbbbbbbccccccccccdddddddddd",
        "1",
    ]
    l = [
        "Col1!",
        "Col2@",
        "col3%",
        "col4!\n(extra)",
        "col5\n",
        "(col6)",
        "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddz",
        1,
    ]
    res = cleanup_column_names(l)

    assert res == [
        "col1",
        "col2",
        "col3pc",
        "col4_extra",
        "col5",
        "col6",
        "aaaaaaaaaabbbbbbbbbbccccccccccdddddddddd",
        "1",
    ]

    l=["col 1"]
    res = cleanup_column_names(l)
    assert res == ["col_1"]


def test_clean_column_names_str():
    """testing the function for cleaning column names
    Testing for string instead of a dataframe
    """
    s = "Col1!"
    s = cleanup_column_names(s)
    assert s == "col1"

    s = "Col  1!"
    res = cleanup_column_names(s)
    assert res == "col_1"


def test_clean_column_names_empty():
    """testing the function for cleaning column names
    Testing for empty input
    """
    s = ""
    s = cleanup_column_names(s)
    assert s == "column_1"

    l = []
    l = cleanup_column_names(l)
    assert l == []

    l= None
    # assert value error
    with pytest.raises(ValueError):
        cleanup_column_names(l)
