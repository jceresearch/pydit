""" Counts occurences of a key in the other dataframe, similar to Excel's COUNTIF()"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def add_counts_between_related_df(
    df1, df2, left_on="", right_on="", on="", inplace=False
):
    """
    Adds column in each df counting occurences of each key in the other dataframe

    This works similar to adding countif() in Excel to sense check if an
    identifier in one sheet is fullly in another (presumably master), or
    if there are duplicated keys,  orphans/gaps, etc.

    This routine does both ways to quickly check whether the relationship is
    one to one, many to many etc.

    Parameters
    ----------
    df1 : DataFrame
        A pandas Dataframe object
    df2 : DataFrame
        A pandas Dataframe object to compare against
    left_on : str, optional
        column to use as key for df1, by default ""
    right_on : str, optional
        column to use as key for df2, by default ""
    on : str, optional
        column to use as key for df1 and df2 if they are the same, by default ""
    inplace : bool, optional
        If True the original dataframes will be mutated, by default False

    Returns
    -------
    DataFrame

        If inplace=False, it returns a tuple of the two dataframes with a new
        column with the count of records found. In df1 it will be "count_[key2]"
        and in df2 it will be "count_[key1]"

        If inplace=True it will return True, and mutate the original dataframes.

    See Also
    --------
    cross_check_key(): There is another function that checks referential
    integrity and does this in a more conceptual way, but often you just want
    to add some counting numbers and filter for >1 or zeroes.

    Examples
    --------

    TODO: Add example


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
