""" pytest version of tests - WIP"""
import os
import sys

import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_blanks, setup_logging


logger = setup_logging()


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
    totals = check_blanks(df, totals_only=True)
    assert totals[0] == 0
    assert totals[1] == 2
    assert totals[2] == 2
    assert totals[3] == 2
    assert totals[4] == 4
    dfx = check_blanks(df)
    d = dfx.to_dict()
    assert d["has_blanks"][0] is True
    assert d["has_blanks"][1] is True
    assert d["has_blanks"][2] is True
    assert d["has_blanks"][3] is True
    assert d["has_blanks"][4] is False

