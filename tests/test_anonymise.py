""" test module for anonymise functions"""
import sys
import os

import pandas as pd
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import anonymise_key


def test_anonymise():
    """ general test that it completes, TBC specifics"""
    d1 = {"mkey": ["a", "b", "c", "d", np.nan], "mvalue": ["aa", "bb", "cc", "dd", ""]}
    d2 = {
        "tkey": [100, 101, 102, 103, 104, 105, 106, 107],
        "mkey": ["a", "a", "a", "b", "c", "c", "e", np.nan],
        "tvalue": [10.12, 20.4, 33.3, 45, 59.99, 60, -1, -1],
    }
    d3 = {
        "tkey": [108, 109, 110, 111, 112, 113, 114, 115],
        "mkey": ["b", "a", "b", "b", "b", "e", "e", "f"],
        "tvalue": [13, 19.04, 10.3, 50, 51.99, 60, 10, 4.20],
    }

    df1 = pd.DataFrame(data=d1)
    df2 = pd.DataFrame(data=d2)
    df3 = pd.DataFrame(data=d3)

    translation = anonymise_key([df1, df2], ["mkey", "mkey"])
    print("Translation:", translation)
    translation2, hash_list = anonymise_key(
        [df3], ["mkey"], translation, create_new_hash_list=True
    )
    print("Translation2:", translation2)
    
    assert "This test is still in development" == False
    
    return True
