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
)

# create the output folder for the png if it does not exist
pathlib.Path("./tests/output").mkdir(parents=True, exist_ok=True)

logger = setup_logging()


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
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    dfres = benford_to_dataframe(list(df["test"]), "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    dfres = benford_to_dataframe(tuple(list(df["test"])), "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Testing if we plug a list with some list as an element it would
    # still work by flattening the list into string so it would be an
    # extra 1
    dfres = benford_to_dataframe(list(df["test"]) + [[1, 2, 3],1,2,3], "", 1)
    assert list(dfres["bf_act_count"]) == [16, 9, 7, 4, 4, 3, 3, 2, 2]
    print(list(dfres["bf_act_count"]))
    print(list(dfres["bf_diff"]))
    assert list(dfres["bf_diff"]) == [1, 0, 1, 1, 0, 0, 0, 1, 0]

def test_check_benford_2():
    d=["1","  2","003","0.4",-0.5,-6,7,800,"9000"," 1000","  002002"]
    dfres=benford_to_dataframe(d, "", 1)
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
    assert res.shape == (9, 7)


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

    assert res[res["bf_exp_count"] > 0]["bf_diffperc"].sum() == 0


if __name__ == "__main__":
    # execute only if run as a script
    test_benford_chart()
    pass
