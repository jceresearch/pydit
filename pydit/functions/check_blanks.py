""" Validation functions"""

import logging

import pandas as pd

from pandas.api.types import is_string_dtype, is_numeric_dtype
import numpy as np


logger = logging.getLogger(__name__)


def check_blanks(
    df, columns=None, zeroes=True, null_strings_and_spaces=True, totals_only=False,
):
    """ Reports on blanks in the Dataframe and optionally saves to an excel file

    Args:
        df_in ([type]): [description]
        columns ([type], optional): [description]. Defaults to None.
        zeroes (bool, optional): [description]. Defaults to True.
        null_strings_and_spaces (bool, optional): [description]. Defaults to True.
        totals_only (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """

    if not isinstance(df, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        return
    df = df.copy()
    if columns and isinstance(columns, list):
        cols = columns
    elif not columns:
        cols = df.columns
    else:
        logger.error("Expecting a list, even a list of one element")
        return

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
