""" Test check_blanks.py"""

import os
import sys

import numpy as np
import pandas as pd
import pytest


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_blanks, setup_logging

logger = setup_logging()


def test_check_blanks_bad_inputs():
    """testing the blanks checker"""
    d = {
        "col1": [1, 2, 3, 4, 5],
        "col2": ["Value 1", np.nan, "", " ", "Value 5"],
        "col3": [np.nan, 2.0, 0.0, 4.0, 5.1],
        "col4": [np.nan, 2, 0, 4, 5],
        "col5": [np.nan, "    ", "  \t", "   \n", "Value 5"],
    }
    df = pd.DataFrame(data=d)
    with pytest.raises(ValueError):
        check_blanks(df, columns="Wrong", totals_only=False)
    with pytest.raises(ValueError):
        check_blanks(df, columns=["Wrong", "col1"], totals_only=False)


def test_check_blanks():
    """testing the blanks checker"""
    d = {
        "col1": [1, 2, 3, 4, 5],
        "col2": ["Value 1", np.nan, "", " ", "Value 5"],
        "col3": [np.nan, 2.0, 0.0, 4.0, 5.1],
        "col4": [np.nan, 2, 0, 4, 5],
        "col5": [np.nan, "    ", "  \t", "   \n", "Value 5"],
        "col6": [np.nan, "", 0, " ", 5],
        "col7": [1, 2, 3, 4, "5"],
    }

    df = pd.DataFrame(data=d)
    totals = check_blanks(df, totals_only=True)
    assert totals["col1"] == 0
    assert totals["col2"] == 1
    assert totals["col3"] == 1
    assert totals["col4"] == 1
    assert totals["col5"] == 1
    totals = check_blanks(
        df, include_zeroes=True, include_nullstrings_and_spaces=True, totals_only=True
    )
    assert totals["col1"] == 0
    assert totals["col2"] == 3
    assert totals["col3"] == 2
    assert totals["col4"] == 2
    assert totals["col5"] == 4
    assert totals["col6"] == 4

    dfx = check_blanks(df)
    d = dfx.to_dict()
    print(dfx)
    assert d["has_blanks"][0] is True
    assert d["has_blanks"][1] is True
    assert d["has_blanks"][2] is False
    assert d["has_blanks"][3] is False
    assert d["has_blanks"][4] is False

    dfx = check_blanks(
        df,
        include_zeroes=True,
        include_nullstrings_and_spaces=True,
    )
    d = dfx.to_dict()
    print(d)
    assert d["has_blanks"][0] is True
    assert d["has_blanks"][1] is True
    assert d["has_blanks"][2] is True
    assert d["has_blanks"][3] is True
    assert d["has_blanks"][4] is False


if __name__ == "__main__":
    # execute only if run as a script
    # test_check_blanks()

    d = {
        "col1": [1, 2, 3, 4, 5],
        "col2": ["Value 1", np.nan, "", " ", "Value 5"],
        "col3": [np.nan, 2.0, 0.0, 4.0, 5.1],
        "col4": [np.nan, 2, 0, 4, 5],
        "col5": [np.nan, "    ", "  \t", "   \n", "Value 5"],
    }

    df = pd.DataFrame(data=d)
    from pandas.api.types import is_string_dtype

    print(is_string_dtype(df["col2"]))
