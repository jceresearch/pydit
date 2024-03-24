""" pytest version of tests - WIP"""

import os
import sys

from datetime import datetime, date

import pytest
import pandas as pd
import numpy as np


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_sequence, setup_logging


logger = setup_logging()


@pytest.fixture(name="df")
def fixture_df():
    """testing the numerical sequence checker"""
    d = {
        "col1": [1, 2, 3, 5, 6],
        "col2": ["Id1", "ID2", "ID3", "ID-4", "ID 5"],
        "col3": [1, 2, 3, 4, 5],
        "col4": [1, 2, np.nan, 5, 6],
        "col5": ["Id1", "ID2", np.nan, "ID-4", "ID 5"],
        "col6": [1, 2, np.nan, 4, 5],
    }
    return pd.DataFrame(data=d)


@pytest.fixture(name="dfdt")
def fixture_df_datetimes():
    """testing the numerical sequence checker"""
    d = {
        "col1": [
            datetime(2023, 1, 1),
            datetime(2023, 1, 2),
            datetime(2023, 1, 3),
            datetime(2023, 1, 4),
            datetime(2023, 1, 6),
        ],
        "col2": [
            datetime(2023, 1, 1),
            datetime(2023, 1, 2),
            np.nan,
            datetime(2023, 1, 4),
            datetime(2023, 1, 5),
        ],
    }
    return pd.DataFrame(data=d)


@pytest.fixture(name="dfd")
def fixture_df_dates():
    """testing the numerical sequence checker"""
    d = {
        "col1": [
            date(2023, 1, 1),
            date(2023, 1, 2),
            date(2023, 1, 3),
            date(2023, 1, 4),
            date(2023, 1, 6),
        ],
        "col2": [
            date(2023, 1, 1),
            date(2023, 1, 2),
            np.nan,
            date(2023, 1, 4),
            date(2023, 1, 5),
        ],
    }
    return pd.DataFrame(data=d)


def test_check_sequence_basics(df):
    """test sequence basics"""
    assert check_sequence(df, "col1") == [4]
    assert check_sequence(df, "col2") == []
    assert check_sequence(df, "col3") == []
    assert check_sequence(df, "col4") == [3, 4]
    assert check_sequence(df, "col6") == [3]
    assert check_sequence(df, "col5") == [3]
    assert check_sequence([1, 2, 3, 4, 5]) == []
    assert check_sequence([1, 2, 4, 5]) == [3]
    assert check_sequence([1, 15]) == [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
    ]
    assert check_sequence(pd.Series([1, 2, 3, 5])) == [4]
    with pytest.raises(TypeError):
        check_sequence("1 2 3 4 5")


def test_sequence_datetime(dfdt):
    """test sequence datetime"""
    assert check_sequence(dfdt, "col1") == [datetime(2023, 1, 5).date()]
    assert check_sequence(dfdt, "col2") == [datetime(2023, 1, 3).date()]


def test_sequence_dates(dfd):
    """test sequence dates"""
    print("Testing dates")
    assert check_sequence(dfd, "col1") == [date(2023, 1, 5)]
    assert check_sequence(dfd, "col2") == [date(2023, 1, 3)]
