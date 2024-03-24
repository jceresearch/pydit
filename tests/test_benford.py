""" Test of the benford checker"""

import os
import sys
import pathlib
import pytest
import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import (
    benford_to_dataframe,
    setup_logging,
    benford_to_plot,
    benford_list_anomalies,
    benford_probability,
    benford_mad,
)

# create the output folder for the png if it does not exist
pathlib.Path("./tests/output").mkdir(parents=True, exist_ok=True)

logger = setup_logging()


def test_benford_mad():
    """testing the benford mad"""
    #
    # The MAD is the Mean Absolute Deviation from the expected Benford distribution
    # create a random sample of 10000 numbers
    data = [
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        3,
        3,
        4,
        4,
        5,
        6,
        7,
        8,
        9,
    ]  # they follow Benford distribution
    df = benford_to_dataframe(data)
    mad = benford_mad(data)
    assert mad == pytest.approx(0.0, rel=1e-2)


def test_benford_distribution():
    """testing the benford distribution"""
    # approximate test float:
    assert benford_probability(1) == pytest.approx(0.301, rel=1e-2)
    assert benford_probability(99) == pytest.approx(0.00436, rel=1e-2)
    assert benford_probability(-99) == pytest.approx(0.00436, rel=1e-2)
    assert benford_probability("1") == pytest.approx(0.301, rel=1e-2)
    assert benford_probability("33") == pytest.approx(0.01296, rel=1e-2)
    # test zero should yield value error
    with pytest.raises(ValueError):
        benford_probability(0)


def test_check_benford_wrong_inputs():
    """testing the benford checker"""
    # fmt: off
    d = [np.nan," ", " ",
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        -1,
        11,
        1.11,
        0.1111,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        7,
        7,
        7,
        8,
        8,
        9,
        9,
    ]
    # fmt: on
    df = pd.DataFrame(d, columns=["test"])
    # This list should match exactly the expected count, i.e. 14,8,6,4,4,3,3,2,2
    with pytest.raises(ValueError):
        benford_to_dataframe(df, "Wrong_Column", 1)


def test_check_benford():
    """testing the benford checker"""
    d = [
        np.nan,
        " ",
        " ",
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        -1,
        11,
        1.11,
        0.1111,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        7,
        7,
        7,
        8,
        8,
        9,
        9,
    ]
    df = pd.DataFrame(d, columns=["test"])
    # This list should match exactly the expected count, i.e. 14,8,6,4,4,3,3,2,2
    dfres = benford_to_dataframe(df, "test", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    dfres = benford_to_dataframe(df["test"], first_n_digits=1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_abs_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    dfres = benford_to_dataframe(list(df["test"]), "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_abs_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    dfres = benford_to_dataframe(tuple(list(df["test"])), "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_abs_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Testing if we plug a list with some list as an element it would
    # still work by flattening the list into string so it would be an
    # extra 1
    dfres = benford_to_dataframe(list(df["test"]) + [[1, 2, 3], 1, 2, 3], "", 1)
    assert list(dfres["bf_act_count"]) == [16, 9, 7, 4, 4, 3, 3, 2, 2]
    print(list(dfres["bf_act_count"]))
    print(list(dfres["bf_abs_diff"]))
    assert list(dfres["bf_abs_diff"]) == [1, 0, 1, 1, 0, 0, 0, 1, 0]


def test_check_benford_2():
    d = ["1", "  2", "003", "0.4", -0.5, -6, 7, 800, "9000", " 1000", "  002002"]
    dfres = benford_to_dataframe(d, "", 1)
    assert list(dfres["bf_act_count"]) == [2, 2, 1, 1, 1, 1, 1, 1, 1]


def test_benford_chart():
    """testing the benford chart"""
    d = [
        np.nan,
        " ",
        " ",
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        -1,
        11,
        1.11,
        0.1111,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        7,
        7,
        7,
        8,
        8,
        9,
        9,
    ]
    df = pd.DataFrame(d, columns=["test"])

    res = benford_to_plot(
        df, "test", 1, show=False, filename="./tests/output/benford.png"
    )
    assert res.shape == (9, 10)


def test_benford_list_anomalies():
    """testing the benford list anomalies"""
    d = [
        np.nan,
        " ",
        " ",
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        -1,
        11,
        1.11,
        0.1111,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        7,
        7,
        7,
        8,
        8,
        9,
        9,
    ]
    df = pd.DataFrame(d, columns=["test"])

    res = benford_list_anomalies(df, "test", 1)

    assert res[res["bf_exp_count"] > 0]["bf_diff_perc"].abs().sum() == 0


if __name__ == "__main__":
    # execute only if run as a script
    pass
