""" pytest module for count_related function"""
import os
import sys

import pandas as pd
import numpy as np
import pytest

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydit import count_related


def test_count_related():
    """test count related basic functionality"""
    df = pd.DataFrame(
        {
            "class": ["bird", "bird", "bird", "mammal", "mammal"],
            "max_speed": [389, 389, 0, 0, np.nan],
            "country": ["UK", " ", "", "", np.nan],
            "type": ["Falcon", "falcon", "parrot", "Lion", "Monkey"],
        }
    )
    res = count_related(df, "class")
    exp = [3, 3, 3, 2, 2]

    assert list(res["count"]) == exp
    res = count_related(df, "max_speed")
    exp = [2, 2, 2, 2, 1]
    assert list(res["count"]) == exp
    res = count_related(df, "country")
    exp = [1, 1, 2, 2, 1]
    assert list(res["count"]) == exp
    res = count_related(df, "type")
    exp = [1, 1, 1, 1, 1]
    assert list(res["count"]) == exp


if __name__ == "__main__":
    test_count_related()
