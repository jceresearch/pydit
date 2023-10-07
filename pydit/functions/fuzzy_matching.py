""" Module with utility functions for fuzzy matching"""

import string
import logging
from functools import lru_cache
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)



def clean_string(
    t=None,
    keep_dot=False,
    keep_dash=False,
    keep_apostrophe=False,
    keep_ampersand=False,
    space_to_underscore=True,
    to_case="lower",
):
    """Sanitising a string

    Cleans the strings applying the following transformations:
    - Normalises unicode to remove accents and other symbols
    - Keeps only [a-zA-Z0-9]
    - Optional to retain dot
    - Spaces to underscore
    - Removes multiple spaces, strips
    - Optional to lowercase

    This is a naive/slow implementation, useful for sanitising things like
    a filename or column headers or small datasets. If you need to cleanup
    large datasets, you need to look into pandas/numpy tools, and vectorised
    functions.


    Parameters
    ----------
    t : str
        String to clean
    keep_dot : bool, optional, default False
        Whether to keep the dot in the string
    keep_dash : bool, optional, default False
        Whether to keep the dash in the string (useful for names)
    keep_aphostrophe : bool, optional, default False
        Whether to keep the apostrophe in the string (useful for names)
    keep_ampersand : True, False, "expand", default False
        Whether to keep the & or not, or expand to "and" 
    space_to_underscore : bool, optional, default True
        Whether to replace spaces with underscores
    case : str, optional, default "lower", choices=["lower", "upper"]
        Whether to lowercase the string

    Returns
    -------
    str
        Cleaned string

    """
    if t != t or t is None:
        return ""

    try:
        t = str(t)
    except Exception as e:
        return ""

    # we are going to normalize using NFKD
    # this will convert characters to their closest ASCII equivalent
    # e.g. é will become e
    # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    r = (
        unicodedata.normalize("NFKD", t)
        .encode("ascii", errors="ignore")
        .decode("utf-8")
    )
    if to_case == "lower":
        r = str.lower(r)
    elif to_case == "upper":
        r = str.upper(r)
    else:
        pass

    if not keep_dot:
        r = re.sub(r"[\.]", " ", r)
    if not keep_dash:
        r = re.sub(r"[-]", " ", r)
    if not keep_apostrophe:
        r = re.sub(r"[']", " ", r)
    if not keep_ampersand:
        r = re.sub(r"[&]"," ",r)
    elif keep_ampersand=="expand":
        r = re.sub(r"[&]","and",r)
    r = re.sub(r"[^a-zA-Z0-9\.\-\&']", " ", r)
    r = r.strip()
    if space_to_underscore:
        r = re.sub(" +", "_", r)
    else:
        r = re.sub(" +", " ", r)
    return r


# we enable the caching in this small piece, maxsize can be set to None=unlimited,
# but we could add a limit , apparently having an actual limit makes it
# marginally faster in some conditions.


def create_fuzzy_key(
    df, input_col, output_col="fuzzy_key", disable_set_sort=False, inplace=False
):
    """
    Create a fuzzy key for a dataframe

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to create the fuzzy key for
    input_col : str
        The column to create the fuzzy key from
    output_col : str, optional
        The column to create the fuzzy key to, by default "fuzzy_key"
    disable_set_sort : bool, optional
        Whether to disable the set sort method, by default False. This is faster
        and should be used if we are going to feed into a fuzzy matching algorithm
        that already does it (like fuzzywuzzy or similar)
    inplace : bool, optional
        Whether to create the fuzzy key inplace or not, by default False

    Returns
    -------
        pandas.Series
            The fuzzy key

    """

    if not inplace:
        df = df.copy()

    # First we are going to deal with the new lines and tabs and empty strings
    df[output_col] = (
        df[input_col].fillna("")
    )
    df[output_col] = (
        df[output_col]
        .replace(" (ltd|plc|inc|llp|limited)", " ", regex=True)
        .replace("(mr|mrs|miss) ", " ", regex=True)
        .replace(" +", " ", regex=True)
        .str.strip()
    )
    if not disable_set_sort:
        df[output_col] = df[output_col].apply(token_set_sort)
    if not inplace:
        return df
    return None
