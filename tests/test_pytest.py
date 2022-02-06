""" pytest version of tests - WIP"""
import os
import sys
import logging


import numpy as np
import pandas as pd
from pandas import Timestamp

# import numpy as np
# from datetime import datetime, date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import file_tools


logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
)
logging.info("Started")

tools = file_tools.FileTools()


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
    totals = tools.check_blanks(df, totals_only=True)
    assert totals[0] == 0
    assert totals[1] == 2
    assert totals[2] == 2
    assert totals[3] == 2
    assert totals[4] == 4
    dfx = tools.check_blanks(df)
    d = dfx.to_dict()
    assert d["has_blanks"][0] is True
    assert d["has_blanks"][1] is True
    assert d["has_blanks"][2] is True
    assert d["has_blanks"][3] is True
    assert d["has_blanks"][4] is False


def test_profile_dataframe():
    """test the function for checking/profiling a dataframe"""
    # test that passing one column will fail gracefully
    df = pd.DataFrame(
        [
            [1, "INV-220001", Timestamp("2022-01-01 00:00:00"), "OPEN", 35.94, ""],
            [2, "INV-220002", Timestamp("2022-01-02 00:00:00"), "OPEN", 99.99, "-5",],
            [
                3,
                "INV-220003",
                Timestamp("2022-01-03 00:00:00"),
                "CANCELLED",
                13.0,
                "reinburse 10.5",
            ],
            [
                4,
                "INV-220003",
                Timestamp("2022-01-04 00:00:00"),
                "OPEN",
                float("nan"),
                "",
            ],
            [5, "INV-220005", Timestamp("2022-01-04 00:00:00"), "OPEN", 204.2, ""],
            [
                6,
                "INV-220006",
                Timestamp("2022-01-15 00:00:00"),
                "OPEN",
                -4.2,
                "discount",
            ],
            [7, float("nan"), Timestamp("2022-01-06 00:00:00"), float("nan"), 0.0, "",],
            [8, "INV-220007", Timestamp("2022-01-15 00:00:00"), "PENDING", 50.4, "",],
            [9, "", pd.NaT, "ERROR", 0.0, ""],
            [10, "INV-220007", Timestamp("2022-01-15 00:00:00"), "PENDING", 50.4, "",],
        ],
        columns=["id", "ref", "date_trans", "status", "amount", "notes"],
    )
    assert tools.profile_dataframe(df["id"]) is None

