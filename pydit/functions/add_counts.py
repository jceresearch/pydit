""" Validation functions"""

import logging


logger = logging.getLogger(__name__)


def add_counts_between_related_df(df1, df2, left_on="", right_on="", on=""):
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
        True: if sucessful
        The calling DataFrames will have a new column
        with the count of records (0 if not found).
        In df1 it will be "count_[key2]" and in df2 it will be "count_[key1]"

    """
    if on:
        left_on = on
        right_on = on
    if (not left_on) or (not right_on):
        logger.error("Missing key")
        return None

    df1["count_fk_" + right_on] = df1[left_on].map(df2[right_on].value_counts())
    df1["count_" + left_on] = df1[left_on].map(df1[left_on].value_counts())

    df2["count_fk_" + left_on] = df2[right_on].map(df1[left_on].value_counts())
    df2["count_" + right_on] = df2[right_on].map(df2[right_on].value_counts())

    df1["count_fk_" + right_on] = df1["count_fk_" + right_on].fillna(0).astype("Int64")
    df2["count_fk_" + left_on] = df2["count_fk_" + left_on].fillna(0).astype("Int64")
    df1["count_" + left_on] = df1["count_" + left_on].fillna(0).astype("Int64")
    df2["count_" + right_on] = df2["count_" + right_on].fillna(0).astype("Int64")

    # TODO: #22 Add_counts_in_each_row: add option for not overwriting the column but creating a new one
    # TODO: #23 Add_counts_in_each_row: add more checks for when not providing a DataFrame or no records
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
        "Sum total of %s is %s",
        "count_fk_" + right_on,
        sum(df1["count_fk_" + right_on]),
    )
    logger.info(
        "Sum total of %s is %s", "count_fk_" + left_on, sum(df2["count_fk_" + left_on])
    )

    return True
