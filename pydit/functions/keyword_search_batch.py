"""Functions to sweep a dataframe for keywords and return a matrix of matches.

"""

import logging
import re
import math

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
    zeroes = max(math.ceil(math.log10(len(keywords))), 2)
    for p in re_compiled:
        logger.info("Searching for keyword: %s", p.pattern)
        regmatch = np.vectorize(lambda x: bool(p.search(x)))
        res = regmatch(df["dummy_keyword_search"].values)
        logger.info("Found %d matches", sum(res))

        dfres["kw_match" + str.zfill(str(n), zeroes)] = res
        n = n + 1
    return dfres


def _keyword_search_str(keywords, df, case_sensitive):
    """Internal function to do a simple string search, no regular expressions used.

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
    return_data="full",
    regexp=True,
    case_sensitive=False,
    labels=None,
    key_column=None,
):
    """
    Searches the keywords in a dataframe or series and returns a matrix of matches

    Creates a boolean column in the dataframe, one per keyword
    and a combined column that is True if any of the other columns is True.
    For simplicity by default we name columns sequentially, pushing keywords
    straight away as columns may yield error with special characters or
    duplicated/banned names.
    If you need labels there is an option to provide them.

    Parameters
    ----------
    obj : pandas.DataFrame or pandas.Series
        The dataframe or series to search
    keywords : list
        The list of regular expressions or string keywords to search for.
    columns : list
        The list of columns to search in, if None then all columns are searched
    return_data : str, optional default="full"
        If "full" then the full dataframe is returned, plus hit columns
        If "target" then the target columns and hits are returned,
        If "result" then only the boolean result columns will be returned,
        If "detail" then a dataframe with a hit per row is returned
        If you use "full_hits", "target_hits" or "result_hits" then only hit rows are returned
    regexp : bool, default True
        If True then the keywords are treated as regular expressions, otherwise
        a simpler string search is performed.
    case_sensitive : bool, default False
        If True then the keywords are case sensitive. The most typical
        case is that we do NOT care about case sensitivity.
        Note: use case_sensitive=True and include special prefix (?i) in the
        regexp itself to disable case sensitivity.
        E.g. the same way you do re.findall('(?i)test', s)
    labels : list, optional
        The list of labels to use for the columns, if None then the labels are
        kw_match_NN. Labels must be the same length as the number of keywords.
        But they could be repeated and automagically will be grouped/rolled up.
    key_column : str, optional, default=None
        If return_data="detail", this is the column to use as the key for
        the returned dataframe

    Returns
    -------
    DataFrame
        A copy of the dataframe with the new hit columns added or just
        the boolean columns for each keyword (depending on return_hit_columns_only)
        Plus a column kw_match_all that is True if any of the other columns is True.

    """

    # Various input validation
    if not isinstance(keywords, (list, str)):
        raise ValueError("keywords must be a list of strings or a string")
    if isinstance(keywords, str):
        keywords = [keywords]
    if isinstance(columns, str):
        columns = [columns]
    if columns:
        try:
            df = obj[columns].copy()
            dffull = obj.copy()
        except Exception as e:
            raise ValueError("Columns not found in dataframe") from e

    else:
        if isinstance(obj.Series):
            df = obj.to_frame()
            dffull = df.copy()

        elif isinstance(obj, DataFrame):
            df = obj.copy()
            dffull = obj.copy()
        elif isinstance(obj, list):
            df = pd.DataFrame(obj, columns="text_data")
            dffull = df.copy()
        else:
            raise TypeError("Type not recognised")

    if labels and (len(labels) != len(keywords)):
        raise ValueError("Number of labels must match number of keywords")
    if len(keywords) < 20:
        logger.info("Searching for keywords: %s", keywords)
    else:
        logger.info("Searching for %d keywords", len(keywords))
    logger.info("Rows to check: %s", df.shape[0])
    if case_sensitive:
        logger.info("Applying case sensitive search")
    if not regexp:
        logger.info("Applying simple keyword search instead of regexp")
    if labels:
        if len(set(labels)) < len(keywords):
            logger.info(
                "Labels provided are repeated, so they will be rolled up using OR logical operator"
            )
    return_data = return_data.lower()
    if return_data not in [
        "full",
        "target",
        "result",
        "detail",
        "full_hits",
        "target_hits",
        "result_hits",
    ]:
        raise ValueError(
            "return_data must be one of full, target, result or detail or ending with _hits"
        )

    if return_data == "full":
        logger.info("Returning full dataframe")
    if return_data == "result":
        logger.info("Returning results (boolean) columns only")
    if return_data == "detail":
        logger.info("Returning details")
    if return_data == "target":
        logger.info("Returning target and boolean columns")

    if return_data == "detail":
        if key_column is None:
            raise ValueError("Must provide a key column if return_details is True")
        if key_column not in dffull.columns:
            raise ValueError("Key column %s not found in dataframe" % key_column)
    # Here the main part of the function starts
    df.fillna("", inplace=True)
    if len(columns) > 1:
        df["dummy_keyword_search"] = df[columns].astype(str).T.agg(" ".join)
    else:
        df["dummy_keyword_search"] = df[columns].astype(str)

    if regexp:
        dfres = _keyword_search_re(keywords, df, case_sensitive)
    else:
        dfres = _keyword_search_str(keywords, df, case_sensitive)

    if "detail" in return_data:
        df = dffull.join(dfres)
        zeroes = max(math.ceil(math.log10(len(keywords))), 2)
        list_hits = []
        for i, kw in enumerate(keywords):
            hit_field = "kw_match" + str.zfill(str(i + 1), zeroes)
            if labels:
                label = labels[i]
            else:
                label = kw
            dftemp = df[df[hit_field] == True][[key_column]].copy()
            dftemp["labels"] = label
            dftemp["keyword"] = kw
            list_hits.append(dftemp)
        dfd = pd.concat(list_hits)
        logger.info("Returning search hits details in %s rows", dfd.shape[0])
        return dfd

    if labels:
        if len(set(labels)) == len(dfres.columns):
            dfres.columns = labels
        else:
            # we are dealing with multiple labels to group
            dfresg = pd.DataFrame()
            for l in set(labels):
                cols = []
                for i, c in enumerate(dfres.columns):
                    if l == labels[i]:
                        cols.append(c)
                dfresg[l] = np.logical_or.reduce(dfres[cols], axis=1)
            dfres = dfresg.copy()

    # we add the combined any() (ie. or) column to dfres after we processed the
    # labels because otherwise the list of labels and hits wouldnt match
    dfres["kw_match_all"] = dfres.apply(any, axis=1)
    # we add a hit count column for convenience
    dfres["kw_match_count"] = dfres.apply(sum, axis=1)
    logger.info("Count of all hits: %s", dfres["kw_match_count"].sum())
    if "_hits" in return_data:
        dfres = dfres[dfres["kw_match_all"] == True].copy()
        logger.info("Returning just hit rows: %s", dfres.shape[0])

    if "full" in return_data:
        dffull = dffull.join(dfres, how="inner").copy()
        logger.info("Returning all columns %s", dffull.columns)
        return dffull

    if "result" in return_data:
        logger.info("Returning hit columns %s", dfres.columns)
        return dfres

    if "target" in return_data:
        df = df[columns].join(dfres, how="inner").copy()
        logger.info("Returning target columns: %s", df.columns)
        return df
