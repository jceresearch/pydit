""" Convenience function to check for duplicates in a dataframe
Check from codespaces
"""


import logging
from typing import Union

import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype


logger = logging.getLogger(__name__)

# pylint: disable=logging-not-lazy
# pylint: disable=logging-fstring-interpolation


def check_duplicates(
    df_or_series,
    columns=None,
    keep=False,
    ascending=None,
    indicator=False,
    return_non_duplicates=False,
    inplace=False,
):
    """
    Duplicate analysis
    Args:
        df_or_series: pandas dataframe or series

        columns (str or list, optional): column or list of column(s) to check
        even if it is one column only, if multiple columns provided
        the check is combined duplicates, exactly as pandas duplicated().

        keep ('first','last' or False, optional): Argument for pandas df.duplicated() method.
        Defaults to 'first'.

        ascending (True, False or None, optional): Argument for DataFrame.value_counts()
        Defaults to None.

        indicator=(True, False, optional): If True, a column is added to the dataframe.
        Defaults to False

        inplace (bool, optional): If True, the dataframe is modified in place.
        If a Series is provided then it is always copied into a new dataframe and
        this parameter is ignored.

    Returns:
        Returns the DataFrame with the duplicates or None if no duplicates found.
    """

    if not isinstance(df_or_series, (pd.DataFrame, pd.Series)):
        raise TypeError("df_or_series must be a pandas DataFrame or Series")

    if isinstance(df_or_series, pd.Series):
        # If it is Series we convert it to DataFrame
        if df_or_series.name is None and isinstance(columns, str):
            df_or_series.name = columns

        else:
            df_or_series.name = "data"
            columns = "data"
        df = df_or_series.to_frame()

    else:
        # If it is DataFrame we deal with the inplace options
        if not inplace:
            # this creates a new copy
            df = df_or_series.copy()
        else:
            # this is just referencing
            df = df_or_series

    if isinstance(columns, str):
        if columns in df.columns:
            cols = [columns]
        else:
            raise ValueError(f"column {columns} not in dataframe")
    else:
        if isinstance(columns, list):
            check_isin = [x in df.columns for x in columns]
            if all(check_isin):
                cols = columns
            else:
                raise ValueError("at least one column provided not in dataframe")
        else:
            cols = df.columns

    fields = ",".join(cols)

    ser_duplicates = df.duplicated(cols, keep=False)
    if keep == "first" or keep == "last":
        ser_duplicates_keep = df.duplicated(cols, keep=keep)
        df["_duplicates_keep"] = ser_duplicates_keep
    else:
        # even if we want the total we do a keep=first to tally the unique instances
        ser_duplicates_keep = df.duplicated(cols, keep="first")
        df["_duplicates_keep"] = ser_duplicates_keep
    df["_duplicates"] = ser_duplicates

    logger.info("Duplicates in fields: %s", fields)

    if df["_duplicates"].any():
        logger.info("(using keep=%s)", keep)
        logger.info("Found %s instances of duplication", df["_duplicates_keep"].sum())
        logger.info("Totalling %s rows", df["_duplicates"].sum())
        logger.info("of population %s", len(df))
        blanks_acum = 0
        for c in cols:
            if is_numeric_dtype(df[c]):
                blanks = ((pd.isna(df[c])) | (df[c] == 0)).sum()
                if blanks > 0:
                    logger.warning(f"{blanks} rows with zeroes or nan in {c}")
            elif is_string_dtype(df[c]):
                blanks = ((pd.isna(df[c])) | (df[c].str.strip() == "")).sum()
                if blanks > 0:
                    logger.warning(f"{blanks} rows with blanks or nan in {c}")
            else:
                blanks = (pd.isna(df[c])).sum()
                if blanks > 0:
                    logger.warning(f"{blanks} rows with nans in {c}")
            blanks_acum += blanks
        if blanks_acum == 0:
            logger.info("No blanks found in the key column(s) provided")

        if ascending is True:
            # Ascending
            df = df.sort_values(cols, ascending=True)
        elif ascending is False:
            # Descending
            df = df.sort_values(cols, ascending=False)

        if return_non_duplicates is False:
            # we just return the duplicates
            dfres = df[df["_duplicates"] == True].copy()
            if keep:
                dfres = dfres[dfres["_duplicates_keep"] == False].copy()
                if indicator:
                    dfres.drop("_duplicates", axis=1, inplace=True)
                else:
                    dfres.drop("_duplicates_keep", axis=1, inplace=True)
                    dfres.drop("_duplicates", axis=1, inplace=True)
            else:
                if indicator:
                    dfres.drop("_duplicates_keep", axis=1, inplace=True)
                else:
                    dfres.drop("_duplicates_keep", axis=1, inplace=True)
                    dfres.drop("_duplicates", axis=1, inplace=True)

        else:
            # we return the non duplicates and follow the keep argument
            # for which duplicates to keep
            dfres = df.copy()
            if keep:
                dfres = dfres[dfres["_duplicates_keep"] == False].copy()
                if indicator:
                    dfres.drop(columns=["_duplicates"], inplace=True)
                else:
                    # If the user doesnt want the indicators we drop them
                    dfres.drop(columns=["_duplicates_keep"], inplace=True)
                    dfres.drop(columns=["_duplicates"], inplace=True)

            else:
                # regardless of the indicator flag, if we bring all records and keep=False we somehow need to flag the duplicates
                dfres.drop(columns=["_duplicates_keep"], inplace=True)

        return dfres

    else:
        logger.info("No duplicates found")
        return None
