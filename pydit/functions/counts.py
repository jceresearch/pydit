"""Add a cumulative count of unique keys, does not mutates the dataframe
"""

from typing import Hashable
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def count_values_in_col(
    df, col, column_name=None, combined=False, percentage=False, inplace=False
):
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
        percentage: bool, optional, default False
            Whether to return percentage over total count
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
                raise ValueError(
                    "column_name, if a list must be the same length as the col list"
                )
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
            # count_summary = df[c].value_counts(dropna=False)
            # count_list = [count_summary[val] for index, val in enumerate(df[c])]
            if flag_auto_name:
                cn = "count_" + c
            else:
                cn = column_name[i]
            # df[cn] = count_list
            df[cn] = df[c].map(df[c].value_counts(dropna=False))
            if percentage:
                count_records = float(df.shape[0])
                df[cn] = df[cn] / count_records

    if inplace:
        return True
    return df


def count_related_key(df1, df2, left_on="", right_on="", on="", inplace=False):
    """Adds column in each df counting occurences of each key in the other dataframe

    This works similar to adding countif() in Excel to sense check if an
    identifier in one sheet is fullly in another (presumably master), or
    if there are duplicated keys,  orphans/gaps, etc.

    This routine does both ways to quickly check whether the relationship is
    one to one, many to many etc.

    Check also cross_check_key() which checks referential integrity and does
    this in a more conceptual way, but often you just want to add some counting
    numbers and filter for >1 or zeroes.

    Parameters
    ----------
    df1 : DataFrame
        A pandas Dataframe object
    df2 : DataFrame
        A pandas Dataframe object to compare against
    left_on : str, optional, default ""
        column to use as key for df1
    right_on : str, optional, default ""
        column to use as key for df2
    on : str, optional, default ""
        column to use as key for df1 and df2 if they are the same"
    inplace : bool, optional, default False
        If True the original dataframes will be mutated

    Returns
    -------
    DataFrame
        If inplace = False, it returns a tuple of the two dataframes with a new
        column with the count of records found. In df1 it will be "count_[key2]"
        and in df2 it will be "count_[key1]".
        If inplace = True it will return True, and mutate the original dataframes.

    """

    if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        pass
    else:
        raise TypeError("df1 and df2 must be pandas DataFrames")

    if left_on == "" and right_on == "" and on == "":
        raise ValueError("You must specify a key to use")

    if left_on != "":
        if left_on not in df1.columns:
            raise ValueError("left_on column not found in df1")
    if right_on != "":
        if right_on not in df2.columns:
            raise ValueError("right_on column not found in df2")
    if on != "":
        if on not in df1.columns:
            raise ValueError("on column not found in df1")
        if on not in df2.columns:
            raise ValueError("on column not found in df2")
        left_on = on
        right_on = on
    else:
        if left_on == "" or right_on == "":
            raise ValueError("You must specify both left_on and right_on key to use")
    if not inplace:
        df1 = df1.copy()
        df2 = df2.copy()

    df1["count_fk_" + right_on] = df1[left_on].map(df2[right_on].value_counts())
    df1["count_" + left_on] = df1[left_on].map(df1[left_on].value_counts())

    df2["count_fk_" + left_on] = df2[right_on].map(df1[left_on].value_counts())
    df2["count_" + right_on] = df2[right_on].map(df2[right_on].value_counts())

    df1["count_fk_" + right_on] = df1["count_fk_" + right_on].fillna(0).astype("Int64")
    df2["count_fk_" + left_on] = df2["count_fk_" + left_on].fillna(0).astype("Int64")
    df1["count_" + left_on] = df1["count_" + left_on].fillna(0).astype("Int64")
    df2["count_" + right_on] = df2["count_" + right_on].fillna(0).astype("Int64")

    mapped_df1 = len(df1[df1["count_fk_" + right_on] > 0])
    mapped_df2 = len(df2[df2["count_fk_" + left_on] > 0])
    logger.info(
        "Mapped %s records in df1 to df2 from a total of %s in df1",
        mapped_df1,
        df1.shape[0],
    )
    logger.info(
        "Mapped %s records in df2 to df1 from a total of %s in df2",
        mapped_df2,
        df2.shape[0],
    )
    logger.info(
        "Sum total in df1 on %s is %s",
        "count_fk_" + right_on,
        sum(df1["count_fk_" + right_on]),
    )
    logger.info(
        "Sum total in df2 on %s is %s",
        "count_fk_" + left_on,
        sum(df2["count_fk_" + left_on]),
    )
    if inplace:
        return True
    else:
        return (df1, df2)


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
