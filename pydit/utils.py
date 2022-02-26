""" Convenience functions"""

import re
import numpy as np


def print_red(*args):
    """ print ansi codes to make the printout red"""
    print("\x1b[31m" + " ".join([str(x) for x in args]) + "\x1b[0m")


def print_green(*args):
    """ print ansi codes to make the printout green"""
    print("\x1b[32m" + " ".join([str(x) for x in args]) + "\x1b[0m")


def deduplicate_list(list_to_deduplicate):
    "Deduplicates a list"
    if not list_to_deduplicate:
        return []
    newlist = list_to_deduplicate.copy()
    for i, el in enumerate(list_to_deduplicate):
        dupes = list_to_deduplicate.count(el)
        if dupes > 1:
            for j in range(dupes):
                pos = [i for i, n in enumerate(list_to_deduplicate) if n == el][j]
                if j == 0:
                    newlist[pos] = str(el)
                else:
                    newlist[pos] = str(el) + "_" + str(j + 1)
        else:
            newlist[i] = str(el)
    return newlist


def version():
    """ version information"""
    return "V.01"


def about():
    """ About information"""
    about_text = "Pydit - Tools for internal auditors\n \
    Version: 1.01\n \
    Released:Jan 2022 "
    return about_text


def dataframe_to_code(df):
    """ utility function to convert a dataframe to a piece of code
    that one can include in a test script or tutorial. May need extra tweaks
    or imports , e.g. from pandas import Timestamp to deal with dates, etc.
    """
    data = np.array2string(df.to_numpy(), separator=", ")
    data = data.replace(" nan", " float('nan')")
    data = data.replace(" NaT", " pd.NaT")
    cols = df.columns.tolist()
    return f"""df = pd.DataFrame({data}, columns={cols})"""


def clean_string(t, keep_dot=False, space_to_underscore=True, case="lower"):
    """Sanitising text:
    - Keeps only [a-zA-Z0-9]
    - Optional to retain dot
    - Spaces to underscore
    - Removes multiple spaces , trims
    - Optional to lowercase
    The purpose is just for easier typing, exporting, saving to filenames.
    Args:
        t (string]): string with the text to sanitise
        keep_dot (bool, optional): Keep the dot or not. Defaults to False.
        space_to_underscore (bool, optional): False to keep spaces. Defaults to True.
        case= "lower" (default), "upper" or "keep"(unchanged)
    Returns:
        string: cleanup string
    """
    r = ""
    if case == "lower":
        r = str.lower(str(t))
    elif case == "upper":
        str.upper(str(t))
    elif case == "keep":
        r = str(t)
    if t:
        if keep_dot is True:
            r = re.sub(r"[^a-zA-Z0-9.]", " ", r)
        else:
            r = re.sub(r"[^a-zA-Z0-9]", " ", r)
        r = r.strip()
        if space_to_underscore is True:
            r = re.sub(" +", "_", r)
        else:
            r = re.sub(" +", " ", r)
    return r
