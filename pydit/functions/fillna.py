"""
Cleanup the dataframes improving over what fillna() does
"""

import logging
from datetime import datetime
import pandas as pd
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
    inplace=False
):
    """
    Cleanup the values of the dataframe with sensible nulls handling.
    
    Args:
        df (DataFrame): Input panda DataFrame
        cols (Optional, list): List of columns to be cleaned, if None, all are cleaned
        date_fillna ('latest','first' or datetime, optional): What to put in NaT values, 
            i.e. Takes the first, last or a specified date to fill the gaps. 
            Defaults to "latest".
        text_fillna (String, Optional, Defaults to ""): String to use to replace nan in 
        text/object columns
        inplace (bool, optional): If True, the dataframe is modified in place.

    Returns:
        DataFrame: Returns a copy of the original dataframe with modifications
        (or the modified original dataframe if inplace=True))        
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expecting a dataframe")
    if not inplace:
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
