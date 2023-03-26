"""
Test module for keyword_search
"""

import os
import sys

import numpy as np
import pandas as pd
import pytest

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import keyword_search


@pytest.fixture(name="df")
def fixture_df():
    """Base DataFrame fixture"""
    # fmt: off
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
        "col7": ["South", "North", "South-East", "South-West", "West", "North"],
    }
    # fmt: on
    df = pd.DataFrame(data)
    return df


def test_keyword_search_hits_only(df):
    """test that it behaves correctly when hits_ is True"""
    res = keyword_search(
        df, ["feb", "mar"], columns=["col1", "col2", "col3"], return_data="full_hits"
    )

    assert list(res["kw_match01"]) == [True, True, False, True]
    assert list(res["kw_match_all"]) == [True, True, True, True]

    assert list(res["col1"]) == ["february", "march", "april", "june"]
    assert list(res["col6"]) == [
        2,
        3,
        4,
        6,
    ]  # col6 is not a hit column but full_hits asks to bring it along


def test_keyword_search_re_with_string(df):
    """test that it behaves correctly when strings are given"""

    res = keyword_search(df, ["feb", "mar"], columns=["col1", "col2", "col3"])
    assert list(res["kw_match01"]) == [False, True, True, False, False, True]
    assert list(res["kw_match02"]) == [False, False, True, True, False, False]
    assert list(res["kw_match_all"]) == [False, True, True, True, False, True]

    res = keyword_search(df, ["hello"], columns="col4")
    assert list(res["kw_match01"]) == [True, True, True, True, True, True]
    assert list(res["kw_match_all"]) == [True, True, True, True, True, True]
    res = keyword_search(df, ["1"], columns="col6")
    assert list(res["kw_match01"]) == [True, False, False, False, False, False]


def test_keyword_search_re(df):
    """test that it behaves correctly when given RE"""
    res = keyword_search(df, [r"west$"], columns=["col7"])
    assert list(res["kw_match01"]) == [False, False, False, True, True, False]


def test_keyword_search_str(df):
    """Test for simpler keyword search"""

    res = keyword_search(
        df,
        ["feb", "mar"],
        columns=["col1", "col2", "col3"],
        regexp=False,
    )
    assert list(res["kw_match01"]) == [False, True, True, False, False, True]
    assert list(res["kw_match02"]) == [False, False, True, True, False, False]
    assert list(res["kw_match_all"]) == [False, True, True, True, False, True]

    res = keyword_search(df, ["hello"], columns="col4", regexp=False)
    assert list(res["kw_match01"]) == [True, True, True, True, True, True]
    assert list(res["kw_match_all"]) == [True, True, True, True, True, True]


def test_keyword_search_labels(df):
    """test that it processes labels correctly"""

    res = keyword_search(
        df, [r"west$", "north"], columns=["col7"], labels=["West", "North"]
    )

    assert list(res["West"]) == [False, False, False, True, True, False]
    assert list(res["kw_match_all"]) == [False, True, False, True, True, True]

    res = keyword_search(
        df,
        [r"west$", "north", "south"],
        columns=["col7"],
        labels=["south_west", "north", "south_west"],
    )
    assert list(res["south_west"]) == [True, False, True, True, True, False]


def test_keyword_search_labels_rollup(df):
    """test that it processes labels rollups correctly"""

    res = keyword_search(
        df,
        ["south-east", "south", "north"],
        columns=["col7"],
        labels=["South", "South", "North"],
    )

    assert list(res["South"]) == [True, False, True, True, False, False]


def test_keyword_search_details(df):
    """test that it processes labels correctly"""

    res = keyword_search(
        df,
        [r"west$", "north"],
        columns=["col7"],
        labels=["West", "North"],
        return_data="detail",
        key_column="col1",
    )
    res_list = list(res["col1"])
    assert res_list == ["april", "may", "february", "june"]


if __name__ == "__main__":
    pass
