"""Cleanup the dataframes wrapping around and improving on fillna().

"""

import logging
from datetime import datetime, date
import pandas as pd
import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime

logger = logging.getLogger(__name__)


def fillna_smart(
    df,
    cols=None,
    numeric_fillna=0,
    date_fillna="latest",
    text_fillna="",
    include_empty_string=False,
    include_spaces=False,
    inplace=False,
):
    """Cleanup the values of the dataframe with sensible nulls handling.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to clean up
    cols : list, optional, default None
        The columns to clean up. If None, will clean up all columns.
    numeric_fillna : int, optional, default 0
        The value to fill in for int columns.
    date_fillna : str or datetime or date, optional, default "latest"
        The date to use for the nulls in the date columns.
        If "latest", will use the latest date in the column.
        If "first", will use the minimum date in the column.
        if "today", will use today's date.
        If date or datetime, will use that date.
        If str, will attempt to parse the date using "%Y-%m-%d" format.
    text_fillna : str, optional, default ""
        The text to use for the nulls in the text columns.
    inplace: bool, optional, default False
        If True, the dataframe is modified in place.

    Returns
    -------
    pandas.DataFrame
        Returns a copy of the original dataframe with modifications

    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expecting a dataframe")
    if not inplace:
        df = df.copy(deep=True)
    if cols is None:
        cols = df.columns
    else:
        if not set(cols).issubset(set(df.columns)):
            raise ValueError("Columns not in dataframe")
        else:
            cols = list(set(cols))

    dtypes = df.dtypes.to_dict()
    for col, typ in dtypes.items():
        if col not in cols:
            # we skip this column
            continue
        if ("int" in str(typ)) or ("float" in str(typ)):
            df[col].fillna(numeric_fillna, inplace=True)
        elif is_datetime(df[col]):
            if date_fillna == "latest":
                val = max(df[col])
                # TODO: fillna_smart() add support for first/last date across all date columns.
            elif date_fillna == "first":
                val = min(df[col])
            elif date_fillna == "today":
                val = date.today()
            elif isinstance(date_fillna, (datetime, date)):
                val = date_fillna
            elif isinstance(date_fillna, str):
                try:
                    val = datetime.strptime(date_fillna, "%Y-%m-%d")
                except:
                    raise ValueError(
                        "Could not parse date_fillna parameter %s", date_fillna
                    )
            else:
                val = pd.NaT
                raise ValueError("date_fillna is not a valid input: %s", date_fillna)
            df[col].fillna(val, inplace=True)
        elif typ == "object":
            if not isinstance(text_fillna, str):
                raise ValueError(
                    "text_fillna needs to be a string, provided: %s", text_fillna
                )
            if include_empty_string:
                df[col] = df[col].replace("", np.nan)
            if include_spaces:
                df[col] = (
                    df[col]
                    .apply(lambda x: x.strip() if isinstance(x, str) else x)
                    .replace("", np.nan)
                )

            df[col].fillna(text_fillna, inplace=True)
        if inplace:
            return True
    return df
