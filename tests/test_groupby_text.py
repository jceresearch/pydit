"""Test module for groupby_text.py"""

import os
import sys

import numpy as np
import pandas as pd
import pytest

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import groupby_text


@pytest.fixture(name="df")
def df_fixture():
    """Base DataFrame fixture"""
    data = {
        "team": ["teamA", "teamA", "teamA", "teamA", "teamA", "teamB", "teamC"],
        "purid": ["P01", "P01", "P01", "P02", "P02", "P03", "P03"],
        "apprid": [1, 2, 3, 4, 5, 6, 7],
        "appr": [
            "ok",
            "ok",
            "rejected",
            "ok",
            " ",
            "Error",
            "ok",
        ],
        "user": ["user1", "user2", "user1", "user2", "", np.nan, "user3"],
    }
    return pd.DataFrame(data)


def test_groupby_bad_formed(df):
    """test for badly formed calls"""

    print("Not a dataframe, should raise type error")
    with pytest.raises(TypeError):
        groupby_text(["list_element", "list_element"], "team", "appr")

    print("Null string , value error")
    with pytest.raises(ValueError):
        groupby_text(df, "", "appr")
        # empty key column, value error

    print("Wrong column name, value error")
    with pytest.raises(ValueError):
        groupby_text(df, "wrong_column_name", "appr")

    print("Wrong value column name, value error")
    with pytest.raises(ValueError):
        groupby_text(df, "team", "purid2")


def test_groupby_text_trim(df):
    """Test that trimming works"""
    res = groupby_text(df, ["team", "purid"], value_cols=["apprid", "appr", "user"])
    exp = [
        "1 ok user1\n2 ok user2\n3 rejected user1",
        "4 ok user2\n5",
        "6 Error",
        "7 ok user3",
    ]
    assert list(res["groupby_text"]) == exp


def test_groupby_text(df):
    """Test ouptut with exmples that should work, various aggregation options"""

    res = groupby_text(df, "purid", value_cols=["appr", "user"])
    exp = ["ok user1\nok user2\nrejected user1", "ok user2", "Error\nok user3"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team", "purid"], value_cols=["appr", "user"])
    exp = ["ok user1\nok user2\nrejected user1", "ok user2", "Error", "ok user3"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team"], value_cols=["user"], row_separator=" ")
    exp = ["user1 user2 user1 user2", "", "user3"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["team"], value_cols=["purid", "appr"], row_separator=" ")
    exp = ["P01 ok P01 ok P01 rejected P02 ok P02", "P03 Error", "P03 ok"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, ["purid"], value_cols=["apprid", "appr"], row_separator="|")
    exp = ["1 ok|2 ok|3 rejected", "4 ok|5", "6 Error|7 ok"]
    assert list(res["groupby_text"]) == exp
    res = groupby_text(df, "purid", value_cols="appr", row_separator="|")
    exp = ["ok|ok|rejected", "ok|", "Error|ok"]
    assert list(res["groupby_text"]) == exp


def test_groupby_text_unique_vs_non_unique():
    """Test that unique values are returned when unique=True"""
    d = {
        "col1": [1, 1, 1, 2, 3, 3, 4],
        "col2": ["a", "a", "a", "b", "c", "c", "e"],
        "col3": ["jan", "jan", "feb", "apr", "may", "jun", "jul"],
    }
    df = pd.DataFrame(d)

    res = groupby_text(df, "col2", value_cols=["col3"], row_separator=" ", unique=True)
    list_res = list(res["groupby_text"])
    exp = [
        "feb jan",
        "apr",
        "jun may",
        "jul",
    ]  # testing unique results, note it is sorted alphabetically ascending
    assert list_res == exp

    res = groupby_text(df, "col1", value_cols=["col3"], row_separator=" ", unique=True)
    list_res = list(res["groupby_text"])
    assert list_res == exp
    assert (
        res[res["col1"] == 1]["groupby_text"].values[0] == "feb jan"
    )  # testing the key is integer

    res = groupby_text(df, "col2", value_cols=["col3"], row_separator=" ")
    list_res = list(res["groupby_text"])
    exp = ["jan jan feb", "apr", "may jun", "jul"]
    assert list_res == exp
    res = groupby_text(df, "col1", value_cols=["col3"], row_separator=" ")
    list_res = list(res["groupby_text"])
    assert list_res == exp  # testing the results is the same if key is integer

    assert (
        res[res["col1"] == 1]["groupby_text"].values[0] == "jan jan feb"
    )  # testing the key is integer


if __name__ == "__main__":
    d = {
        "col1": [1, 1, 1, 2, 3, 3, 4],
        "col2": ["a", "a", "a", "b", "c", "c", "e"],
        "col3": ["jan", "jan", "feb", "apr", "may", "jun", "jul"],
    }
    df = pd.DataFrame(d)
    dfg = df.groupby(["col1"])["col3"].apply(set).apply(" ".join).reset_index()
    print(dfg)
