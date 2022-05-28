"""
Test module for keyword_search 
"""

import os
import sys

import numpy as np
import pandas as pd

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import keyword_search


def test_keyword_search():
    """Base DataFrame fixture"""
    data = {
        "col1": ["january", "february", "march", "april", "may", ""],
        "col2": ["winter", "Winter", "spring", "spring", np.nan, "summer"],
        "col3": ["London", "Paris", "New York", "Berlin", 0, "Rome"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "hello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
    }
    df = pd.DataFrame(data)
    # assert "test not implemented" == False
    res = keyword_search(df, "hello", columns=["col4"])
    print(res)


if __name__ == "__main__":
    test_keyword_search()
