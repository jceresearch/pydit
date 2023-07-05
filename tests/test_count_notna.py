""" pytest module for extra count functions
These are convenience functions for when we need to check if a few columns have
values or not, and whether they are the same.

"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydit import count_isna, count_notna, has_different_values


def test_count_isna():
    """test count"""
    df = pd.DataFrame(
        {
            "K": ["K0", "K1", "K2", "K3", "K4"],
            "B": ["A", np.nan, "C", "D1", "E1"],
            "C": ["A", "B", np.nan, "D1", "E2"],
            "D": ["A", "B", np.nan, "D", "E3"],
            "E": ["A", "B", np.nan, "D", ""],
            "F": [1, 2, np.nan, 4, 5],
            "G": [1, np.nan, np.nan, 5, 6],
            "H": [1, 2, np.nan, 6, 6],
        },
        index=[0, 1, 2, 3, 4],
    )

    res = count_isna(df, ["F", "G", "H"])
    exp = [0, 1, 3, 0, 0]
    assert list(res) == exp
    res = count_isna(df, ["B", "C", "D","E"])
    exp = [0, 1, 3, 0, 0]
    assert list(res) == exp

    with pytest.raises(TypeError):
        res = count_isna(df, "H")
        
        
def test_count_notna():
    """test count"""
    df = pd.DataFrame(
        {
            "K": ["K0", "K1", "K2", "K3", "K4"],
            "B": ["A", np.nan, "C", "D1", "E1"],
            "C": ["A", "B", np.nan, "D1", "E2"],
            "D": ["A", "B", np.nan, "D", "E3"],
            "E": ["A", "B", np.nan, "D", ""],
            "F": [1, 2, np.nan, 4, 5],
            "G": [1, np.nan, np.nan, 5, 6],
            "H": [1, 2, np.nan, 6, 6],
        },
        index=[0, 1, 2, 3, 4],
    )

    res = count_notna(df, ["F", "G", "H"])
    exp = [3, 2, 0, 3, 3]
    assert list(res) == exp
    res = count_notna(df, ["B", "C", "D","E"])
    exp = [4, 3, 1, 4, 4]
    assert list(res) == exp

    with pytest.raises(TypeError):
        res = count_notna(df, "H")
    
def test_has_diferent_value():
    """test count"""
    df = pd.DataFrame(
        {
            "K": ["K0", "K1", "K2", "K3", "K4"],
            "B": ["A", np.nan, "C", "D1", "E1"],
            "C": ["A", "B", np.nan, "D1", "E2"],
            "D": ["A", "B", np.nan, "D", "E3"],
            "E": ["A", "B", np.nan, "D", ""],
            "F": [1, 2, np.nan, 4, 5],
            "G": [1, np.nan, np.nan, 5, 6],
            "H": [1, 2, np.nan, 6, 6],
        },
        index=[0, 1, 2, 3, 4],
    )

    res = has_different_values(df, ["F", "G", "H"])
    exp = [3, 2, 0, 3, 3]
    assert list(res) == exp
    res = count_notna(df, ["B", "C", "D","E"])
    exp = [4, 3, 1, 4, 4]
    assert list(res) == exp

    with pytest.raises(TypeError):
        res = count_notna(df, "H")
    