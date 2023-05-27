"""Utility functions, they are not used directly in the core functions.

The functions below can be used directly.
However, when needed for a specific core function, instead of importing them, 
we would create a copy of the function and rename it with an _ prefix.
This is to ensure that a core function's module is self-standing, ie can be
used/imported with no other dependencies.

"""
import random
import string
import logging
import re
from datetime import datetime
import unicodedata
import pandas as pd
import numpy as np
import math

# pylint: disable=W0702
# pylint: disable=W0613

logger = logging.getLogger()


def print_red(*args):
    """print ansi codes to make the printout red"""
    print("\x1b[31m" + " ".join([str(x) for x in args]) + "\x1b[0m")


def print_green(*args):
    """print ansi codes to make the printout green"""
    print("\x1b[32m" + " ".join([str(x) for x in args]) + "\x1b[0m")


def deduplicate_list(
    list_to_deduplicate, default_field_name="column", force_lower_case=True
):
    """Deduplicates a list

    Uses enumerate and a loop, so it is not good for very long lists
    This function is for dealing with header/field names, where performance
    is not really an issue



    Returns a list of fields with no duplicates and suffixes where there were
    duplicates
    V0.1 - 14 May 2022
    """

    def _get_random_string(length):
        # choose from all letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    if not list_to_deduplicate:
        return []
    try:
        if force_lower_case:
            list_clean = [
                str.lower(str.strip(str(x)))
                if isinstance(x, str) or isinstance(x, int)
                else ""
                for x in list_to_deduplicate
            ]
        else:
            list_clean = [
                str.strip(str(x)) if isinstance(x, str) or isinstance(x, int) else ""
                for x in list_to_deduplicate
            ]
    except Exception as e:
        logger.error(e)
        return False
    new_list = []
    for i, el in enumerate(list_clean):
        if el == "":
            new_value = default_field_name + "_" + str(i + 1)
        else:
            if el in new_list:
                new_value = el + "_2"
            else:
                new_list.append(el)
                continue
        if new_value in new_list:
            n = 2
            while el + "_" + str(n) in new_list and n < 10000:
                n = n + 1
            new_value = el + "_" + str(n)
            if new_value in new_list:
                new_value = el + "_" + _get_random_string(4)
                if new_value in new_list:
                    new_value = el + "_" + _get_random_string(8)
                    if new_value in new_list:
                        return False
        new_list.append(new_value)
    return new_list


def dataframe_to_code(df):
    """Convert a dataframe to source code that one can include in a test script or tutorial.

    May need extra tweaks or imports, e.g. from pandas import Timestamp to deal with dates, etc.


    """
    data = np.array2string(df.to_numpy(), separator=", ")
    data = data.replace(" nan", " float('nan')")
    data = data.replace(" NaT", " pd.NaT")
    cols = df.columns.tolist()
    return f"""df = pd.DataFrame({data}, columns={cols})"""


def clean_string(
    t=None,
    keep_dot=False,
    keep_dash=False,
    keep_apostrophe=False,
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
    r = re.sub(r"[^a-zA-Z0-9\.\-']", " ", r)
    r = r.strip()
    if space_to_underscore:
        r = re.sub(" +", "_", r)
    else:
        r = re.sub(" +", " ", r)
    return r


def create_test_dataframe(dataset_name: str, n_rows: int = 10, n_cols: int = 10):
    """Create test dataframes

    IMPORTANT these are NOT to be used for the core test suite.
    These are meant for the examples and for users to play, tutorials etc.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset
        One of: random_numeric, random_categorical, dataset_01
    n_rows : int, optional, default 10
        Number of rows in the dataframe
    n_cols : int, optional, default 10
        Number of columns in the dataframe

    Returns
    -------
    pd.DataFrame
        A test dataframe

    """

    if dataset_name == "random_numeric":
        df = pd.DataFrame(
            np.random.randn(n_rows, n_cols),
            columns=["col" + str(x) for x in range(1, n_cols + 1)],
        )
        return df
    elif dataset_name == "random_categorical":
        df = pd.DataFrame(
            np.random.randint(0, 10, (n_rows, n_cols)),
            columns=["col" + str(x) for x in range(1, n_cols + 1)],
        )
        return df
    elif dataset_name == "dataset_01":
        yyyy = datetime.now().year

        data = {
            "col1": ["january", "february", "march", "april", "may", "june"],
            "col2": ["Jan", "Feb", "Mar", "Apr", np.nan, 0],
            "col3": [1, 2, 3, 4, 5, 6],
            "col4": [
                datetime(yyyy, 1, 1),
                datetime(yyyy, 2, 1),
                datetime(yyyy, 3, 1),
                datetime(yyyy, 4, 1),
                datetime(yyyy, 5, 1),
                datetime(yyyy, 6, 1),
            ],
            "col5": [423.34, 120.01, 123.45, 12.34, 9.45, 12.00],
        }
        df = pd.DataFrame(data)
        return df
