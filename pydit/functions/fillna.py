"""Improving on fillna() with customaisable options for various types and opinionated defaults.

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
    """Cleanup the values of the dataframe with opinionated nulls handling.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to clean up
    cols : list, optional, default None
        The columns to clean up. If None, will clean up all columns.
    numeric_fillna : int/float, optional, default 0
        The value to fill in for numeric columns.
    date_fillna : str or datetime or date, optional, default "latest"
        The date to use for the nulls in the date columns.
        If "latest", will use the latest date in the column.
        If "first", will use the minimum date in the column.
        if "today", will use today's date.
        If date or datetime provided, will use that date.
        If str, will attempt to parse the date using "%Y-%m-%d" format.
    text_fillna : str, optional, default ""
        The text to use for the nulls in the text columns.
    include_empty_string : bool, optional, default False
        Whether to consider empty string as nulls to fill.
    include_spaces : bool, optional, default False
        Whether to consider spaces as nulls to fill.
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

    logger.info("Filling nulls in columns: {}".format(cols))
    if include_empty_string:
        logger.info("Will consider empty string as null")
    if include_spaces:
        logger.info("Will consider spaces as null")

    # Quick check of nans that will be filled
    na_counts = dict(df[cols].isnull().sum())
    logger.info("Quick check of nulls:")
    for c in na_counts.keys():
        logger.info("{} has {} nulls".format(c, na_counts[c]))

    dtypes = df.dtypes.to_dict()
    for col, typ in dtypes.items():
        if col not in cols:
            # we skip this column
            continue

        if ("int" in str(typ)) or ("float" in str(typ)):
            df[col].fillna(numeric_fillna, inplace=True)
            logger.info(
                "Filling nulls in numeric column {} with {}".format(col, numeric_fillna)
            )
        elif is_datetime(df[col]):
            if date_fillna == "latest":
                val = max(df[col])
            elif date_fillna == "first":
                val = min(df[col])
            elif date_fillna == "today":
                val = date.today()
            elif isinstance(date_fillna, (datetime, date)):
                val = date_fillna
            elif isinstance(date_fillna, str):
                try:
                    val = datetime.strptime(date_fillna, "%Y-%m-%d")
                except Exception as e:
                    raise ValueError(
                        "Could not parse date_fillna parameter, expected Y-m-d and provided %s"
                        % date_fillna
                    ) from e
            else:
                val = pd.NaT
            logger.info(
                "Filling nulls in datetime column {} with {} : {} ".format(
                    col, date_fillna, val
                )
            )
            df[col].fillna(val, inplace=True)
        elif typ == "object":
            if not isinstance(text_fillna, str):
                raise ValueError(
                    "text_fillna needs to be a string, provided: %s" % text_fillna
                )
            if include_empty_string:
                df[col] = df[col].replace("", np.nan)
            if include_spaces:
                df[col] = (
                    df[col]
                    .apply(lambda x: x.strip() if isinstance(x, str) else x)
                    .replace("", np.nan)
                )
            logger.info(
                "Filling nulls in object/text type column {} with {}".format(
                    col, text_fillna
                )
            )
            df[col].fillna(text_fillna, inplace=True)
        if inplace:
            return True
    return df
