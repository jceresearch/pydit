""" Test module for fuzzy.py """

import os
import sys

import numpy as np
import pandas as pd
import pytest

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position

# pyright: reportUndefinedVariable=false, reportMissingImports=false,
# pyright: reportOptionalSubscript=false, reportInvalidStringEscapeSequence=false
# pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import create_fuzzy_key


@pytest.fixture(name="df")
def df_fixture():
    """Base DataFrame fixture"""
    data = [
        ["  New\rLine", "line new"],
        ["Iñaqui  ", "inaqui"],
        ["Tab\tEntry", "entry tab"],
        ["Lucía", "lucia"],
        ["", ""],
        [np.nan, ""],
        ["Mr. Ryan     O'Neill", "oneill ryan"],
        ["Miss Ana-María", "ana maria"],
        ["John Smith 2nd", "2nd john smith"],
        ["Peter\uFF3FDrücker", "drucker peter"],
        ["Emma\u005FWatson", "emma watson"],
        ["Jeff Bezos", "bezos jeff"],
        ["  jeff   . Bezos  ", "bezos jeff"],
        ["Amazon Ltd.", "amazon"],
        ["Bezos, Jeff", "bezos jeff"],
        ["Charlie, 2 Delta, 1 Alpha, ", "1 2 alpha charlie delta"],
        ["Emma Emma Hermione", "emma hermione"],
        ["Marks & Spencer", "and marks spencer"],
    ]
    return pd.DataFrame(data, columns=["input", "expected"])


def test_fuzzy_matching(df):
    """Test that fuzzy matching works"""
    test_df = create_fuzzy_key(df, "input", "fuzzy", token_sort="token_set_sort")
    test_df["test_check"] = test_df["expected"] == test_df["fuzzy"]
    assert len(test_df[test_df["test_check"] == False]) == 0
