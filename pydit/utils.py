""" Convenience functions
While these can be used within the pydit package, e.g. the logging or file manager module
we should not use them as imports in the functions, as we want those to be self standing.
The principle is that we could drop a particular function module to do an audit test and it would
work just fine, being simple and self contained enough to be understood and audited,
rather than relying on a complex set of imports, decorators and auxiliary functions.
I still want to keep the master copy of those functions here, with tests and documentation.
Because we would drop in the specific function module a copy at a point in time we need to somewhat keep version
control. Possibly he test suite for a particular function/module should include the tests for those auxiliary functions. 
Somewhat cumbersome but the idea is to make it easier for an auditor to use one specific module without having to
understand the entire works of the package if he/she chooses to.

"""

import random
import string
import logging

import re

import numpy as np


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


def check_types(varname: str, value, expected_types: list):
    """
    One-liner syntactic sugar for checking types.
    It can also check callables.

    Example usage:

    ```python
    check('x', x, [int, float])
    ```

    :param varname: The name of the variable (for diagnostic error message).
    :param value: The value of the `varname`.
    :param expected_types: The type(s) the item is expected to be.
    :raises TypeError: if data is not the expected type.
    """
    is_expected_type: bool = False
    for t in expected_types:
        if t is callable:
            is_expected_type = t(value)
        else:
            is_expected_type = isinstance(value, t)
        if is_expected_type:
            break

    if not is_expected_type:
        raise TypeError(
            "{varname} should be one of {expected_types}".format(
                varname=varname, expected_types=expected_types
            )
        )
