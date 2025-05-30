"""Test map_values.py"""

import os
import sys

import numpy as np
import pandas as pd
import pytest

# pyright: reportUndefinedVariable=false, reportMissingImports=false,
# pyright: reportOptionalSubscript=false, reportInvalidStringEscapeSequence=false
# pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import map_values, setup_logging

logger = setup_logging()


def test_check_map_values_bad_inputs():
    """testing the blanks checker"""
    d = {
        "col1": [1, 2, 3],
        "col2": [
            "red",
            "amber",
            "green",
        ],
        "col3": [
            "high",
            "medium",
            "low",
        ],
    }

    df = pd.DataFrame(data=d)
    with pytest.raises(TypeError):
        map_values(
            "wrong value",
            input_column="col1",
            mapping="red_amber_green",
            output_column="col4",
        )
    with pytest.raises(ValueError):
        map_values(
            df,
            input_column="col1",
            mapping="red_amber_green_purple_golden",
            output_column="col4",
        )


def test_check_map_values_simple_cases():
    """testing very simple cases"""
    d = {"col1": [1, 2, 3], "col2": ["red", "amber", "green"]}
    df = pd.DataFrame(data=d)
    res = map_values(
        df,
        input_column="col1",
        mapping="to_red_amber_green",
        output_column="col_output",
    )
    assert res["col_output"].tolist() == ["red", "amber", "green"]

    res = map_values(
        df, input_column="col2", mapping="red_amber_green", output_column="col_output"
    )
    assert res["col_output"].tolist() == [1, 2, 3]

    res = map_values(
        df, input_column="col2", mapping="red_amber_green_r", output_column="col_output"
    )
    assert res["col_output"].tolist() == [3, 2, 1]


def test_check_map_values_blanks():
    """testing blanks"""

    d = {"col1": [1, 2, np.nan], "col2": ["red", "amber", "blue"]}
    df = pd.DataFrame(data=d)
    res = map_values(
        df,
        input_column="col1",
        mapping="to_red_amber_green",
        output_column="col_output",
    )
    assert res["col_output"].tolist() == ["red", "amber", np.nan]


def test_check_map_values_advanced_cases():
    """testing with a mix of nas and various oddities"""
    d = {
        "col1": [1, 2, 3, np.nan, 0],
        "col2": ["red", "amber", "green", np.nan, "blue"],
    }
    df = pd.DataFrame(data=d)

    res = map_values(
        df,
        input_column="col1",
        mapping="to_red_amber_green",
        output_column="col_output",
        na_action="ignore",
    )
    assert (
        res["col_output"].equals(pd.Series(["red", "amber", "green", np.nan, np.nan]))
        is True
    )

    res = map_values(
        df,
        input_column="col2",
        mapping="red_amber_green",
        output_column="col_output",
        na_action="ignore",
    )
    assert res["col_output"].equals(pd.Series([1, 2, 3, np.nan, np.nan])) is True
