""" Test of split transactions """

import os
import sys

from datetime import datetime, date

import pytest
import pandas as pd
import numpy as np


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_for_split_transactions, setup_logging


logger = setup_logging()


def test_split_transactions():
    """test of split transactions"""
    # dataframe with several potential split transactions
    data = {
        "date": [
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 3),
            datetime(2024, 1, 4),
            datetime(2024, 1, 5),
            datetime(2024, 6, 6),
            datetime(2024, 1, 7),
            datetime(2024, 1, 8),
            datetime(2024, 1, 9),
            datetime(2024, 1, 10),
        ],
        "amount": [4999, 2000, 3000, 4000, 5000, 800, 7000, 8000, 9000, 60000],
        "supplier": ["A", "B", "B", "C", "C", "C", "D", "D", "D", "E"],
    }
    thresholds = [5000, 10000, 25000, 50000]
    dfinput = pd.DataFrame(data)
    dfoutput = check_for_split_transactions(
        dfinput,
        limits=thresholds,
        days_horizon=30,
        tolerance_perc=0.01,
        tolerance_abs=1000,
        amount_col="amount",
        categ_col="supplier",
        date_col="date",
    )
    assert list(dfoutput["split_transaction_hit_flag"]) == [
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        1,
        0,
    ]
    print(dfoutput)
