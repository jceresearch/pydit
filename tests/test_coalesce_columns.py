""" Test module for coalesce_columns"""
import os
import sys

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

# pylint: disable=redefined-outer-name
# pylint: disable=import-error
# pylint: disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import coalesce_columns


@pytest.fixture
def df():
    """Base DataFrame fixture"""
    return pd.DataFrame({"a": [1, np.nan, 3], "b": [2, 3, 1], "c": [3, np.nan, 9]})


@pytest.fixture
def df_nans():
    """DataFrame with multiple NaNs"""
    return pd.DataFrame({"s1": [np.nan, np.nan, 6, 9, 9], "s2": [np.nan, 8, 7, 9, 9]})


@pytest.fixture
def df_text():
    """Simple dataframe with text columns"""
    return pd.DataFrame(
        {
            "class": ["bird", "bird", "bird", "mammal", "mammal"],
            "max_speed": [389, 0, 0, 0, np.nan],
            "country": ["UK", " ", "", "", np.nan],
            "type": ["falcon", "falcon", "parrot", "Lion", "Monkey"],
        }
    )


def test_coalesce_with_nans(df, target_column_name="result"):
    """Test output if `default_value` is not provided."""
    result = coalesce_columns(df, "a", "b", "c", target_column_name="result")
    expected = [1, 3, 3]
    assert list(result["result"]) == expected


def test_concat_all_texts(df_text):
    expected = [
        "bird_falcon",
        "bird_falcon",
        "bird_parrot",
        "mammal_Lion",
        "mammal_Monkey",
    ]
    result = coalesce_columns(
        df_text,
        ["class", "type"],
        operation="concatenate",
        target_column_name="result",
        separator="_",
    )
    print(result)
    assert list(result["result"]) == expected


def test_concat_some_empty(df_text):
    expected = [
        "bird 389.0",
        "bird 0.0",
        "bird 0.0",
        "mammal 0.0",
        "mammal ",
        # TODO: #28 find an elegant way of stripping the trailing space in coalesce_columns() using concatenate option
    ]
    result = coalesce_columns(
        df_text,
        ["class", "max_speed"],
        operation="concatenate",
        target_column_name="result",
        separator=" ",
        default_value="",
    )
    print(result)
    assert list(result["result"]) == expected


def test_wrong_column_names(df):
    """Raise Error if wrong columns is provided for `column_names`."""
    with pytest.raises(ValueError):
        coalesce_columns(df, "a", "d")


def test_wrong_type_column_names(df):
    """Raise Error if empty column is provided for `column_names`."""
    with pytest.raises(ValueError):
        coalesce_columns(df, "", target_column_name="new_col")


def test_wrong_type_column_names2(df):
    """Raise Error if none objec is provided for `column_names`."""
    columns = None
    with pytest.raises(ValueError):
        coalesce_columns(df, columns, target_column_name=None)


def test_wrong_type_target_column_name(df):
    """Raise TypeError if wrong type is provided for `target_column_name`."""
    with pytest.raises(TypeError):
        coalesce_columns(df, "a", "b", target_column_name=["new_name"])


def test_wrong_type_default_value(df):
    """Raise TypeError if wrong type is provided for `default_value`."""
    with pytest.raises(TypeError):
        coalesce_columns(
            df, "a", "b", target_column_name="new_name", default_value=[1, 2, 3]
        )


def test_len_column_names_less_than_2(df):
    """Raise Error if column_names length is less than 2."""
    with pytest.raises(ValueError):
        coalesce_columns(df, "a")


def test_empty_column_names(df):
    """Return dataframe if `column_names` is empty."""
    assert_frame_equal(coalesce_columns(df), df)


def test_coalesce_without_target(df):
    """Test output if `target_column_name` is not provided."""
    result = coalesce_columns(df, "a", "b", "c")
    expected_output = df.assign(a=df["a"].combine_first(df["b"].combine_first(df["c"])))
    assert_frame_equal(result, expected_output)


def test_coalesce_without_delete(df_nans):
    """Test ouptut if nulls remain and `default_value` is provided."""
    expected = df_nans.assign(s3=df_nans.s1.combine_first(df_nans.s2).fillna(0))
    result = coalesce_columns(
        df_nans, "s1", "s2", target_column_name="s3", default_value=0
    )
    assert_frame_equal(result, expected)
