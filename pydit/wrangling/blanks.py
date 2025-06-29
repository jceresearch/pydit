"""Checks for various types of nulls/blanks in a dataframe and returns counts."""

import pandas as pd
import numpy as np

import logging

logger = logging.getLogger(__name__)


def check_blanks(
    obj,
    columns=None,
    include_zeroes=False,
    include_nullstrings_and_spaces=False,
    totals_only=True,
    silent=False,
):
    """
    Returns by default a summary dictionary with column names as key and
    count of blanks as value, for the columns selected (or all if no column
    list provided)

    If "total_only" is False it would return detailed information of the blanks
     original/copied dataframe with
    a) one boolean column per input columns, True when there are blanks in that record
    b) a summary boolean column if any of the previous is true


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
    silent : bool, optional, default False
        If True, logging level set to critical, ie no info messages shown

    Returns
    -------
    pandas.DataFrame
        A dataframe with the counts of blanks in each column.
        Or a summary dictionary with various counts.

    See also
    --------
    profile_dataframe() : Profile the dataframe, includes metrics on blanks

    Examples
    --------
    Basic usage with a DataFrame containing NaN values:

    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     'A': [1, 2, None, 4],
    ...     'B': ['x', 'y', None, 'z'],
    ...     'C': [1.0, 2.0, 3.0, 4.0]
    ... })
    >>> result = check_blanks(df, silent=True)
    >>> result['A']
    1
    >>> result['B']
    1
    >>> result['C']
    0

    Test with specific columns:

    >>> result = check_blanks(df, columns=['A', 'B'], silent=True)
    >>> len(result)
    2
    >>> 'C' in result
    False

    Test including zeroes as blanks:

    >>> df_zeros = pd.DataFrame({'A': [1, 0, 3], 'B': [0, 2, 0]})
    >>> result = check_blanks(df_zeros, include_zeroes=True, silent=True)
    >>> result['A']
    1
    >>> result['B']
    2

    Test including null strings and spaces:

    >>> df_strings = pd.DataFrame({
    ...     'text': ['hello', '', '   ', 'world', None]
    ... })
    >>> result = check_blanks(df_strings, include_nullstrings_and_spaces=True, silent=True)
    >>> result['text']
    3

    Test with Series input:

    >>> series = pd.Series([1, None, 3, None], name='my_series')
    >>> result = check_blanks(series, silent=True)
    >>> result['my_series']
    2

    Test with totals_only=False to get detailed DataFrame:

    >>> df_small = pd.DataFrame({'A': [1, None], 'B': [None, 2]})
    >>> result = check_blanks(df_small, totals_only=False, silent=True)
    >>> 'A_blanks' in result.columns
    True
    >>> 'has_blanks' in result.columns
    True
    >>> int(result['has_blanks'].sum())
    2

    """
    if silent:
        logger.setLevel(logging.CRITICAL)

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
        df = obj.copy()

    if isinstance(columns, list):
        cols = columns
    elif isinstance(columns, str):
        cols = [columns]
    else:
        cols = df.columns
        logger.debug("No columns provided, checking all columns")
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
        s1 = pd.isna(df[c])
        if include_zeroes:
            s2 = df[c] == 0
        else:
            s2 = pd.Series(False, index=df.index)
        if include_nullstrings_and_spaces:
            s3 = ~df[c].fillna("").astype(str).str.strip().astype(bool)
        else:
            s3 = pd.Series(False, index=df.index)
        s = s1 | s2 | s3
        if not totals_only:
            df[c + "_blanks"] = s
        total_results[c] = int(s.sum())

    if not totals_only:
        new_cols = [c + "_blanks" for c in cols]
        df["has_blanks"] = np.any(df[new_cols], axis=1)

    logger.info(
        "Blanks per column:%s", ",".join([f"{k}:{v}" for k, v in total_results.items()])
    )
    if totals_only:
        return total_results

    return df
