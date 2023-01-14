""" Calculate basic dataframe metrics on data completion/quality/uniqueness
"""
import logging

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

logger = logging.getLogger(__name__)


def profile_dataframe(obj, return_dict=False, unique_min=10):
    """Create a summary of a DataFrame with various statistics.

    Returns a DataFrame or a dict with common statistics to profile the data.
    In particular it focuses on unique (cardinality) blanks, nulls, and datetimes.

    Parameters
    ----------
    obj : pandas.DataFrame
        DataFrame to profile.
    return_dict : bool, optional, default=False
        If True, return a dict instead of a DataFrame.

    unique_min : int, optional, default=10

    Returns
    -------
    DataFrame
        DataFrame with various statistics.

    """

    if isinstance(obj, pd.DataFrame):
        df = obj.copy()
        df.reset_index(
            inplace=True
        )  # this moves the index as a column so we can profile it too
        dtypes = df.dtypes.to_dict()
    else:
        raise TypeError("df must be a pandas.DataFrame")
    logger.info("Profiling dataframe: %s rows , %s columns", df.shape[0], df.shape[1])

    col_metrics = []
    for col, typ in dtypes.items():
        metrics = {}
        metrics["column"] = col
        metrics["dtype"] = typ
        metrics["records"] = len(df[col])
        metrics["count_unique"] = len(set(df[pd.notna(df[col])][col]))
        metrics["nans"] = len(df[pd.isnull(df[col])])
        if metrics["count_unique"] <= unique_min:
            value_counts_series = df[col].value_counts(dropna=False)
            metrics["value_counts"] = value_counts_series.to_dict()
        else:
            metrics["value_counts"] = []
        if "float" in str(typ):
            metrics["max"] = max(df[col])
            metrics["min"] = min(df[col])
            metrics["sum"] = df[col].sum(skipna=True)
            metrics["sum_abs"] = df[col].abs().sum(skipna=True)
            metrics["std"] = df[col].std()
            metrics["zeroes"] = np.count_nonzero(df[col] == 0)
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
            values = df[col].fillna("").astype(str).str.strip()
            numeric_chars = values.str.replace(
                r"[^0-9^-^.]+", "", regex=True
            )  # TODO: refactor this regex for more general cases
            numeric_chars_no_blank = numeric_chars[numeric_chars.str.len() > 0]
            numeric = pd.to_numeric(numeric_chars_no_blank, errors="coerce")
            if len(numeric) > 0:
                metrics["max"] = max(numeric)
                metrics["min"] = min(numeric)
            metrics["empty_strings"] = len(values[values.str.len() == 0])
        col_metrics.append(metrics)

    df_metrics = pd.DataFrame(col_metrics)
    df_metrics["cardinality_perc"] = df_metrics["count_unique"] / df_metrics["records"]
    if return_dict:
        return df_metrics.set_index("column").T.to_dict()
    cols = [
        "column",
        "dtype",
        "records",
        "count_unique",
        "nans",
        "zeroes",
        "empty_strings",
        "cardinality_perc",
        "max",
        "min",
        "sum",
        "sum_abs",
        "std",
        "value_counts",
    ]
    return df_metrics[cols]
