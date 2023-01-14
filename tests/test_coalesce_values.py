""" Test module for coalesce_values"""
import os
import sys

import pandas as pd


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import coalesce_values, start_logging_info

# start_logging_info()


def test_coalesce_values():
    """test the coalesce_values function"""
    data = {
        "a": [
            "Label 1",
            "Label 2",
            "Label 2",
            "Label 3",
            "Label 3",
            "Label 3",
            "Label 4",
        ],
        "b": [1, 2, 2, 3, 3, 3, 4],
        "c": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "d": [1, 2, 3, 4, 5, 6, 7],
    }
    df = pd.DataFrame(data)
    result = coalesce_values(df, "a", top_n_values_to_keep=2)
    assert list(result["a_collapsed"]) == [
        "OTHER",
        "LABEL 2",
        "LABEL 2",
        "LABEL 3",
        "LABEL 3",
        "LABEL 3",
        "OTHER",
    ]

    result = coalesce_values(df, "b", top_n_values_to_keep=2)

    assert list(result["b_collapsed"]) == ["OTHER", "2", "2", "3", "3", "3", "OTHER"]
    result = coalesce_values(df, "b", top_n_values_to_keep=2, other_label=0)
    assert list(result["b_collapsed"]) == [0, 2, 2, 3, 3, 3, 0]

    result = coalesce_values(df, "c", top_n_values_to_keep=5)
    assert list(result["c_collapsed"]) == [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "OTHER",
        "OTHER",
    ]
    result = coalesce_values(df, "c", top_n_values_to_keep=100)
    assert list(result["c_collapsed"]) == [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
    ]


if __name__ == "__main__":
    """Run the tests"""
    test_coalesce_values()
