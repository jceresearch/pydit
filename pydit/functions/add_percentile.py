""" add_percentile adds a percentile column to a DataFrame, supports groups """

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def add_percentile(df, col, col_group=None):
    """Adds columns for percentile for a chosen column and also
    within a category group , if provided
    from https://stackoverflow.com/questions/50804120/how-do-i-get-the-percentile-for-a-row-in-a-pandas-dataframe
    Using the percentile with linear interpolation method, but kept
    various ranks calculations for reference

    Args:
        df_in (DataFrame): Pandas DataFrame
        col (str, mandatory): Column to use as value/score
        col_group (List, optional): List of columns,  Defaults to None.

    Returns:
        DataFrame: A new copy of the DataFrame with the percentile column
        
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("df is not a pandas DataFrame")
        return
    if isinstance(col,list) and len(col)==1:
        col=col[0]
    if col not in df.columns:
        logger.error("Column %s not in DataFrame", col)
        return
    if col_group and not set(col_group).issubset(set(df.columns)):
        logger.error("Columns %s not in DataFrame", col_group)
        return
    df = df.copy(deep=True)
    logger.info("Adding percentile column based on column %s", col)
    if col_group:
        col_group_joined = "_".join(col_group)
        df["percentile_in_" + col_group_joined] = (
            df.groupby(col_group)[col].rank(pct=True).mul(100)
        )
        logger.debug("and grouping by column percentile_in_%s", col_group_joined)
    else:
        df["RANKTMP"] = df[col].rank(method="max")
        sz = df["RANKTMP"].size - 1
        df["percentile_in_" + col] = df["RANKTMP"].apply(lambda x: (x - 1) / sz)

        # These are alternative ways of calculating for reference/debugging
        # df["PCNT_RANK"] = df[col].rank(method="max", pct=True)
        # df["POF"] = df[col].apply(
        #    lambda x: stats.percentileofscore(df[col], x, kind="weak")
        # )
        # df["QUANTILE_VALUE"] = df["PCNT_RANK"].apply(
        #    lambda x: df[col].quantile(x, "lower"))
        # df["CHK"] = df["PCNT_LIN"].apply(lambda x: df[col].quantile(x))

        df.drop("RANKTMP", inplace=True, axis=1)

    return df
