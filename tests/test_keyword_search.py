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
        "col1": ["january", "february", "march", "april", "may", "june"],
        "col2": [" Jan", " Feb", "Mar", "Apr", np.nan, "Feb"],
        "col3": ["dec", "jan", "feb", "mar", 0, "may"],
        "col4": [
            "Hello world",
            "Hello\nworld",
            "Hello world\n",
            "Hello world ",
            " Hello world",
            "Hi, hello world",
        ],
        "col6": [1, 2, 3, 4, 5, 6],
    }
    df = pd.DataFrame(data)
    # assert "test not implemented" == False
    res = keyword_search(df, ["feb", "mar"], columns=["col1", "col2", "col3"])
    print(res)


if __name__ == "__main__":
    test_keyword_search()
