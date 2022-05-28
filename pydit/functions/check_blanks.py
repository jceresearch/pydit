""" 
Checks for blanks in a dataframe and returns the counts of various types of blansk
"""

import logging

import pandas as pd

from pandas.api.types import is_string_dtype, is_numeric_dtype
import numpy as np


logger = logging.getLogger(__name__)


def check_blanks(
    obj_in,
    columns=None,
    zeroes=True,
    null_strings_and_spaces=True,
    totals_only=False,
    inplace=False,
):
    """Reports on blanks in the Dataframe and optionally saves to an excel file

    Args:
        obj_in ([type]): [description]
        columns ([type], optional): [description]. Defaults to None.
        zeroes (bool, optional): [description]. Defaults to True.
        null_strings_and_spaces (bool, optional): [description]. Defaults to True.
        totals_only (bool, optional): [description]. Defaults to False.
        inplace (bool, optional): If True it mutates the dataframe otherwise returns a copy. Defaults to False.

    Returns:
        [type]: [description]
    """

    # We validate and standardise the input
    if not isinstance(obj_in, (pd.DataFrame, pd.Series)):
        raise TypeError("Expecting a dataframe or a Series")
    if isinstance(obj_in, pd.Series):
        if not obj_in.name:
            name = "data"
        else:
            name = obj_in.name

        df = obj_in.to_frame(name=name)
    else:
        if not inplace:
            df = obj_in.copy()

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
        if is_numeric_dtype(df[c]) and zeroes:
            df[c + "_blanks"] = (pd.isna(df[c])) | (df[c] == 0)
        elif is_string_dtype(df[c]) and null_strings_and_spaces:
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
        return total_results

    return df
