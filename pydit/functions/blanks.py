""" Checks for various types of nulls/blanks in a dataframe and returns counts.
"""

import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype
import numpy as np

import logging

logger = logging.getLogger(__name__)


def check_blanks(
    obj,
    columns=None,
    include_zeroes=False,
    include_nullstrings_and_spaces=False,
    totals_only=False,
    inplace=False,
):
    """
    Reports on blanks in the Dataframe, one boolean column per input columns,
    plus a summary boolean column showing (True for each record if any column has blanks.

    It can optionally return a summary dataframe.
    Check out https://github.com/ResidentMario/missingno library for
    a nice visualization (seems to come with Anaconda)

    Parameters
    ----------
    obj : DataFrame or Series
        The dataframe or series to check for blanks
    columns : list, optional, default None
        The columns to check for blanks. If None, all columns are checked.
    include_zeroes : bool, optional, default False
        If True, checks for zeroes as blanks
    include_nullstrings_and_spaces : bool, optional, default False
        If True, checks for null strings and spaces as blanks
    totals_only : bool, optional, default False
        If True, only the total counts are returned
    inplace : bool, optional, default False
        If True, the dataframe is modified in place. If False, a new dataframe is returned.

    Returns
    -------
    pandas.DataFrame
        A dataframe with the counts of blanks in each column.
        Or a summary dictionary with various counts.
        If inplace is True, the dataframe is modified in place and returns True

    See also
    --------
    profile_dataframe() : Profile the dataframe, includes metrics on blanks

    """

    # We validate and standardise the input
    if not isinstance(obj, (pd.DataFrame, pd.Series)):
        raise TypeError("Expecting a dataframe or a Series")
    if isinstance(obj, pd.Series):
        if not obj.name:
            name = "data"
        else:
            name = obj.name

        df = obj.to_frame(name=name)
        inplace = False  # to ensure we return a dataframe
    else:
        if not inplace:
            df = obj.copy()

    if isinstance(columns, list):
        cols = columns
    elif isinstance(columns, str):
        cols = [columns]
    else:
        cols = df.columns
        logger.debug("Using all columns")
    if not set(cols).issubset(set(df.columns)):
        raise ValueError("Column(s) provided not found in the dataframe")

    fields = ",".join(cols)
    logger.info("Checking for blanks in %s", fields)
    if include_zeroes:
        logger.info("Including zeroes as blanks")
    if include_nullstrings_and_spaces:
        logger.info("Including null strings and spaces as blanks")

    total_results = {}

    for c in cols:
        if is_numeric_dtype(df[c]) and include_zeroes:
            s = (pd.isna(df[c])) | (df[c] == 0)
            if not totals_only:
                df[c + "_blanks"] = s
            total_results[c] = s.sum()
        elif is_string_dtype(df[c]) and include_nullstrings_and_spaces:
            s = ~df[c].fillna("").astype(str).str.strip().astype(bool)
            if not totals_only:
                df[c + "_blanks"] = s
            total_results[c] = s.sum()
        else:
            if not totals_only:
                df[c + "_blanks"] = pd.isna(df[c])
            total_results[c] = df[c].isnull().sum()

    if not totals_only:
        new_cols = [c + "_blanks" for c in cols]
        df["has_blanks"] = np.any(df[new_cols], axis=1)

    logger.info("Total blanks found in each column:\n%s", total_results)
    if totals_only:
        return total_results

    if inplace:
        return True

    return df
