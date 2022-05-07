""" Convenience functions"""
import random
import string
import logging
import socket
import warnings

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


def check_column_presence(
    df: pd.DataFrame, column_names: Union[Iterable, str], present: bool = True
):
    """
    One-liner syntactic sugar for checking the presence or absence
    of columns.

    Example usage:

    ```python
    check(df, ['a', 'b'], present=True)
    ```

    This will check whether columns `'a'` and `'b'` are present in
    `df`'s columns.

    One can also guarantee that `'a'` and `'b'` are not present
    by switching to `present=False`.

    :param df: The name of the variable.
    :param column_names: A list of column names we want to check to see if
        present (or absent) in `df`.
    :param present: If `True` (default), checks to see if all of `column_names`
        are in `df.columns`. If `False`, checks that none of `column_names` are
        in `df.columns`.
    :raises ValueError: if data is not the expected type.
    """
    if isinstance(column_names, str) or not isinstance(column_names, Iterable):
        column_names = [column_names]

    for column_name in column_names:
        if present and column_name not in df.columns:  # skipcq: PYL-R1720
            raise ValueError(f"{column_name} not present in dataframe columns!")
        elif not present and column_name in df.columns:
            raise ValueError(f"{column_name} already present in dataframe columns!")


def skipna(f: Callable) -> Callable:
    """
    Decorator for escaping `np.nan` and `None` in a function.

    Example usage:

    ```python
    df[column].apply(skipna(transform))

    # Can also be used as shown below
    @skipna
    def transform(x):
        pass
    ```

    :param f: the function to be wrapped.
    :returns: the wrapped function.
    """

    def _wrapped(x, *args, **kwargs):
        if (type(x) is float and np.isnan(x)) or x is None:
            return np.nan
        return f(x, *args, **kwargs)

    return _wrapped


def skiperror(f: Callable, return_x: bool = False, return_val=np.nan) -> Callable:
    """
    Decorator for escaping any error in a function.

    Example usage:

    ```python
    df[column].apply(
        skiperror(transform, return_val=3, return_x=False))

    # Can also be used as shown below
    @skiperror(return_val=3, return_x=False)
    def transform(x):
        pass
    ```
    :param f: the function to be wrapped.
    :param return_x: whether or not the original value that caused error
        should be returned.
    :param return_val: the value to be returned when an error hits.
        Ignored if `return_x` is `True`.
    :returns: the wrapped function.
    """

    def _wrapped(x, *args, **kwargs):
        try:
            return f(x, *args, **kwargs)
        except Exception:  # skipcq: PYL-W0703
            if return_x:
                return x
            return return_val

    return _wrapped


def is_connected(url: str) -> bool:
    """
    This is a helper function to check if the client
    is connected to the internet.

    Example:
        print(is_connected("www.google.com"))
        console >> True

    :param url: We take a test url to check if we are
        able to create a valid connection.
    :raises OSError: if connection to `URL` cannot be
        established
    :return: We return a boolean that signifies our
        connection to the internet
    """
    try:
        sock = socket.create_connection((url, 80))
        if sock is not None:
            sock.close()
            return True
    except OSError as e:

        warnings.warn(
            "There was an issue connecting to the internet. "
            "Please see original error below."
        )
        raise e
    return False
