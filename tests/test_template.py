import os
import sys

import pandas as pd
import pytest


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# create a fixture dataframe with 3 columns and 10 rows
@pytest.fixture
def df1():
    data = {
        "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "B": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "C": [21, 22, 23, 24, 25, 26, 27, 28, 29, None],
    }
    return pd.DataFrame(data)


# create another df2 fixture
@pytest.fixture
def df2():
    data = {
        "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "B": [11, 12, 13, 14, 15, 16, 17, 18, None, None],
        "C": [21, 22, None, None, None, None, None, None, None, None],
    }
    return pd.DataFrame(data)
