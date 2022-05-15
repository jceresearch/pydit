""" test fillna smart"""
import os
import sys

import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import fillna_smart, setup_logging


logger = setup_logging()


def test_fillna_smart():
    """ testing the blanks checker"""
    d = {
        "col1": [1, 2, 3, 4, 5],
        "col2": ["Value 1", "Value 2", "", " ", "Value 5"],
        "col3": [np.nan, 2.0, 0.0, 4.0, 5.1],
        "col4": [np.nan, 2, 0, 4, 5],
        "col5": [np.nan, "    ", "  \t", "   \n", "Value 5"],
    }
    df = pd.DataFrame(data=d)
    result = fillna_smart(
        df, text_fillna="EMPTY", include_empty_string=True, include_spaces=True
    )

    assert list(result["col2"]) == ["Value 1", "Value 2", "EMPTY", "EMPTY", "Value 5"]
    assert list(result["col3"]) == [0.0, 2.0, 0.0, 4.0, 5.1]
    assert list(result["col4"]) == [0, 2, 0, 4, 5]
    assert list(result["col5"]) == ["EMPTY", "EMPTY", "EMPTY", "EMPTY", "Value 5"]

    return df


if __name__ == "__main__":
    # execute only if run as a script
    print(test_fillna_smart())
