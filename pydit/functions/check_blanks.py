""" 
Checks for blanks in a dataframe and returns the counts of various types of blansk
"""

import logging

import pandas as pd

from pandas.api.types import is_string_dtype, is_numeric_dtype
import numpy as np


logger = logging.getLogger(__name__)


def check_blanks(
    obj,
    columns=None,
    include_zeroes=True,
    include_nullstrings_and_spaces=True,
    totals_only=False,
    inplace=False,
):
    """
    Reports on blanks in the Dataframe, one boolean column per input columns,
    plus a summary column that is True if any column has blanks.

    It can optionally return a summary dataframe.


    Parameters
    ----------
    obj : DataFrame or Series
        The dataframe or series to check for blanks
    columns : list, optional
        The columns to check for blanks. If None, all columns are checked.
    include_zeroes : bool, optional
        If True, checks for zeroes as blanks
    include_nullstrings_and_spaces : bool, optional
        If True, checks for null strings and spaces as blanks
    totals_only : bool, optional
        If True, only the total counts are returned
    inplace : bool, optional
        If True, the dataframe is modified in place. If False, a new dataframe is returned.
        Defaults to False.

    Returns
    -------
    DataFrame
        A dataframe with the counts of blanks in each column.
        Or a summary list with various counts.



    Examples
    --------


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
    try:
        dfsubset = df[cols]
    except:
        raise ValueError("Columns not found in dataframe")

    fields = ",".join(cols)
    logger.info("Checking for blanks in %s", fields)
    total_results = []
    for c in cols:
        if is_numeric_dtype(df[c]) and include_zeroes:
            df[c + "_blanks"] = (pd.isna(df[c])) | (df[c] == 0)
        elif is_string_dtype(df[c]) and include_nullstrings_and_spaces:
            df[c + "_strip"] = df[c].fillna("").astype(str).str.strip()
            logger.debug("Checking for spaces and nullstring too in %s", c)
            df[c + "_blanks"] = ~df[c + "_strip"].astype(bool)
            df.drop(c + "_strip", axis=1, inplace=True)
        else:
            logger.debug("Checking just for NaN or NaT in %s", c)
            df[c + "_blanks"] = pd.isna(df[c])
        total_results.append(df[c + "_blanks"].sum())
    new_cols = [c + "_blanks" for c in cols]
    df["has_blanks"] = np.any(df[new_cols], axis=1)

    logger.info(
        "Total blanks found in each column:\n%s", dict(zip(cols, total_results))
    )

    if totals_only:
        dict_totals = dict(zip(cols, total_results), columns=["column", "count"])
        return dict_totals

    return df
