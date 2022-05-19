""" Test module for add_percentile.py """
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
def df():
    """Base DataFrame fixture"""
    return pd.DataFrame([78, 38, 42, 48, 31, 89, 94, 102, 122, 122], columns=["INCOME"])


@pytest.fixture
def df2():
    """Fixture with sequential values"""
    return pd.DataFrame([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=["INCOME"])


def test_add_percentile(df):
    """Test ouptut with example from stack overflow."""
    expected = [0.44, 0.11, 0.22, 0.33, 0.0, 0.56, 0.67, 0.78, 1.0, 1.0]
    result = add_percentile(df, "INCOME")
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


if __name__ == "__main__":
    import scipy.stats

    # execute only if run as a script
    # from https://stackoverflow.com/questions/50804120/how-do-i-get-the-percentile-for-a-row-in-a-pandas-dataframe

    temp = pd.DataFrame([78, 38, 42, 48, 31, 89, 94, 102, 122, 122], columns=["INCOME"])
    temp["PCNT_RANK"] = temp["INCOME"].rank(method="max", pct=True)
    temp["POF"] = temp["INCOME"].apply(
        lambda x: scipy.stats.percentileofscore(temp["INCOME"], x, kind="weak")
    )
    temp["QUANTILE_VALUE"] = temp["PCNT_RANK"].apply(
        lambda x: temp["INCOME"].quantile(x, "lower")
    )
    temp["RANK"] = temp["INCOME"].rank(method="max")
    sz = temp["RANK"].size - 1
    temp["PCNT_LIN"] = temp["RANK"].apply(lambda x: (x - 1) / sz)
    temp["CHK"] = temp["PCNT_LIN"].apply(lambda x: temp["INCOME"].quantile(x))
    result = add_percentile(temp, "INCOME")
    print(result.sort_values("INCOME"))
