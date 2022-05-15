""" Transform and Munging functions"""

import logging
from datetime import datetime

import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime


logger = logging.getLogger(__name__)


def fillna_smart(
    df,
    cols=None,
    date_fillna="latest",
    text_fillna="",
    include_empty_string=False,
    include_spaces=False,
):
    """Cleanup the actual values of the dataframe with sensible
    nulls handling.

    Args:
        df (DataFrame): Input panda DataFrame
        cols (Optional, list): List of columns to be cleaned, if None all are cleaned
        date_fillna ('latest','first' or datetime, optional): What to put in NaT values, 
            takes the first, last or a specified date to fill the gaps. Defaults to "latest".
        text_fillna (String, Optional, Defaults to ""): String to use to replace nan in text/object columns

    Returns:
        DataFrame: Returns a copy of the original dataframe with modifications
        Beware if the dataframe is large you may have memory issues.
    """
    df = df.copy(deep=True)
    if cols is None:
        cols = df.columns
    else:
        if not set(cols).issubset(set(df.columns)):
            logger.error("Columns provided are not in the dataframe")
            return df
        else:
            cols = list(set(cols))

    dtypes = df.dtypes.to_dict()
    for col, typ in dtypes.items():
        if col not in cols:
            # we skip this column
            continue
        if ("int" in str(typ)) or ("float" in str(typ)):
            df[col].fillna(0, inplace=True)
        elif is_datetime(df[col]):
            if date_fillna == "latest":
                val = max(df[col])
            elif date_fillna == "first":
                val = min(df[col])
            elif isinstance(date_fillna, datetime):
                val = date_fillna
            df[col].fillna(val, inplace=True)
        elif typ == "object":
            if include_empty_string:
                df[col] = df[col].replace("", np.nan)
            if include_spaces:
                df[col] = (
                    df[col]
                    .apply(lambda x: x.strip() if isinstance(x, str) else x)
                    .replace("", np.nan)
                )
            df[col].fillna(text_fillna, inplace=True)
    return df
