""" test of base functions"""

import os
import sys
import pathlib

import pandas as pd

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import (
    setup_logging,
    load,
    save,
    _stem_name,
    load_config,
    set_config,
    setup_project,
)


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp


logger = setup_logging()


def test_stem_name():
    """test the internal function to find the stemp of a filename"""
    assert _stem_name("Test.xlsx") == "test"
    assert _stem_name(r"c:\test\test.xlsx") == "test"
    assert _stem_name(r".\Test.xls") == "test"


def test_load():
    """test of basic loading"""
    setup_project("test",project_path="./tests/")
    set_config("input_path", "./tests/test_data/", project_path="./tests/")
    config=load_config(project_path="./tests/")
    print("Input path set to :",config["input_path"] )
    df = load("test_data.xlsx",config=config)
    if df is not None:
        print("Dataframe loaded")
        assert df.shape[0] == 10
    else:
        raise ValueError("Dataframe not loaded")


def test_save():
    """test for saving objects"""
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
    setup_project("test")
    set_config("output_path", "./tests/output/")
    set_config("temp_path", "./tests/temp/")

    assert not save(s2, "test_zero_len.xlsx")
    assert not save(df1, "test_zero_len.xlsx")
    assert not save(t1, "test_zero_len.pickle")
    assert not save(l1, "test_zero_len.pickle")
    assert save(s1, "test_nonzero_len.xlsx")
    assert save(s1, "test_nonzero_len.csv")
    assert not save(d1, "test_zero_len.xlsx")
    assert save(df, "test_non_zero_len_df.xlsx")
    path_saved = save(df, "test_non_zero_len_df.xlsx")
    assert path_saved == "./tests/output/test_non_zero_len_df.xlsx"


def test_save_big():
    """test for saving objects bigger than Excel limit"""
    list_big = list(range(1, 400000))
    d = {
        "col1": list_big,
        "col2": list_big,
    }
    df = pd.DataFrame(data=d)
    # We ensure the output path exists, this needs to be put into a fixture
    path = pathlib.Path("./tests/output/")
    path.mkdir(parents=True, exist_ok=True)
    path = pathlib.Path("./tests/temp/")
    path.mkdir(parents=True, exist_ok=True)

    set_config("output_path", "./tests/output/")
    set_config("temp_path", "./tests/temp/")
    set_config("max_rows_to_excel", 100000)
    assert save(df, "big.xlsx", also_pickle=True)


if __name__ == "__main__":
    # execute only if run as a script
    test_save()
