""" pytest version of tests - WIP"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import pydit_core

import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp
import logging

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
)
logging.info("Started")

tools = pydit_core.Tools()


def test_init():
    """ testing the initiatlisation and setup"""
    assert tools.input_path == "."


def test_check_sequence():
    """ testing the numerical sequence checker"""
    d = {
        "col1": [1, 2, 3, 5, 6],
        "col2": ["Id1", "ID2", "ID3", "ID-4", "ID 5"],
        "col3": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data=d)
    assert tools.check_sequence(df, "col1") == [4]
    assert tools.check_sequence(df, "col2") == []
    assert tools.check_sequence(df, "col3") == []
    assert tools.check_sequence([1, 2, 3, 4, 5]) == []
    assert tools.check_sequence([1, 2, 4, 5]) == [3]
    assert tools.check_sequence([1, 15]) == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert tools.check_sequence(pd.Series([1, 2, 3, 5])) == [4]
    assert tools.check_sequence("1 2 3 4 5") == None
