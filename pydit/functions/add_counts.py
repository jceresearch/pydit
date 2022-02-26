""" Validation functions"""

import logging


logger = logging.getLogger(__name__)


def add_counts(df1, df2, left_on=None, right_on=None, on=None):
    """Add a count column that will bring the count of that key in the
    other table.

    Args:
        df1 (DataFrame): Pandas DataFrame
        df2 (DataFrame): Pandas DataFrame
        left_on (str, optional): Name of the column to use as key for df1. Defaults to None.
        right_on (str, optional): Name of the column to use as key for df2. Defaults to None.
        on (str, optional): Name of the column to use as key for df1 and df2 if they are the same. 
        Defaults to None.
    Either on is needed, or left_on and right_on have to provide a value

    Returns:
        True: if sucessfull
        The calling DataFrames will have a new column
        with the count of records (0 if not found).
        In df1 it will be "count_[key2]" and in df2 it will be "count_[key1]"

    """
    if on:
        left_on = on
        right_on = on
    if (not left_on) or (not right_on):
        print("Missing key")
        return None
    # df1["count"]= df1['mkey'].map(df2.groupby('mkey')['mkey'].count())
    # df2["count"]= df2['mkey'].map(df1.groupby('mkey')['mkey'].count())
    df1["count_" + right_on] = df1["mkey"].map(df2[right_on].value_counts())
    df2["count_" + left_on] = df2["mkey"].map(df1[left_on].value_counts())
    df1["count_" + right_on] = df1["count_" + left_on].fillna(0).astype("Int64")
    df2["count_" + left_on] = df2["count_" + right_on].fillna(0).astype("Int64")
    # TODO: #22 Add_counts_in_each_row: add option for not overwriting the column but creating a new one
    # TODO: #23 Add_counts_in_each_row: add more checks for when not providing a DataFrame or no records

    return True
