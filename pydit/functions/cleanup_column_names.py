""" Transform and Munging functions"""

import logging

import re

from pydit.utils import deduplicate_list


logger = logging.getLogger(__name__)


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
            logger.exception("Problem converting header into str, leaving it blank")
            new = ""
        new = re.sub("%", "pc", new)
        new = re.sub(r"[^a-zA-Z0-9£$€]", " ", new)
        new = re.sub(" +", " ", new)
        new = new[0 : max_field_name_len ]
        new = str.lower(new.strip())
        new = re.sub(" +", "_", new)

        new_cols.append(new)
    # We apply arbitrary limit of field names to avoid some random issues with importing in
    # other systems, for example PowerBI has a limit of 80 charts for importing column
    # names, just in case keeping this quite low, feel free to increase or remove
    new_cols = deduplicate_list(new_cols)
    df.columns = new_cols
    logger.debug("Previous column names:%s", prev_cols)
    logger.info("New columns names:%s", list(df.columns))
    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicated column names remain!!! check what happened")
    return list(df.columns)
