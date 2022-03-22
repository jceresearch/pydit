""" Test of the benford checker"""
import os
import sys

import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import benford_to_dataframe, setup_logging

logger = setup_logging()


def test_check_benford():
    """ testing the benford checker"""
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

    dfres = benford_to_dataframe(df, "Wrong_Column", 1)
    assert dfres is None

    dfres = benford_to_dataframe(list(df["test"]), "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    dfres = benford_to_dataframe(tuple(list(df["test"])), "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Testing if we plug a list with some list as an element, does it
    # fail gracefully or ignore (should ignore if we send a list as the
    # to_numeric of the series will coerce errors and we fillna them to 0)
    dfres = benford_to_dataframe(list(df["test"]) + [[1, 2, 3]], "", 1)
    assert list(dfres["bf_act_count"]) == [14, 8, 6, 4, 4, 3, 3, 2, 2]
    assert list(dfres["bf_diff"]) == [0, 0, 0, 0, 0, 0, 0, 0, 0]


if __name__ == "__main__":
    # execute only if run as a script
    test_check_benford()
