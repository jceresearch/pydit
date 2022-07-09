"""
Test module for keyword_search
"""

import os
import sys

import numpy as np
import pandas as pd

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import keyword_search


def test_keyword_search_re_with_string():
    "Test that it behaves correctly when just strings are given"
    data = {
        "col1": ["january", "february", "march", "april", "may", "june"],
        "col2": [" Jan", " Feb", "Mar", "Apr", np.nan, "Feb"],
        "col3": ["dec", "jan", "feb", "mar", 0, "may"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "Hi, \nhello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
    }
    df = pd.DataFrame(data)
    res = keyword_search(df, ["feb", "mar"], columns=["col1", "col2", "col3"])
    assert list(res["kw_match01"]) == [False, True, True, False, False, True]
    assert list(res["kw_match02"]) == [False, False, True, True, False, False]
    assert list(res["kw_match_all"]) == [False, True, True, True, False, True]
    res = keyword_search(df, ["hello"], columns="col4")
    assert list(res["kw_match01"]) == [True, True, True, True, True, True]
    assert list(res["kw_match_all"]) == [True, True, True, True, True, True]
    res = keyword_search(df, ["1"], columns="col6")
    assert list(res["kw_match01"]) == [True, False, False, False, False, False]


def test_keyword_search_re():
    """test that it behaves correctly when given RE"""
    data = {
        "col1": ["january", "february", "march", "april", "may", "june"],
        "col2": [" Jan", " Feb", "Mar", "Apr", np.nan, "Feb"],
        "col3": ["dec", "jan", "feb", "mar", 0, "may"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "Hi, \nhello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
        "col7": ["South", "North", "East-West", "West-South", "West", "North"],
    }
    df = pd.DataFrame(data)
    res = keyword_search(df, [r"west$"], columns=["col7"])
    assert list(res["kw_match01"]) == [False, False, True, False, True, False]


def test_keyword_search_str():
    """Test for simpler keyword search"""

    """Base DataFrame fixture"""
    data = {
        "col1": ["january", "february", "march", "april", "may", "june"],
        "col2": [" Jan", " Feb", "Mar", "Apr", np.nan, "Feb"],
        "col3": ["dec", "jan", "feb", "mar", 0, "may"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "Hi, \nhello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
    }
    df = pd.DataFrame(data)
    res = keyword_search(
        df, ["feb", "mar"], columns=["col1", "col2", "col3"], regexp=False
    )
    assert list(res["kw_match01"]) == [False, True, True, False, False, True]
    assert list(res["kw_match02"]) == [False, False, True, True, False, False]
    assert list(res["kw_match_all"]) == [False, True, True, True, False, True]
    res = keyword_search(df, ["hello"], columns="col4", regexp=False)
    assert list(res["kw_match01"]) == [True, True, True, True, True, True]
    assert list(res["kw_match_all"]) == [True, True, True, True, True, True]


def test_keyword_search_labels():
    """test that it processes labels correctly"""
    data = {
        "col1": ["january", "february", "march", "april", "may", "june"],
        "col2": [" Jan", " Feb", "Mar", "Apr", np.nan, "Feb"],
        "col3": ["dec", "jan", "feb", "mar", 0, "may"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "Hi, \nhello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
        "col7": ["South", "North", "East-West", "West-South", "West", "North"],
    }
    df = pd.DataFrame(data)
    res = keyword_search(
        df, [r"west$", "north"], columns=["col7"], labels=["West", "North"]
    )

    assert list(res["West"]) == [False, False, True, False, True, False]
    assert list(res["kw_match_all"]) == [False, True, True, False, True, True]

    res = keyword_search(
        df,
        [r"west$", "north", "south"],
        columns=["col7"],
        labels=["south_west", "north", "south_west"],
    )
    assert list(res["south_west"]) == [True, False, True, True, True, False]


def test_keyword_search_details():
    """test that it processes labels correctly"""
    data = {
        "col1": ["january", "february", "march", "april", "may", "june"],
        "col2": [" Jan", " Feb", "Mar", "Apr", np.nan, "Feb"],
        "col3": ["dec", "jan", "feb", "mar", 0, "may"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "Hi, \nhello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
        "col7": ["South", "North", "East-West", "West-South", "West", "North"],
    }
    df = pd.DataFrame(data)
    res = keyword_search(
        df,
        [r"west$", "north"],
        columns=["col7"],
        labels=["West", "North"],
        return_data="details",
        key_column="col1",
    )
    res_list = list(res["col1"])
    assert res_list == ["march", "may", "february", "june"]


if __name__ == "__main__":
    test_keyword_search_details()
