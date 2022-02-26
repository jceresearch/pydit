""" Transform and Munging functions"""

import logging
from datetime import datetime

import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime


logger = logging.getLogger(__name__)


def fillna_smart(df, date_fillna="latest"):
    """Cleanup the actual values of the dataframe with sensible
    nulls handling.

    Args:
        df ([type]): Input DataFrame
        date_fillna ('latest','first' or datetime, optional):
        What to put in NaT values, takes the first, last or a specified
        date to fill the gaps.
        Defaults to "latest".

    Returns:
        DataFrame: Returns copy of the original dataframe with modifications
        Beware if the dataframe is large you may have memory issues.
    """

    df = df.copy(deep=True)
    dtypes = df.dtypes.to_dict()
    for col, typ in dtypes.items():
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
            df[col].fillna("", inplace=True)
    return df
