""" Module with utility functions for fuzzy matching"""

import string
import logging
from functools import lru_cache
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@lru_cache(maxsize=3000)
# we enable the caching in this small piece, maxsize can be set to None=unlimited,
# but we could add a limit , apparently having an actual limit makes it
# marginally faster in some conditions.


def token_set_sort(s=None):
    """Create a fuzzy key for a string using token set sort method
    set sort method is described here: https://en.wikipedia.org/wiki/Jaccard_index

    Parameters
    ----------
    s : str
        The string to create the fuzzy key from

    Returns
    -------
    str
        The fuzzy key

    """
    if s is np.nan:
        return ""
    if s is None:
        return ""
    s = str(s)
    if s == "" or str.strip(s) == "":
        return ""
    s = s.translate(str.maketrans("", "", string.punctuation))
    sl = list(set(str.split(s)))
    sl.sort()
    s = "".join(sl)
    return s


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
        df[input_col]
        .str.lower()
        .replace("'", "", regex=True)
        .replace(r"\s", " ", regex=True)
        .replace("", np.nan, regex=True)
    )
    # Now we are going to deal with non standar chars
    #
    # This version directly removes accented chars and spanish enie
    # df['fuzzy'] = df['fuzzy'].str.encode('ascii', 'ignore').str.decode('ascii')

    # This will also remove accented chars
    # from string import printable
    # st = set(printable)
    # df["fuzzy"] = df["fuzzy"].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))

    # This will retain the characters but standardise for compatibility, there are various
    # libraries that do that too. I would use other versions if performance is a concern
    df[output_col] = (
        df[output_col]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .replace("[^a-z1-9 &]", " ", regex=True)
        .replace(" (ltd|plc|inc|llp|limited)", " ", regex=True)
        .replace(" (&)", " and ", regex=True)
        .replace("(mr|mrs|miss) ", " ", regex=True)
        .replace(" +", " ", regex=True)
        .str.strip()
    )
    if not disable_set_sort:
        df[output_col] = df[output_col].apply(token_set_sort)
    if not inplace:
        return df
    return None
