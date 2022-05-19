""" Add a count column that will bring the count of that key in the referenced table"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def add_counts_between_related_df(df1, df2, left_on="", right_on="", on=""):
    """Add a count column to bring the count of that key in those tables

    This works similar to adding countif() in Excel to sense check if an 
    identifier in one sheet is in fullly in another (presumably master), or
    if there are duplicated keys or orphans/gaps. 
    This routine does both ways so you can quickly check whether you have 
    one to one, many to many etc, and where there may be the anomales.
    There is another function that checks referential integrity and does this
    in a more conceptual way, but often you just need to add some counting 
    numbers and filter for >1 or zeroes.

    Args:
        df1 (DataFrame): Primary pandas dataFrame
        df2 (DataFrame): Secondary/Referenced pandas DataFrame
        left_on (str, optional): column to use as key for df1. Defaults to None.
        right_on (str, optional): column to use as key for df2. Defaults to None.
        on (str, optional): Name of the column to use as key for df1 and df2 if they are the same.

    Returns:
        True: if sucessful
        The calling DataFrames will be mutated:
        - a new column will be created with the count of records found.
        - In df1 it will be "count_[key2]" and in df2 it will be "count_[key1]"

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
        "Sum total in df2 on %s is %s", "count_fk_" + left_on, sum(df2["count_fk_" + left_on])
    )

    return True
