""" test of base functions"""

import os
import sys
import pathlib

import pandas as pd

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import FileManager, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp


logger = setup_logging()
fm = FileManager().getInstance()


def test_stem_name():
    """ test the internal function to find the stemp of a filename"""
    assert fm._stem_name("Test.xlsx") == "test"
    assert fm._stem_name(r"c:\test\test.xlsx") == "test"
    assert fm._stem_name(r".\Test.xls") == "test"


def test_load():
    fm.input_path = "./tests/test_data/"
    df = fm.load("test_data.xlsx")
    assert df.shape[0] == 10


def test_save():
    """ test for saving objects"""
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
    # We ensure the output path exists, this needs to be put into a fixture
    path = pathlib.Path("./tests/output/")
    path.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path("./tests/temp/")
    path.mkdir(parents=True, exist_ok=True)

    fm.output_path = "./tests/output/"
    fm.temp_path = "./tests/temp/"
    assert not fm.save(s2, "test_zero_len.xlsx")
    assert not fm.save(df1, "test_zero_len.xlsx")
    assert not fm.save(t1, "test_zero_len.pickle")
    assert not fm.save(l1, "test_zero_len.pickle")
    assert fm.save(s1, "test_nonzero_len.xlsx")
    assert fm.save(s1, "test_nonzero_len.csv")
    assert not fm.save(d1, "test_zero_len.xlsx")
    assert fm.save(df, "test_non_zero_len_df.xlsx")
    path_saved = fm.save(df, "test_non_zero_len_df.xlsx")
    assert path_saved == "./tests/output/test_non_zero_len_df.xlsx"


if __name__ == "__main__":
    # execute only if run as a script
    test_save()
