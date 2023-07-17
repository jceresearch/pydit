"""Module for checking for duplicates in a dataframe.

It wraps the pandas.DataFrame.duplicated() to perform a more "end to end" check
with logging and informational messages. This can be useful in an audit scenario
as we tend to have to do a lot of duplicate checks in intermediate files.

"""


import logging

import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

logger = logging.getLogger(__name__)

# pylint: disable=logging-not-lazy
# pylint: disable=logging-fstring-interpolation


def check_duplicates(
    obj,
    columns=None,
    keep=False,
    ascending=None,
    add_indicator_column=False,
    also_return_non_duplicates=False,
    dropna=True,
    inplace=False,
):
    """Check for duplicates in a dataframe.


    Parameters
    ----------
    obj:  DataFrame or Series
        The dataframe or series to check for duplicates
    columns: str or list, optional
        Column or list of column(s) to check even if it is one column only.
        If multiple columns provided the check is combined duplicates.
    keep: 'first','last' or False, optional
        Argument for pandas df.duplicated() method.
        Defaults to 'first'.
    ascending: True, False, boolean list with same len() as columns, or None, optional
        Sorting criteria to provide to DataFrame.sort_values() which runs just before the duplicates check.
        Defaults to None.
    indicator: bool, optional
        If True, a boolean column is added to the dataframe to flag duplicate rows.
        Defaults to False
    also_return_non_duplicates: bool, optional
        If True, the return values will include non-duplicate rows too.
    dropna: bool, optional
        If True, the check will ignore NaN values.
        Defaults to True.
    inplace: bool, optional
        If True, the dataframe is modified in place.
        For Series a new dataframe is created and this parameter is ignored.

    Returns
    -------
    pandas.DataFrame
        Returns the DataFrame with the duplicates or None if no duplicates found.
        If also_return_non_duplicates is True, the return values will include
        non-duplicate rows too.

    """

    if not isinstance(obj, (pd.DataFrame, pd.Series)):
        raise TypeError("obj must be a pandas DataFrame or Series")

    if isinstance(obj, pd.Series):
        # If it is Series we convert it to DataFrame
        if obj.name is None and isinstance(columns, str):
            obj.name = columns
        else:
            obj.name = "data"
            columns = "data"
        df = obj.to_frame()

    else:
        # If it is DataFrame we deal with the inplace options
        if not inplace:
            # this creates a new copy
            df = obj.copy()
        else:
            # this is just referencing
            df = obj

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

    has_all_nans = df[cols].isnull().apply(all, axis=1)
    has_any_nans = df[cols].isnull().apply(any, axis=1)
    all_nans_count = sum(has_all_nans)
    not_all_nans_count = sum(has_any_nans) - all_nans_count

    if dropna:
        if all_nans_count > 0:
            df = df.dropna(subset=cols, how="all")
            logger.info("Dropping %s records with all nan:", all_nans_count)
            if not_all_nans_count > 0:
                logger.info(
                    "Of the remaining %s records, %s has some nans",
                    df.shape[0],
                    not_all_nans_count,
                )
    else:
        if all_nans_count > 0:
            logger.info("Dataframe includes %s records with all nan:", all_nans_count)
        if not_all_nans_count > 0:
            logger.info("and %s records with some nan:", not_all_nans_count)

    # Boolean series with the results of all duplicated() method
    ser_duplicates = df.duplicated(cols, keep=False)
    ser_duplicates_first = df.duplicated(cols, keep="first")
    if keep == "last":
        ser_duplicates_last = df.duplicated(
            cols,
            keep="last",
        )
    ser_duplicates_unique = np.logical_and(ser_duplicates, ~ser_duplicates_first)
    logger.info("Duplicates in fields: %s", fields)

    if ser_duplicates.any():
        logger.info("(using keep=%s)", keep)
        logger.info(
            "Found %s unique duplication instances", ser_duplicates_unique.sum()
        )
        logger.info("Totalling %s rows", ser_duplicates.sum())
        logger.info("of a population of %s", len(df))
        if not dropna:
            if all_nans_count > 0:
                logger.info("Remember, duplicates count include 1 for the nan rows")

        blanks_acum = 0
        for c in cols:
            if is_numeric_dtype(df[c]):
                blanks = (pd.isna(df[c])).sum()
                if blanks > 0:
                    logger.warning(f"{blanks} rows with nan in {c}")
                zeroes = (df[c] == 0).sum()
                if zeroes > 0:
                    logger.warning(f"{zeroes} rows with zeroes in {c}")
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

        if ascending is not None:
            # Ascending
            df = df.sort_values(cols, ascending=asc_params)
            logger.info("Sorting by %s with params: %s ", cols, asc_params)

        if also_return_non_duplicates:
            # we return the non duplicates and follow the keep argument
            # for which duplicates to keep
            logger.info(
                "Returning non-duplicates and records we kept with keep=%s", keep
            )
            if add_indicator_column:
                df["_duplicates"] = ser_duplicates
            if keep == "first":
                dfres = df.loc[(~ser_duplicates) | ~ser_duplicates_first].copy()
            elif keep == "last":
                dfres = df.loc[(~ser_duplicates) | ~ser_duplicates_last].copy()
            else:
                dfres = df.copy()

        else:
            # we just return the duplicates
            logger.info("Returning duplicates applying pandas keep=%s", keep)
            if add_indicator_column:
                df["_duplicates"] = ser_duplicates
            if keep == "first":
                dfres = df.loc[ser_duplicates_first].copy()
            elif keep == "last":
                dfres = df.loc[ser_duplicates_last].copy()
            else:
                dfres = df.loc[ser_duplicates].copy()

        return dfres

    else:
        logger.warning("No duplicates found")
        if not inplace and also_return_non_duplicates:
            return df

        return None
