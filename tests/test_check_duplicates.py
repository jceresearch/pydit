""" pytest version of tests - WIP"""
import os
import sys

import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_duplicates, setup_logging

logger = setup_logging()


def test_check_duplicates():
    """ testing the blanks checker"""
    d = {
        "col1": [1, 2, 3, 4, 5],
        "col2": ["Value 1", "Value 1", "", " ", "Value 5"],
    }
    df = pd.DataFrame(data=d)
    dfdupes = check_duplicates(df, ["col1"])
    assert dfdupes is None
    dfdupes = check_duplicates(df, ["col2"])
    assert len(dfdupes) == 2


if __name__ == "__main__":
    # execute only if run as a script
    test_check_duplicates()
