"""Adds a percentile column to a DataFrame, optionally based on a column """

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def add_percentile(df, col, col_group=None, inplace=False):
    """
    Adds columns for percentile for a chosen column in a DataFrame

    It can also provide it within a category group (col_group)

    Parameters
    ----------
    df : DataFrame
        A pandas Dataframe object
    col : str
        The column to calculate the percentile for
    col_group : list, optional, default None
        The column to group by, by default None
    inplace : bool, optional, default False
        If True the original dataframes will be mutated, by default False

    See Also:
    ---------
    https://stackoverflow.com/questions/50804120/how-do-i-get-the-percentile-for-a-row-in-a-pandas-dataframe
    Using the percentile with linear interpolation method, but kept various
    ranks calculations for reference.

    These are alternative ways of calculating for reference/debugging:

    df["PCNT_RANK"] = df[col].rank(method="max", pct=True)

    df["POF"] = df[col].apply(lambda x: stats.percentileofscore(df[col], x, kind="weak"))

    df["QUANTILE_VALUE"] = df["PCNT_RANK"].apply(lambda x: df[col].quantile(x, "lower"))

    df["CHK"] = df["PCNT_LIN"].apply(lambda x: df[col].quantile(x))

    You can check these methods in acdtion in the test suite

    Returns
    -------
    pandas.DataFrame
        If inplace=False, returns a copy of the dataframe with the new columns added.
        If inplace=True, it will return True, and mutate the original dataframes.

    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(col, (str, list)):
        raise TypeError("col must be a string or, at a stretch, a list of one element")
    if isinstance(col, list):
        if len(col) > 1:
            raise ValueError("expected one element in col")
        else:
            col = col[0]

    if col not in df.columns:
        raise ValueError("col not found in dataframe")
    if col_group and not set(col_group).issubset(set(df.columns)):
        raise ValueError("col_group has elements not found in dataframe")
    if not inplace:
        df = df.copy(deep=True)

    logger.info("Adding percentile column based on column %s", col)
    if col_group:
        col_group_joined = "_".join(col_group)
        df["percentile_in_" + col_group_joined] = (
            df.groupby(col_group)[col].rank(pct=True).mul(100)
        )
        # TODO: #31 research why we use here a different formula when grouping vs full population below
        logger.info("and grouping by column percentile_in_%s", col_group_joined)

    else:
        df["RANKTMP"] = df[col].rank(method="max")
        sz = df["RANKTMP"].size - 1
        df["percentile_in_" + col] = df["RANKTMP"].apply(lambda x: (x - 1) / sz)
        df.drop("RANKTMP", inplace=True, axis=1)
    if inplace:
        return True
    return df
