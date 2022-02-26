""" Convenience functions"""
import random
import string
import logging

import re
import numpy as np
import pandas as pd

logger = logging.getLogger()


def print_red(*args):
    """ print ansi codes to make the printout red"""
    print("\x1b[31m" + " ".join([str(x) for x in args]) + "\x1b[0m")


def print_green(*args):
    """ print ansi codes to make the printout green"""
    print("\x1b[32m" + " ".join([str(x) for x in args]) + "\x1b[0m")


def deduplicate_list(
    list_to_deduplicate, default_field_name="column", force_lower_case=True
):
    """deduplicates a list
    Uses enumerate and a loop, so it is not good for very long lists
    This function is for dealing with header/field names, where performance
    is not really an issue
    Returns a list of fields with no duplicates and suffixes where there were
    duplicates
    """

    def get_random_string(length):
        # choose from all letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    if not list_to_deduplicate:
        return []
    try:
        if force_lower_case:
            list_clean = [
                "" if pd.isna(x) else str.lower(str.strip(str(x)))
                for x in list_to_deduplicate
            ]
        else:
            list_clean = [
                "" if pd.isna(x) else str.strip(str(x)) for x in list_to_deduplicate
            ]
    except:
        logger.error("Unable to convert elements in the list to string type")
        return False
    new_list = []
    for i, el in enumerate(list_clean):
        if pd.isna(el) or el == "":
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
                new_value = el + "_" + get_random_string(4)
                if new_value in new_list:
                    new_value = el + "_" + get_random_string(8)
                    if new_value in new_list:
                        return False
        new_list.append(new_value)
    return new_list


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
