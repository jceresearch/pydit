""" Profiling functions"""


import logging

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_string_dtype, is_numeric_dtype

# from scipy import stats

logger = logging.getLogger(__name__)


def profile_dataframe(df):
    """[summary]
    Args:
        df ([type]): [description]
    Returns:
        [type]: [description]
    """
    # df=in_df.copy() # if we needed to do transformations create a copy
    if isinstance(df, pd.DataFrame):
        dtypes = df.dtypes.to_dict()
    else:
        return
    col_metrics = []
    for col, typ in dtypes.items():
        metrics = {}
        metrics["column"] = col
        metrics["dtype"] = typ
        metrics["records"] = len(df[col])
        metrics["count_unique"] = len(set(df[pd.notna(df[col])][col]))
        metrics["nans"] = len(df[pd.isnull(df[col])])
        if metrics["count_unique"] < 5:
            value_counts_series = df[col].value_counts(dropna=False)
            metrics["value_counts"] = value_counts_series.to_dict()
        else:
            metrics["value_counts"] = []
        if "float" in str(typ):
            metrics["max"] = max(df[col])
            metrics["min"] = min(df[col])
            metrics["sum"] = sum(df[col])
            metrics["sum_abs"] = sum(abs(df[col]))
            metrics["std"] = df[col].std()
            metrics["zeroes"] = np.count_nonzero(df[col] == 0)
            # TODO: possibly add hist/sparkline data to further add to the profiling
        elif "int" in str(typ):
            metrics["max"] = max(df[col])
            metrics["min"] = min(df[col])
            metrics["sum"] = sum(df[col])
            metrics["sum_abs"] = sum(abs(df[col]))
            metrics["std"] = df[col].std()
            metrics["zeroes"] = np.count_nonzero(df[col] == 0)
        elif is_datetime(df[col]):
            metrics["max"] = max(df[col])
            metrics["min"] = min(df[col])
        elif typ == "object":
            values = df[pd.notna(df[col])][col]
            numeric_chars = values.str.replace(
                r"[^0-9^-^.]+", "", regex=True
            )  # TODO: refactor this regex, currently very simplistic works only for clean id sequences, e.g. double dots
            numeric_chars_no_blank = numeric_chars[numeric_chars.str.len() > 0]
            numeric = pd.to_numeric(numeric_chars_no_blank, errors="coerce")
            if len(numeric) > 0:
                metrics["max"] = max(numeric)
                metrics["min"] = min(numeric)
            metrics["empty_strings"] = len(df[df[col].str.strip().eq("")])
        col_metrics.append(metrics)

    df_metrics = pd.DataFrame(col_metrics)
    df_metrics["cardinality_perc"] = df_metrics["count_unique"] / df_metrics["records"]
    return df_metrics


def add_percentile(df_in, col, col_group=None):
    """Adds columns for percentile for a chosen column and also
    wilhing a category group , if provided 
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
    if not isinstance(df_in, pd.DataFrame):
        return
    if col not in df_in.columns:
        return
    if col_group and not set(col_group).issubset(set(df_in.columns)):
        return
    df = df_in.copy()
    logger.info("Adding percentile column based on column %s", col)
    if col_group:
        col_group_joined = "_".join(col_group)
        df["percentile_in_" + col_group_joined] = (
            df.groupby(col_group)[col].rank(pct=True).mul(100)
        )
        logger.debug("and grouping by column percentile_in_%s", col_group_joined)
    else:
        # df["PCNT_RANK"] = df[col].rank(method="max", pct=True)
        # df["POF"] = df[col].apply(
        #    lambda x: stats.percentileofscore(df[col], x, kind="weak")
        # )
        # df["QUANTILE_VALUE"] = df["PCNT_RANK"].apply(
        #    lambda x: df[col].quantile(x, "lower")
        # )
        df["RANKTMP"] = df[col].rank(method="max")
        sz = df["RANKTMP"].size - 1
        df["percentile_in_" + col] = df["RANKTMP"].apply(lambda x: (x - 1) / sz)
        # df["CHK"] = df["PCNT_LIN"].apply(lambda x: df[col].quantile(x))
        df.drop("RANKTMP", inplace=True, axis=1)

    return df


def main():
    """ Profiling routines routine"""


if __name__ == "__main__":
    main()
