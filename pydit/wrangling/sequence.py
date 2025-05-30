"""Module to check for numerical sequence of DataFrame column or Series"""

# pylint disable=import-error, bare-except, unu


import logging
from datetime import date
import itertools

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas import Series

logger = logging.getLogger(__name__)


def check_sequence(obj_in, col=None):
    """Checks the numerical sequence of a series including dates

    If a text column is provided it will attempt to convert to numeric after
    extacting any non numeric chars.

    Parameters
    ----------
    obj_in : list, pandas.Series or pandas.DataFrame
        The list, series or dataframe to check
    col : str
        The column name to check, if a DataFrame is provided.


    Returns
    -------
    list
        A list of the missing values in the series

    """

    # TODO: #32 check_sequence() refactor to do better input validation and error handling and simpler flow control
    if col:
        try:
            obj = obj_in[col]
        except Exception as exc:
            raise ValueError("Column not found in dataframe") from exc
    else:
        if isinstance(obj_in, Series):
            obj = obj_in.copy()
        elif isinstance(obj_in, list):
            obj = pd.Series(obj_in)
        else:
            raise TypeError(
                f"Object type not supported, needs to be a list or series: {type(obj_in)}"
            )
    if "int" in str(obj.dtype):
        logger.debug("Data is of type integers")
        unique = set([i for i in obj[pd.notna(obj)]])
        fullrng = set(range(min(unique), max(unique) + 1))
        diff = fullrng.difference(unique)
        if diff:
            logger.info("Missing values: %s", len(diff))
            logger.info("First 10 missing values: %s", list(diff)[:10])
            return list(diff)
        else:
            logger.info("Sequence provided is complete")
            return []
    if "object" in str(obj.dtype):
        try:
            max_value = obj[obj.notnull()].max()
            if isinstance(max_value, date):
                obj = pd.to_datetime(obj, errors="coerce")
                logger.debug("Converted to datetime")
            else:
                pass
        except Exception as e:
            raise ValueError(
                "Multiple data types detected, please cleanup the column first"
            ) from e
    if is_datetime(obj):
        unique = set([i.date() for i in obj[pd.notna(obj)]])
        fullrng = pd.date_range(min(unique), max(unique), freq="d")
        fullrng = set([i.date() for i in fullrng])
        diff = fullrng.difference(unique)
        if diff:
            logger.info("Missing values: %s", len(diff))
            logger.info("First 10 missing values: %s", list(diff)[:10])
            working_days = [wd for wd in diff if wd.weekday() < 5]
            logger.info("Working days missing: %s", len(working_days))
            logger.info("First 10 working days missing: %s", working_days[:10])
            return list(diff)
        else:
            logger.info("Sequence of dates is complete")
            return []
    if "float" in str(obj.dtype):
        logger.debug("Data is of type floats")
        unique = set([int(i) for i in obj[pd.notna(obj)]])
        fullrng = set(range(min(unique), max(unique)))
        diff = fullrng.difference(unique)
        if diff:
            logger.info("Missing values: %s", len(diff))
            logger.info("First 10 missing values: %s", list(diff)[:10])
            return list(diff)
        else:
            logger.info("Sequence provided is complete")
            return []

    if "object" in str(obj.dtype):
        logger.debug("Strings object as if they were dates we already processed")
        numeric_chars = obj.fillna("").str.replace(r"[^0-9]", "", regex=True)
        numeric_chars_no_blank = numeric_chars[numeric_chars != ""]
        numeric = pd.to_numeric(
            numeric_chars_no_blank, errors="coerce", downcast="integer"
        )
        print("numeric_chars", numeric_chars)
        print("numeric", numeric)
        unique = set(numeric)
        if unique:
            fullrng = set(range(min(unique), max(unique)))
            diff = fullrng.difference(unique)
            if diff:
                logger.info("Missing values: %s", len(diff))
                logger.info("Fist 10:%s", list(diff)[:10])
                return list(diff)
            else:
                logger.info("Sequence is complete")
                return []
        else:
            raise ValueError("No numeric values found")
    return


def group_gaps(gap_list):
    """Groups a list of gaps into a list of lists of consecutive gaps

    Parameters
    ----------
    gap_list : list
        A list of gaps (integers)

    Returns
    -------
    list
        A list of lists of consecutive gaps

    """
    try:

        def to_ranges(iterable):
            iterable = sorted(set(iterable))
            for key, group in itertools.groupby(
                enumerate(iterable), lambda t: t[1] - t[0]
            ):
                group = list(group)
                yield [group[0][1], group[-1][1], group[-1][1] - group[0][1] + 1]

        df_grouped = pd.DataFrame.from_records(
            list(to_ranges(gap_list)), columns=["start", "end", "count"]
        )
    except TypeError as exc:
        raise TypeError("Grouping only works for integers for now") from exc
    return df_grouped
