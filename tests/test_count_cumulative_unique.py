""" pytest module for count_cumulative_unique function"""
import os
import sys


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import count_cumulative_unique


def test_count_cumulative_unique_1(dataframe):
    """test case sensitive"""
    dataframe["ccu"] = ["a", "b", "c", "A", "B", "C", "a", "b", "c"]
    df = count_cumulative_unique(
        dataframe, "ccu", dest_column_name="ccu_count", case_sensitive=True
    )
    # column ccu_count should contain [1,2,3,4,5,6,6,6,6]
    assert all(df["ccu_count"] == [1, 2, 3, 4, 5, 6, 6, 6, 6])


def test_count_cumulative_unique_2(dataframe):
    """Test not case sensitive"""
    dataframe["ccu"] = ["a", "b", "c", "A", "B", "C", "a", "b", "c"]
    df = count_cumulative_unique(
        dataframe, "ccu", dest_column_name="ccu_count", case_sensitive=False
    )
    # column ccu_count should contain [1,2,3,3,3,3,3,3,3]
    assert all(df["ccu_count"] == [1, 2, 3, 3, 3, 3, 3, 3, 3])
