"""Add a cumulative count of unique keys, does not mutates the dataframe
"""

from typing import Hashable

import pandas as pd


def count_related(df, col, column_name="count"):
    """Count the number of values from col

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to be analyzed
    col : str
        Name of the column containing values to tally
    column_name : str, optional, default 'count'
        Name of the column to be created containing the count of values

    Returns
    -------
    pd.DataFrame
        New dataframe with a new column containing the count of values




    """
    df = df.copy()

    def _get_counts(val):
        if pd.isna(val):
            return df[col].isna().sum()
        else:
            return len(df[df[col] == val])

    count_list = [_get_counts(val) for index, val in enumerate(df[col])]

    df[column_name] = count_list
    return df


def count_cumulative_unique(
    df: pd.DataFrame,
    column_name: Hashable,
    dest_column_name: str,
    case_sensitive: bool = True,
    inplace=False,
) -> pd.DataFrame:
    """Generates a running total of cumulative unique values in a given column.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to be analyzed
    column_name : Hashable
        Name of the column containing values from which a running count
        of unique values will be created.
    dest_column_name : str
        Name of the column to be created containing the cumulative count
        of unique values.
    case_sensitive : bool, optional, default True
        Whether or not uppercase and lowercase letters
        will be considered equal (e.g., 'A' != 'a' if `True`).

    Returns
    -------
    pd.DataFrame
        Dataframe with a new column containing the cumulative count of
        unique values in the given column.

    This method does NOT mutate the original DataFrame by default.

    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expecting a dataframe")
    if not inplace:
        df = df.copy()
    if not case_sensitive:
        # Make it so that the the same uppercase and lowercase
        # letter are treated as one unique value
        df[column_name] = df[column_name].astype(str).map(str.lower)

    df[dest_column_name] = (
        (df[[column_name]].drop_duplicates().assign(dummyabcxyz=1).dummyabcxyz.cumsum())
        .reindex(df.index)
        .ffill()
        .astype(int)
    )

    return df
