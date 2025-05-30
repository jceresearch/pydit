"""Test module for add_percentile.py"""

import os
import sys

import pandas as pd
import pytest

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import add_percentile


@pytest.fixture
def df1():
    """Base DataFrame fixture"""
    df = pd.DataFrame([78, 38, 42, 48, 31, 89, 94, 102, 122, 122], columns=["INCOME"])
    df["dataset"] = "df1"
    return df


@pytest.fixture
def df2():
    """Fixture with sequential values"""
    df = pd.DataFrame([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["INCOME"])
    df["dataset"] = "df2"
    return df


def test_add_percentile(df1):
    """Test ouptut with example from stack overflow."""
    expected = [0.44, 0.11, 0.22, 0.33, 0.0, 0.56, 0.67, 0.78, 1.0, 1.0]
    result = add_percentile(df1, "INCOME")
    perc = [round(x, 2) for x in list(result["percentile_in_INCOME"])]
    print(perc)
    assert perc == expected


def test_add_percentile2(df2):
    """Test ouptut with a simple 1 to 10 sequence."""
    expected = [0.0, 0.11, 0.22, 0.33, 0.44, 0.56, 0.67, 0.78, 0.89, 1.0]
    result = add_percentile(df2, "INCOME")
    perc = [round(x, 2) for x in list(result["percentile_in_INCOME"])]
    print(perc)
    assert perc == expected


def test_add_percentile_categories():
    """Testing add_percentiles within categories provided as separate columns"""
    col1 = range(1, 100)
    col2 = [1] * 30 + [2] * 50 + [3] * 20
    col3 = [1] * 10 + [2] * 90
    df = pd.DataFrame(zip(col1, col2, col3), columns=["col1", "col2", "col3"])
    res = add_percentile(df, "col1", ["col2", "col3"])
    print("test_add_percentile_categories: ")
    print(res)
    res_list = list(res["percentile_in_col2_col3"])
    assert res_list[4] == 50.0
    assert res_list[98] == 100.0
