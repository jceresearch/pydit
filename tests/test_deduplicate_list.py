""" test of base functions"""

import os
import sys
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import deduplicate_list, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

logger = setup_logging()


def test_deduplicate_list():
    """test the intermal function to cleanup dataframe column names"""
    assert deduplicate_list(["A", "B", "B"]) == ["a", "b", "b_2"]
    assert deduplicate_list([]) == []
    assert deduplicate_list([1, 2, 2]) == ["1", "2", "2_2"]
    assert deduplicate_list(["a", np.NaN, "b", "a", np.NaN, " ", ""]) == [
        "a",
        "column_2",
        "b",
        "a_2",
        "column_5",
        "column_6",
        "column_7",
    ]
    assert deduplicate_list
    ([1, "aloha ", "aloha", 2, 2, 2, 2, 2, 2, 2, 2]) == [
        "1",
        "aloha",
        "aloha_2",
        "2",
        "2_2",
        "2_3",
        "2_4",
        "2_5",
        "2_6",
        "2_7",
        "2_8",
    ]
