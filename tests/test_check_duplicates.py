""" pytest version of tests - WIP"""
import os
import sys

import numpy as np
import pandas as pd
import pytest

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_duplicates, setup_logging

logger = setup_logging()


def test_check_duplicates_dataframe():
    """test check duplicates"""
    d = {
        "col1": [1, 2, 3, 4, 5, 6, 7],
        "col2": ["Value 1", "Value 1", "", " ", "Value 5", "Value 6", "Value 7"],
        "col4": [1, 2, 3, 4, 4, np.nan, np.nan],
    }
    df = pd.DataFrame(data=d)
    print(df)
    dfdupes = check_duplicates(df, ["col1"])
    assert dfdupes is None
    dfdupes = check_duplicates(df, ["col2"])
    assert len(dfdupes) == 2
    with pytest.raises(ValueError):
        check_duplicates(df, ["col3"])

    dfdupes = check_duplicates(df, "col2")
    assert len(dfdupes) == 2
    with pytest.raises(ValueError):
        dfdupes = check_duplicates(df, "col3")

    dfdupes = check_duplicates(df, ["col2"], keep="first")
    assert len(dfdupes) == 1
    assert dfdupes["col1"].iloc[0] == 1  # the first record is kept
    dfdupes = check_duplicates(
        df, ["col2"], keep="first", indicator=True, return_non_duplicates=True
    )
    assert len(dfdupes) == 6
    assert dfdupes["_duplicates_keep"].any() == False
    dfdupes = check_duplicates(
        df, ["col2"], keep=False, indicator=True, return_non_duplicates=False
    )
    assert len(dfdupes) == 2
    assert dfdupes["_duplicates"].all() == True
    dfdupes = check_duplicates(
        df, ["col2"], keep=False, indicator=False, return_non_duplicates=True
    )
    assert len(dfdupes) == 7  # we should get all the population
    assert sum(dfdupes["_duplicates"]) == 2
    # total number of duplicates as we got a keep=False argument
    # we still get an indicator column , overriding the indicator=False otherwise what is the point
    # note that the col2 has a blank and a space value and gets reported as blanks both, but not
    # as duplicates as we are not stripping them for the duplicate count.
    # TODO: #26 TBC if we want to strip the blanks as an option, before looking for dupes.

    dfdupes = check_duplicates(
        df, ["col4"], keep=False, indicator=False, return_non_duplicates=False
    )
    assert len(dfdupes) == 4  # we should get the duplicates and the two nans


def test_check_duplicates_series():
    """test check duplicates"""
    ser1 = pd.Series(data=[1, 2, 3, 4, 5, 6, 7], name="col1")
    ser2 = pd.Series(
        data=["Value 1", "Value 1", "", " ", "Value 5", "Value 6", "Value 7"],
        name="col2",
    )
    ser3 = pd.series(data=[1, 2, 3, 4, 4, np.nan, np.nan], name="col3")
    print(ser1.name)
    dfdupes = check_duplicates(ser1, ["col1"])
    assert dfdupes is None


if __name__ == "__main__":
    # execute only if run as a script
    test_check_duplicates()
