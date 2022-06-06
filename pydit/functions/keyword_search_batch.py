"""Functions to sweep a dataframe for keywords and return a matrix of matches.
"""

import logging
import re

import pandas as pd
import numpy as np
from pandas import Series, DataFrame


logger = logging.getLogger(__name__)


def keyword_search(obj, keywords, columns=None):
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

    Returns
    -------
    DataFrame
        The dataframe with the new columns added
        This is a copy of the original dataframe

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
        except:
            raise ValueError("Columns not found in dataframe")

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

    n = 1
    dfres = pd.DataFrame()
    for re_text in keywords:
        logger.info("Searching for keyword: %s", re_text)
        pattern = re.compile(re_text, re.IGNORECASE)
        # TODO: keyword_search() implement option for case sensitive search
        regmatch = np.vectorize(lambda x: bool(pattern.search(x)))
        dfres["kw_match" + str.zfill(str(n), 2)] = regmatch(
            df["dummy_keyword_search"].values
        )
        n = n + 1

    match_columns = [m for m in dfres.columns if "kw_match" in m]

    dfres["kw_match_all"] = dfres.apply(lambda row: any(row[match_columns]), axis=1)

    return dfres


def keyword_search_str(keyword_list, df_in, field_name):
    """Simpler version with no regular expressions, which is less powerful but
    could be faster if we wish to do lots of keywords on a large file, normally
    regexp are fine and can take normal keywords too, use this as an exception"""
    df = df_in.copy()
    keyword_list = [x.lower() for x in keyword_list]
    listed = df[field_name].str.lower().tolist()
    for i, kw in enumerate(keyword_list):
        df["kw_match" + str.zfill(str(i + 1), 2)] = [kw in n for n in listed]
    match_columns = [m for m in df.columns if "kw_match" in m]
    df["kw_match_all"] = df.apply(lambda row: any(row[match_columns]), axis=1)
    return df
