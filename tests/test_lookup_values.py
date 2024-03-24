""" Test for Lookup Values """

import os
import sys

import pytest
import pandas as pd
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import lookup_values, setup_logging


logger = setup_logging()


def test_lookup_values():
    """testing the lookup values function"""

    df = pd.DataFrame(
        {
            "a": [
                [1, 2],
                2,
                3,
                np.nan,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                [1, 11],
                [12, 13],
                [1, 2, 3, 22],
            ]
        }
    )
    df_ref = pd.DataFrame(
        {
            "ref": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "val_1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "val_2": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"],
        }
    )

    # Note that if there are duplicates in the master reference file, the first one is taken
    # and there is no warning, you must check for duplicates in the master reference file
    # The other interesting behaviour is when there is nan in a multiple key, only valid results
    # are returned, nan is only returned if there is no valid result at all.
    res = lookup_values(df, "a", df_ref, "ref", "val_1", flatten_list=True, fillna="NA")
    assert res.tolist() == [
        "1, 3",
        "3",
        "4",
        "NA",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "NA",
        "1",
        "NA",
        "1, 3, 4",
    ]
    res = lookup_values(df, "a", df_ref, "ref", "val_1", flatten_list=False, fillna=0)
    assert res.tolist() == [
        [1, 3],
        [3],
        [4],
        [0],
        [6],
        [7],
        [8],
        [9],
        [10],
        [11],
        [0],
        [1],
        [0],
        [1, 3, 4],
    ]
