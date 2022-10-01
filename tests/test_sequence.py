""" pytest version of tests - WIP"""
import os
import sys

import pytest
import pandas as pd

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_sequence, setup_logging


logger = setup_logging()


def test_check_sequence():
    """testing the numerical sequence checker"""
    d = {
        "col1": [1, 2, 3, 5, 6],
        "col2": ["Id1", "ID2", "ID3", "ID-4", "ID 5"],
        "col3": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data=d)
    assert check_sequence(df, "col1") == [4]
    assert check_sequence(df, "col2") == []
    assert check_sequence(df, "col3") == []
    assert check_sequence([1, 2, 3, 4, 5]) == []
    assert check_sequence([1, 2, 4, 5]) == [3]
    assert check_sequence([1, 15]) == [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
    ]
    assert check_sequence(pd.Series([1, 2, 3, 5])) == [4]
    with pytest.raises(TypeError):
        check_sequence("1 2 3 4 5")
