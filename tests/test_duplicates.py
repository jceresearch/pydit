""" Testing check_duplicates using pytest """
import os
import sys

import numpy as np
import pandas as pd
import pytest


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_duplicates, start_logging_info

logger = start_logging_info()
"col1": [1, 2, 3, 5, 6],
        "col2": ["Id1", "ID2", "ID3", "ID-4", "ID 5"],
        "col3": [1, 2, 3, 4, 5],
        "col4:": [
            datetime(2023, 1, 1),
            datetime(2023, 1, 2),
            datetime(2023, 1, 3),
            datetime(2023, 1, 10),
            datetime(2023, 1, 11),
        ],
        "col5": [
            date(2023, 1, 1),
            date(2023, 1, 2),
            date(2023, 1, 3),
            date(2023, 1, 10),
            date(2023, 1, 11),
        ],
    """Base DataFrame fixture"""
    data = {
        "col1": [1, 2, 3, 4, 5, 6, 7, 8],
        "col2": [
            "V1",
            "V1",
            "",
            " ",
            "V5",
            "V6",
            "V7",
            "V8",
        ],
        "col4": [1, 1, 1, 4, 4, np.nan, np.nan, 5],
        "col5": [1, 2, 3, 4, 4, 5, 5, 5],
        "col6": [1, 3, 5, 7, 11, 13, 17, 19],
    }

    return pd.DataFrame(data)


def test_check_duplicates_df_invalid(df):
    """test check duplicates"""

    with pytest.raises(ValueError):
        check_duplicates(df, ["col3"])
    with pytest.raises(ValueError):
        check_duplicates(df, "col3")


def test_check_duplicates_dataframe_no_dupes(df):
    """test check duplicates no dupes check"""

    dfdupes = check_duplicates(df, ["col1"])
    assert dfdupes is None

    dfdupes = check_duplicates(df, ["col2"])
    assert len(dfdupes) == 2  # "Value 1" and "Value 1"

    # Same but providing a string as column reference
    dfdupes = check_duplicates(df, "col2")
    assert len(dfdupes) == 2


def test_check_duplicates_dataframe_keep_false(df):
    """test get full population"""

    dfdupes = check_duplicates(
        df,
        ["col1"],
        keep=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert (
        len(dfdupes) == 8
    )  # we should get all the population even if there are no dupes

    dfdupes = check_duplicates(
        df,
        ["col2"],
        keep=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 8  # we should get all the population
    assert sum(dfdupes["_duplicates"]) == 2
    # total number of duplicates as we got a keep=False argument
    # we still get an indicator column , overriding the indicator=False otherwise what is the point
    # note that the col2 has a blank and a space value and gets reported as blanks both, but not
    # as duplicates as we are not stripping them for the duplicate count.
    # TODO: #26 TBC if we want to strip the blanks as an option, before looking for dupes.
    # Getting the entire population of non dupes and only first occurrence of dupes

    dfdupes = check_duplicates(
        df,
        ["col2"],
        keep="first",
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 7

    dfdupes = check_duplicates(
        df,
        ["col2"],
        keep="first",
        dropna=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 7

    assert (
        dfdupes["_duplicates"].sum() == 1
    )  # we get the first record flagged as having duplicates


def test_check_duplicates_dataframe(df):
    """Detailed tests for check_duplicates"""

    dfdupes = check_duplicates(df, ["col2"], keep="first")
    assert len(dfdupes) == 1
    assert (
        dfdupes["col1"].iloc[0] == 2
    )  # the first record is kept it returns the second
    dfdupes = check_duplicates(df, ["col2"], keep=False)
    assert len(dfdupes) == 2

    # Getting just dupes, with the indicator of being a dupe, somewhat useless
    # but tests the passthrough of keep=False
    dfdupes = check_duplicates(
        df,
        ["col2"],
        keep=False,
        add_indicator_column=True,
        also_return_non_duplicates=False,
    )
    assert len(dfdupes) == 2
    assert dfdupes["_duplicates"].sum() == 2

    dfdupes = check_duplicates(
        df,
        ["col4"],
        keep=False,
        dropna=False,
        add_indicator_column=True,
        also_return_non_duplicates=False,
    )
    assert len(dfdupes) == 7

    dfdupes = check_duplicates(
        df,
        ["col4"],
        keep=False,
        dropna=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 8

    dfdupes = check_duplicates(
        df,
        ["col4"],
        keep="first",
        dropna=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 4

    assert (
        dfdupes["_duplicates"].sum() == 3
    )  # we should get the duplicates and the nans as dupes

    dfdupes = check_duplicates(
        df,
        ["col5"],
        keep="first",
        dropna=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 5
    assert dfdupes["col6"].sum() == 29

    dfdupes = check_duplicates(
        df,
        ["col5"],
        keep="last",
        dropna=False,
        add_indicator_column=True,
        also_return_non_duplicates=True,
    )
    assert len(dfdupes) == 5
    assert dfdupes["col6"].sum() == 39


def test_check_duplicates_series():
    """test check duplicates"""
    ser1 = pd.Series(data=[1, 2, 3, 4, 5, 6, 7], name="col1")
    ser2 = pd.Series(
        data=["Value 1", "Value 1", "", " ", "Value 5", "Value 6", "Value 7"],
        name="col2",
    )

    dfdupes = check_duplicates(ser1, ["col1"])
    assert dfdupes is None

    dfdupes = check_duplicates(ser2, ["col2"])
    assert list(dfdupes["data"]) == ["Value 1", "Value 1"]

    dfdupes = check_duplicates(ser2)
    assert list(dfdupes["data"]) == ["Value 1", "Value 1"]


if __name__ == "__main__":
    pass
