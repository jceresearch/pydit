"""Functions to sweep a dataframe for keywords and return a matrix of matches.
"""

import logging
import re

import pandas as pd
import numpy as np
from pandas import DataFrame


logger = logging.getLogger(__name__)


def _keyword_search_re(keywords, df, case_sensitive):
    """Internal function to do keyword search with regexp (regular expressions).

    If you dont know what is a regexp, then you probably want to use
    the simpler string search, but regexps are way more powerful

    Arguments
    ---------
    keywords : list of strings
        The list of regular expressions as string
    df : pandas.DataFrame
        The dataframe to search.
    case_sensitive : bool
        If True then the keywords are case sensitive.
        Provided by the parent function

    Returns
    -------
    pandas.DataFrame
        The dataframe with the boolean columns one per keyword searched.


    """

    # We do a quick compilation pass so we can detect issues with the regex
    re_compiled = []
    for re_text in keywords:
        try:
            if case_sensitive:
                pattern = re.compile(re_text)
            else:
                pattern = re.compile(re_text, re.IGNORECASE)
            re_compiled.append(pattern)
        except Exception as e:
            raise ValueError("Invalid regular expression: " + re_text) from e
    dfres = pd.DataFrame()
    n = 1  # used for column naming
    for p in re_compiled:
        logger.info("Searching for keyword: %s", p.pattern)
        regmatch = np.vectorize(lambda x: bool(p.search(x)))
        res = regmatch(df["dummy_keyword_search"].values)
        logger.info("Found %d matches", sum(res))
        dfres["kw_match" + str.zfill(str(n), 2)] = res
        n = n + 1
    return dfres


def _keyword_search_str(keywords, df, case_sensitive):
    """Internal function to do a simpler keyword search with no regular expressions

    While less powerful it could be faster if we wish to do lots of keywords on a
    large file, normally regexp are fine and can take normal keywords too, use
    this as an exception.

    Arguments
    ---------
    keywords : list of strings
        The list of keywords to search for.
    df : pandas.DataFrame
        The dataframe to search.
    case_sensitive : bool, default False

    Returns
    -------
    pandas.DataFrame
        The dataframe with the boolean columns one per keyword searched.


    """
    if case_sensitive:
        # We just use the values directly
        listed = df["dummy_keyword_search"].tolist()
    else:
        keywords = [x.lower() for x in keywords]
        listed = df["dummy_keyword_search"].str.lower().tolist()
    dfres = pd.DataFrame()
    for i, kw in enumerate(keywords):
        dfres["kw_match" + str.zfill(str(i + 1), 2)] = [kw in n for n in listed]
    return dfres


def keyword_search(
    obj,
    keywords,
    columns=None,
    return_hit_columns_only=False,
    regexp=True,
    case_sensitive=False,
):
    """
    Searches the keywords in a dataframe or series and returns a matrix of matches

    Creates a boolean column in the dataframe, one per keyword
    and a combined column that is True if any of the other columns is True.
    For simplicity we name columns sequentially as pushing keywords straight
    as columns may yield error with special characters or duplicated/banned names

    Parameters
    ----------
    obj : pandas.DataFrame or pandas.Series
        The dataframe or series to search
    keywords : list
        The list of regular expressions or string keywords to search for.
    columns : list
        The list of columns to search in, if None then all columns are searched
    return_hit_columns_only : bool, optional, default=False
        If True then it only returns the boolean columns created, by default
        it will return the dataframe with the boolean columns added.
    regexp : bool, default True
        If True then the keywords are treated as regular expressions, otherwise
        a simpler string search is performed.
    case_sensitive : bool, default False
        If True then the keywords are case sensitive. The most typical
        case is that we do NOT care about case sensitivity.
        Note: use case_sensitive=True and include special prefix (?i) in the
        regexp itself to disable case sensitivity.
        E.g. the same way you do re.findall('(?i)test', s)

    Returns
    -------
    DataFrame
        A copy of the dataframe with the new hit columns added or just
        the boolean columns for each keyword (depending on return_hit_columns_only)
        Plus a combined column that is true if any of the other columns is true.

    """

    if not isinstance(keywords, (list, str)):
        raise ValueError("keywords must be a list of strings or a string")
    if isinstance(keywords, str):
        keywords = [keywords]
    if isinstance(columns, str):
        columns = [columns]
    if columns:
        try:
            df = obj[columns].copy()
        except Exception as e:
            raise ValueError("Columns not found in dataframe") from e

    else:
        if isinstance(obj.Series):
            df = obj.to_frame()

        elif isinstance(obj, DataFrame):
            df = obj.copy()
        elif isinstance(obj, list):
            df = pd.DataFrame(obj, columns="text_data")

        else:
            raise TypeError("Type not recognised")

    df.fillna("", inplace=True)
    if len(columns) > 1:
        df["dummy_keyword_search"] = df[columns].astype(str).T.agg(" ".join)
    else:
        df["dummy_keyword_search"] = df[columns].astype(str)

    if regexp:
        dfres = _keyword_search_re(keywords, df, case_sensitive)
    else:
        dfres = _keyword_search_str(keywords, df, case_sensitive)

    dfres["kw_match_all"] = dfres.apply(any, axis=1)
    if return_hit_columns_only:
        return dfres
    df = df.join(dfres)
    return df
