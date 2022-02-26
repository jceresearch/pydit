""" test of base functions"""

import os
import sys

import pandas as pd

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import FileManager, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp


logger = setup_logging()
logger.info("Started")


fm = FileManager().getInstance()


def test_stem_name():
    """ test the internal function to find the stemp of a filename"""
    assert fm._stem_name("Test.xlsx") == "test"
    assert fm._stem_name(r"c:\test\test.xlsx") == "test"
    assert fm._stem_name(r".\Test.xls") == "test"


def test_save():
    """ test for savling objects"""
    d = {
        "col1": [1, 2, 3, 5, 6],
        "col2": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data=d)
    s1 = pd.Series((1, 2, 3, 4))
    s2 = df[df.col1 == 10]["col1"]
    df1 = df[df["col1"] == 10]
    t1 = ""
    l1 = []
    d1 = {}
    assert fm.save(s2, "test_zero_len.xlsx") == False
    assert fm.save(df1, "test_zero_len.xlsx") == False
    assert fm.save(t1, "test_zero_len.pickle") == False
    assert fm.save(l1, "test_zero_len.pickle") == False
    assert fm.save(s1, "test_nonzero_len.xlsx") == True
    assert fm.save(d1, "test_zero_len.xlsx") == False
    assert fm.save(df, "test_zero_len.xlsx") == True
    return


if __name__ == "__main__":
    test_stem_name
    test_save
