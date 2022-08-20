""" pytest module for count_cumulative_unique function"""
import os
import sys
import pandas as pd
import pytest


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import count_cumulative_unique


@pytest.fixture(name="df")
def fixture_dataframe():
    data = {
        "a": [1, 2, 3] * 3,
        "Bell__Chart": [1.234_523_45, 2.456_234, 3.234_612_5] * 3,
        "decorated-elephant": [1, 2, 3] * 3,
        "animals@#$%^": ["rabbit", "leopard", "lion"] * 3,
        "cities": ["Cambridge", "Shanghai", "Basel"] * 3,
    }
    df = pd.DataFrame(data)
    return df


def test_count_cumulative_unique_1(df):
    """test case sensitive"""
    df["ccu"] = ["a", "b", "c", "A", "B", "C", "a", "b", "c"]
    df = count_cumulative_unique(
        df, "ccu", dest_column_name="ccu_count", case_sensitive=True
    )
    # column ccu_count should contain [1,2,3,4,5,6,6,6,6]
    assert all(df["ccu_count"] == [1, 2, 3, 4, 5, 6, 6, 6, 6])


def test_count_cumulative_unique_2(df):
    """Test not case sensitive"""
    df["ccu"] = ["a", "b", "c", "A", "B", "C", "a", "b", "c"]
    df = count_cumulative_unique(
        df, "ccu", dest_column_name="ccu_count", case_sensitive=False
    )
    # column ccu_count should contain [1,2,3,3,3,3,3,3,3]
    assert all(df["ccu_count"] == [1, 2, 3, 3, 3, 3, 3, 3, 3])
