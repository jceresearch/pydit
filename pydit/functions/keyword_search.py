""" 
functions to sweep a dataframe for keywords and return a matrix of matches
or a sparse matrix if the keyword list is large
"""

import logging
import re

import pandas as pd
import numpy as np
from pandas import Series, DataFrame


logger = logging.getLogger(__name__)


def keyword_search(obj_in, keywords, columns=None):
    """
    Searches the keywords in a dataframe or series and returns a matrix of matches

    Creates a boolean column in the dataframe, one per keyword
    and a combined column that is True if any of the other columns is True.
    For simplicity we name columns sequentially as pushing keywords straight
    as columns may yield error with special characters or duplicated/banned names
    """

    if not keywords:
        raise ValueError("keywords must be a list of strings or a string")

    if columns:
        try:
            df = obj_in[columns].copy()
        except:
            raise ValueError("Columns not found in dataframe")

    else:
        if isinstance(obj_in, Series):
            df = obj_in.to_frame()

        elif isinstance(obj_in, DataFrame):
            df = obj_in.copy()
        elif isinstance(obj_in, list):
            df = pd.DataFrame(obj_in, columns="text_data")

        else:
            raise ValueError("Type not recognised")

    if isinstance(keywords, str):
        keywords = [keywords]

    df.fillna("", inplace=True)
    if len(columns) > 1:
        df["dummy_keyword_search"] = df[columns].astype(str).T.agg(" ".join)
    else:
        df["dummy_keyword_search"] = df[columns].astype(str)

    n = 1

    for re_text in keywords:
        print(re_text)
        pattern = re.compile(re_text, re.IGNORECASE)
        regmatch = np.vectorize(lambda x: bool(pattern.search(x)))
        df["kw_match" + str.zfill(str(n), 2)] = regmatch(
            df["dummy_keyword_search"].values
        )
        n = n + 1

    match_columns = [m for m in df.columns if "kw_match" in m]
    df["kw_match_all"] = df.apply(lambda row: any(row[match_columns]), axis=1)
    df.drop(["dummy_keyword_search"], axis=1, inplace=True)

    return df


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
