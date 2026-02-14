"""Test module for coalesce_values"""

import os
import sys

import pandas as pd
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import coalesce_values


def test_coalesce_values_01():
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
        "e": ["Red", "Red", "Red", "Red", "Red", "Red", "Red"],
        "f": ["a", "b", "c", "d", "e", "f", "g"],
        "g": ["a", "a", "a", "b", "b", "c", np.nan],
        "h": [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        "i": [np.nan, np.nan, np.nan, "b", "b", "c", "d"],
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

    result = coalesce_values(df, "e", top_n_values_to_keep=2)
    assert list(result["e_collapsed"]) == [
        "RED",
        "RED",
        "RED",
        "RED",
        "RED",
        "RED",
        "RED",
    ]

    result = coalesce_values(df, "f", top_n_values_to_keep=2, other_label="OTHER")
    assert list(result["f_collapsed"]) == [
        "A",
        "B",
        "OTHER",
        "OTHER",
        "OTHER",
        "OTHER",
        "OTHER",
    ]

    result = coalesce_values(df, "g", top_n_values_to_keep=2, other_label="OTHER")
    assert list(result["g_collapsed"]) == ["A", "A", "A", "B", "B", "OTHER", "OTHER"]




def test_coalesce_values_02():
    """test the coalesce_values function against NAN values"""
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
        "e": ["Red", "Red", "Red", "Red", "Red", "Red", "Red"],
        "f": ["a", "b", "c", "d", "e", "f", "g"],
        "g": ["a", "a", "a", "b", "b", "c", np.nan],
        "h": [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        "i": [np.nan, np.nan, np.nan, "b", "b", "c", "d"],
    }
    df = pd.DataFrame(data)

    result = coalesce_values(df, "h", top_n_values_to_keep=2, show_nan=True)
    assert list(result["h_collapsed"]) == [
        "N/A",
        "N/A",
        "N/A",
        "N/A",
        "N/A",
        "N/A",
        "N/A",
    ] # All values are NaN, so they should all be treated as "N/A" and not coalesced into "OTHER"

    result = coalesce_values(df, "i", top_n_values_to_keep=2, show_nan=False)
    assert list(result["i_collapsed"]) == [
        "OTHER",
        "OTHER",
        "OTHER",
        "B",
        "B",
        "C",
        "OTHER",
    ] 
