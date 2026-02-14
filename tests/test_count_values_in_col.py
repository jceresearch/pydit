"""pytest module for count_values_in_col function"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydit import count_values_in_col


# fixture
@pytest.fixture(name="df")
def df():
    df = pd.DataFrame(
        {
            "class": ["bird", "bird", "bird", "mammal", "mammal", "insect"],
            "max_speed": [389, 389, 0, 0, np.nan, np.nan],
            "country": ["UK", " ", "", "", np.nan, np.nan],
            "type": ["Falcon", "falcon", "parrot", "Lion", "Monkey", "Bee"],
            "type_lower": ["falcon", "falcon", "parrot", "lion", "monkey", "bee"],
        }
    )
    return df


def test_count_values_in_col_invalid(df):
    """test invalid column name"""
    with pytest.raises(ValueError):
        res = count_values_in_col(df, "wrong_col", "count")
    with pytest.raises(ValueError):
        res = count_values_in_col(df, ["wrong_col"], "count")
    with pytest.raises(ValueError):
        res = count_values_in_col(df, ["class", "wrong_col"], "count")
    with pytest.raises(ValueError):
        res = count_values_in_col(df, ["class", "max_speed"], "wrong_count")
    with pytest.raises(ValueError):
        res = count_values_in_col(df, ["class", "max_speed"], column_name="wrong_count")


def test_count_values_in_col(df):
    """test count related basic functionality"""

    res = count_values_in_col(df_input=df, col="class", column_name="count")
    exp = [3, 3, 3, 2, 2, 1]
    assert list(res["count"]) == exp

    res = count_values_in_col(
        df_input=df, col="max_speed", column_name="count_max_speed"
    )
    exp = [2, 2, 2, 2, 2, 2]
    assert list(res["count_max_speed"]) == exp

    res = count_values_in_col(df_input=df, col="country", column_name="count")
    exp = [1, 1, 2, 2, 2, 2]

    assert list(res["count"]) == exp
    res = count_values_in_col(df, "type", "count")

    exp = [1, 1, 1, 1, 1, 1]
    assert list(res["count"]) == exp


def test_count_values_in_col_combined(df):
    """test combined count"""

    res = count_values_in_col(df, ["class", "type"], combined=True)
    exp = [1, 1, 1, 1, 1, 1]
    assert list(res["count_combined"]) == exp

    with pytest.raises(ValueError):
        res = count_values_in_col(
            df, ["class", "type"], column_name="dummy", combined=True
        )

    res = count_values_in_col(df, ["class", "type_lower"], combined=True)
    exp = [2, 2, 1, 1, 1, 1]
    assert list(res["count_combined"]) == exp

    res = count_values_in_col(df, ["max_speed", "country"], combined=True)
    exp = [1, 1, 2, 2, 2, 2]
    assert list(res["count_combined"]) == exp


def test_count_values_in_col_perc(df):
    """test count returning percentages"""

    res = count_values_in_col(df, "class", "count", percentage=True)
    exp = [0.5, 0.5, 0.5, 0.3333333333333, 0.3333333333333, 0.1666666666666]
    np.testing.assert_almost_equal(list(res["count"]), exp, decimal=5)

    res = count_values_in_col(df, "max_speed", "count", percentage=True)
    exp = [
        0.33333333,
        0.33333333,
        0.33333333,
        0.33333333,
        0.33333333,
        0.33333333,
    ]
    np.testing.assert_almost_equal(list(res["count"]), exp, decimal=4)


if __name__ == "__main__":
    # test_count_values_in_col_combined()
    pass
