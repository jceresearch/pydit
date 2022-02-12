""" pytest version of tests - WIP"""
import os
import sys
import logging


import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import validate, setup_logging


logger = logging.getLogger()
setup_logging(logger)
logger.info("Started")


def test_check_sequence():
    """ testing the numerical sequence checker"""
    d = {
        "col1": [1, 2, 3, 5, 6],
        "col2": ["Id1", "ID2", "ID3", "ID-4", "ID 5"],
        "col3": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data=d)
    assert validate.check_sequence(df, "col1") == [4]
    assert validate.check_sequence(df, "col2") == []
    assert validate.check_sequence(df, "col3") == []
    assert validate.check_sequence([1, 2, 3, 4, 5]) == []
    assert validate.check_sequence([1, 2, 4, 5]) == [3]
    assert validate.check_sequence([1, 15]) == [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
    ]
    assert validate.check_sequence(pd.Series([1, 2, 3, 5])) == [4]
    assert validate.check_sequence("1 2 3 4 5") == None


def test_check_blanks():
    """ testing the blanks checker"""
    d = {
        "col1": [1, 2, 3, 4, 5],
        "col2": ["Value 1", "Value 2", "", " ", "Value 5"],
        "col3": [np.nan, 2.0, 0.0, 4.0, 5.1],
        "col4": [np.nan, 2, 0, 4, 5],
        "col5": [np.nan, "    ", "  \t", "   \n", "Value 5"],
    }
    df = pd.DataFrame(data=d)
    totals = validate.check_blanks(df, totals_only=True)
    assert totals[0] == 0
    assert totals[1] == 2
    assert totals[2] == 2
    assert totals[3] == 2
    assert totals[4] == 4
    dfx = validate.check_blanks(df)
    d = dfx.to_dict()
    assert d["has_blanks"][0] is True
    assert d["has_blanks"][1] is True
    assert d["has_blanks"][2] is True
    assert d["has_blanks"][3] is True
    assert d["has_blanks"][4] is False
