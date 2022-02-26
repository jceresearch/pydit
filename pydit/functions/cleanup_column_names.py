""" Transform and Munging functions"""

import logging
from pydit.utils import deduplicate_list

logger = logging.getLogger(__name__)


def cleanup_column_names(df, max_field_name_len=40):
    """ Cleanup the column names of a Pandas dataframe
        e.g. removes non alphanumeric chars, _ instead of space, perc instead
        of %, strips trailing spaces, converts to lowercase
        """

    df.columns = df.columns.str.replace(r"%", "pc", regex=True)
    df.columns = df.columns.str.replace(r"[^a-zA-Z0-9]", " ", regex=True)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" +", "_", regex=True)
    df.columns = df.columns.str.lower()
    # arbitrary limit of field names to avoid some random issues with importing in
    # other systems, for example PowerBI has a limit of 80 charts for importing column
    # names, just in case keeping this quite low, feel free to increase or remove
    df.column = df.columns.str[0:max_field_name_len]
    new_cols = deduplicate_list(list(df.columns))
    df.columns = new_cols
    logger.info("New columns names:%s", list(df.columns))
    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicated column names remain!!! check what happened")
    return list(df.columns)
