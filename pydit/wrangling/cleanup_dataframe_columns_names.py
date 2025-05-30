"""Module for cleaning up column names of a DataFrame"""

import logging
import string
import re
import random
import unicodedata
import pandas as pd


logger = logging.getLogger(__name__)


def _strip_accents(text: str) -> str:
    """Remove accents from an unicode text.
    Inspired from [StackOverflow][so].
    [so]: https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-strin
    """  # noqa: E501

    return "".join(
        letter
        for letter in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(letter)
    )


def _deduplicate_list(
    list_to_deduplicate, default_field_name="column", case_insensitive=True
):
    """Internal function for deduplicating a list.

    Uses enumerate and a loop, so it is not good for very long lists.
    This function is meant to be used for header/field names, where performance
    is not a concern given the size of the list to deduplicate.

    This is a copy of the corresponding function in the utility module
    V0.1 - 14 May 2022

    Parameters
    -----------

    list_to_deduplicate : list
        The list to deduplicate
    default_field_name : str, optional, default "column"
        The default field name to use if the field is empty
    force_lower_case : bool, optional, default True
        If True, will convert the field name to lower case

    Returns
    -------
    list
        Returns a list of fields with no duplicates and suffixes where there were duplicates.


    """

    def _get_random_string(length):
        # choose from all letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    if not list_to_deduplicate:
        return []
    try:
        if case_insensitive:
            list_clean = [
                (
                    str.lower(str.strip(str(x)))
                    if isinstance(x, str) or isinstance(x, int)
                    else ""
                )
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
                        raise ValueError(
                            "Failed to create a unique value, failed at: " + new_value
                        )
        new_list.append(new_value)
    return new_list


def cleanup_column_names(
    obj,
    max_field_name_len=40,
    silent=False,
):
    """Cleanup the column names of a Pandas dataframe.

    e.g. removes non alphanumeric chars, replaces _ instead of space, perc instead
    of %, converts main currency signs (usd, gpb, eur), strips trailing spaces,
    converts to lowercase.



    It also ensures that the resulting list doesn't have duplicates or nulls, in
    which case it would fix.

    Parameters
    ----------
    obj : pandas.DataFrame or list of strings or string
        The dataframe or a list of strings, or a string to clean up.
    max_field_name_len : int, optional, default 40
        The maximum length of the field name

    Returns
    -------
    pandas.DataFrame
        A copy of the pandas DataFrame with cleaned column names

    list
        A copy of the list of strings with cleaned column names if the input was a list

    str
        A cleaned string if the input was a sole string. Note that if you provided
        a single element list it will still return a list of one element.

    """
    if isinstance(obj, list):
        prev_cols = obj.copy()
    elif isinstance(obj, pd.DataFrame):
        prev_cols = list(obj.columns)
    elif isinstance(obj, str):
        prev_cols = [obj]
    else:
        raise ValueError(
            "obj must be a pandas DataFrame or a list of strings, or a string"
        )

    if len(prev_cols) != len(set(prev_cols)):
        logger.warning(
            "Input list has duplicates, the result will be deduplicated but "
            "check if that was expected: %s",
            prev_cols,
        )

    new_cols = []
    for e in prev_cols:
        try:
            new = str(e)
        except Exception as e:
            logger.exception(e)
            new = "unnamed"
            continue
        new = _strip_accents(new)
        new = re.sub("%", "pc", new)
        new = re.sub("£", "gbp", new)
        new = re.sub(r"\$", "usd", new)
        new = re.sub("€", "eur", new)
        new = re.sub(r"[^a-zA-Z0-9]", " ", new)
        new = re.sub(" +", " ", new)
        new = new[0:max_field_name_len]
        new = str.lower(new.strip())
        new = re.sub(" +", "_", new)

        new_cols.append(new)
    # We apply arbitrary limit of field names to avoid some random issues with importing in
    # other systems, for example PowerBI has a limit of 80 charts for importing column
    # names, just in case keeping this quite low, feel free to increase or remove
    new_cols = _deduplicate_list(new_cols)

    if len(new_cols) != len(set(new_cols)):
        raise ValueError(f"Duplicated column names!!! check: {new_cols}")
    if not silent:
        logger.debug("Previous names:%s", prev_cols)
        logger.info("New names:%s", list(new_cols))
    if isinstance(obj, str):
        return new_cols[0]
    if isinstance(obj, list):
        return new_cols
    if isinstance(obj, pd.DataFrame):
        obj = obj.copy()
        obj.columns = new_cols
        return obj
