""" Transform and Munging functions"""

import logging
import string
import re
import random
import string


logger = logging.getLogger(__name__)


def _deduplicate_list(
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


def cleanup_column_names(df, max_field_name_len=40):
    """ Cleanup the column names of a Pandas dataframe
        e.g. removes non alphanumeric chars, _ instead of space, perc instead
        of %, strips trailing spaces, converts to lowercase
        """
    prev_cols = list(df.columns)
    new_cols = []
    for e in prev_cols:
        try:
            new = str(e)
        except Exception as e:
            logger.exception(e)
            new = ""
        new = re.sub("%", "pc", new)
        new = re.sub(r"[^a-zA-Z0-9£$€]", " ", new)
        new = re.sub(" +", " ", new)
        new = new[0:max_field_name_len]
        new = str.lower(new.strip())
        new = re.sub(" +", "_", new)

        new_cols.append(new)
    # We apply arbitrary limit of field names to avoid some random issues with importing in
    # other systems, for example PowerBI has a limit of 80 charts for importing column
    # names, just in case keeping this quite low, feel free to increase or remove
    new_cols = _deduplicate_list(new_cols)
    df.columns = new_cols
    logger.debug("Previous column names:%s", prev_cols)
    logger.info("New columns names:%s", list(df.columns))
    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicated column names remain!!! check what happened")
    return list(df.columns)
