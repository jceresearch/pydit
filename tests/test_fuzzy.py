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
        ["  New\rLine", "linenew"],
        ["Iñaqui  ", "inaqui"],
        ["Tab\tEntry", "entrytab"],
        ["Lucía", "lucia"],
        ["", ""],
        [np.nan, ""],
        ["Mr. Ryan     O'Neill", "oneillryan"],
        ["Miss Ana-María", "anamaria"],
        ["John Smith 2nd", "2ndjohnsmith"],
        ["Peter\uFF3FDrücker", "druckerpeter"],
        ["Emma\u005FWatson", "emmawatson"],
        ["Jeff Bezos", "bezosjeff"],
        ["  jeff   . Bezos  ", "bezosjeff"],
        ["Amazon Ltd.", "amazon"],
        ["Bezos, Jeff", "bezosjeff"],
        ["Charlie, 2 Delta, 1 Alpha, ", "12alphacharliedelta"],
        ["Emma Emma Hermione", "emmahermione"],
        ["Marks & Spencer", "andmarksspencer"],
    ]
    return pd.DataFrame(data, columns=["input", "expected"])


def test_fuzzy_matching(df):
    """Test that fuzzy matching works"""
    test_df = create_fuzzy_key(df, "input", "fuzzy")
    test_df["test_check"] = test_df["expected"] == test_df["fuzzy"]
    assert len(test_df[test_df["test_check"] == False]) == 0
