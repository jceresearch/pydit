"""Add a cumulative count of unique keys, does not mutates the dataframe
"""

from typing import Hashable

import pandas as pd


def count_related(df, col, column_name=None, combined=False, inplace=False):
    """Generates a column counting occurrence of values in a given column.

    If several columns provided, it will generate a column for each of them, but
    if combined is True, it will generate a column counting unique
    combinations of values in the columns.


        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to be analyzed
        col : str or list of str
            Name of the column containing values to tally
        column_name : str or list of str, optional, default None
            Name of the columns to be created containing the count of values
            If None, the column name will be "count_[col]".
        combined : bool, optional, default False
            Whether or not compute the counts combining all the columns provided
        inplace : bool, optional, default False
            Whether or not to mutate the original DataFrame


        Returns
        -------
        pd.DataFrame
            New dataframe with a new column containing the count of values
            If inplace is True, the original DataFrame is modified.

    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expecting a dataframe")
    if not column_name:
        column_name = ""
        flag_auto_name = True
    else:
        flag_auto_name = False
    if isinstance(col, str):
        cols_list = [col]
        if isinstance(column_name, str) and str.strip(column_name) != "":
            column_name = [column_name]
        elif isinstance(column_name, list) and len(column_name) > 1:
            raise ValueError("column_name must be same length as col")
        elif not isinstance(column_name, (list, str)):
            raise TypeError("column_name must be a string or list of strings")
        else:
            flag_auto_name = True  # we ignore the column_name
    elif isinstance(col, list):
        cols_list = col
        if isinstance(column_name, list):
            if len(column_name) != len(cols_list):
                raise ValueError("column_name must be the same length as col")
        else:
            flag_auto_name = True  # ignore whatever we put there
    else:
        raise TypeError("Expecting a string or list of strings")
    for c in cols_list:
        if c not in df.columns:
            raise ValueError("Column not found in dataframe")
    if not inplace:
        df = df.copy()

    if combined:
        s1 = df[cols_list].astype("str").T.agg("_".join)
        df["combined_count_source"] = s1
        count_summary = s1.value_counts(dropna=False)
        count_list = [count_summary[val] for index, val in enumerate(s1)]
        if flag_auto_name:
            cn = "count_combined"
        else:
            cn = column_name[0]
        df[cn] = count_list
    else:
        for i, c in enumerate(cols_list):
            count_summary = df[c].value_counts(dropna=False)
            count_list = [count_summary[val] for index, val in enumerate(df[c])]
            if flag_auto_name:
                cn = "count_" + c
            else:
                cn = column_name[i]
            df[cn] = count_list

    if inplace:
        return True
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
