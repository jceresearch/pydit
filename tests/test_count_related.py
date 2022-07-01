""" pytest module for count_related function"""
from math import comb
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
            "class": ["bird", "bird", "bird", "mammal", "mammal", "insect"],
            "max_speed": [389, 389, 0, 0, np.nan, np.nan],
            "country": ["UK", " ", "", "", np.nan, np.nan],
            "type": ["Falcon", "falcon", "parrot", "Lion", "Monkey", "Bee"],
            "type_lower": ["falcon", "falcon", "parrot", "lion", "monkey", "bee"],
        }
    )
    res = count_related(df, "class", "count")
    exp = [3, 3, 3, 2, 2, 1]
    assert list(res["count"]) == exp
    res = count_related(df, "max_speed", "count_max_speed")
    exp = [2, 2, 2, 2, 2, 2]
    assert list(res["count_max_speed"]) == exp
    res = count_related(df, "country", "count")
    exp = [1, 1, 2, 2, 2, 2]
    assert list(res["count"]) == exp
    res = count_related(df, "type", "count")
    exp = [1, 1, 1, 1, 1, 1]
    assert list(res["count"]) == exp


def test_count_related_combined():
    """test combined count"""
    df = pd.DataFrame(
        {
            "class": ["bird", "bird", "bird", "mammal", "mammal", "insect"],
            "max_speed": [389, 389, 0, 0, np.nan, np.nan],
            "country": ["UK", " ", "", "", np.nan, np.nan],
            "type": ["Falcon", "falcon", "parrot", "Lion", "Monkey", "Bee"],
            "type_lower": ["falcon", "falcon", "parrot", "lion", "monkey", "bee"],
        }
    )
    res = count_related(df, ["class", "type"], "count", combined=True)
    exp = [1, 1, 1, 1, 1, 1]
    assert list(res["count_combined"]) == exp

    res = count_related(df, ["class", "type_lower"], combined=True)
    exp = [2, 2, 1, 1, 1, 1]
    assert list(res["count_combined"]) == exp

    res = count_related(df, ["max_speed", "country"], combined=True)
    exp = [1, 1, 2, 2, 2, 2]
    assert list(res["count_combined"]) == exp


if __name__ == "__main__":
    # test_count_related_combined()
    pass
