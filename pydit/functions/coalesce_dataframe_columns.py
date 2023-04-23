"""Function for performing coalesce."""

import logging
from typing import Optional, Union
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def coalesce_columns(
    df: pd.DataFrame,
    *column_names,
    target_column_name: Optional[str] = None,
    default_value: Optional[Union[int, float, str]] = None,
    operation=None,
    separator=" ",
    silent: bool = False,
) -> pd.DataFrame:
    """Coalesce columns.

    Coalesce columns together.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to clean up
    *column_names : str
        The column names to coalesce
    target_column_name : str, optional, default None
        The name of the column to store the coalesced values in.
        If None, the values will be stored in the first column.
    default_value : int, float, str, optional, default None
        The default value to use if the target column is empty.
    operation : str, optional, "concatenate","last" or None, default None
        If None, the first non nan value will prevail, from left to right,
        ignoring the rest of the row.
        If "concatenate", all values will be converted to text and concatenated
        together, nans will be replaced with nullstring.
        If "last", the last non nan value will prevail, from right to left,
    separator : str, optional, default " "
        The separator to use when concatenating values
    silent : bool, optional, default False
        If True, suppress logging output

    Returns
    -------
    pandas.DataFrame
        Pandas DataFrame with coalesced column.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Please provide a pandas DataFrame")

    if not column_names:
        raise ValueError("Please provide at least one column name")

    if isinstance(column_names[0], list) and len(column_names) == 1:
        # if we provide a list insteand of consecutive arguments
        try:
            column_names = column_names[0]
        except Exception as exc:
            raise ValueError("Empty list of columns provided") from exc
    if isinstance(column_names, list) or isinstance(column_names, tuple):
        unmatched_columns = [x for x in column_names if x not in df.columns]
        matched_columns = [x for x in column_names if x in df.columns]
        if len(unmatched_columns) > 0:
            logger.warning("Some columns names provided are not in the dataframe")
        if len(matched_columns) == 0:
            raise ValueError("No columns provided are in the dataframe")
        column_names = matched_columns.copy()
    else:
        raise ValueError("Please provide a list of columns")

    if target_column_name is None:
        target_column_name = column_names[0]
    else:
        if not isinstance(target_column_name, str):
            raise TypeError("Please provide a string for the target column name")

    if default_value:
        if not isinstance(default_value, (int, float, str)):
            raise TypeError("Please provide a default value int, str or float")
    if not silent:
        logger.info("Coalescing columns: %s", " ".join([str(c) for c in column_names]))
        logger.info("Target column name: %s", target_column_name)
        logger.info("Default value: %s", default_value)
        logger.info("Operation: %s", operation)

    # bfill/ffill combo is faster than combine_first
    if operation is None:
        outcome = (
            df.filter(column_names)
            .bfill(axis="columns")
            .ffill(axis="columns")
            .iloc[:, 0]
        )
    elif operation == "concatenate":
        if default_value is None:
            fillna_value = ""
        else:
            fillna_value = default_value
        dftemp = df[column_names].fillna(fillna_value).astype("str", copy=True)
        outcome = dftemp.T.agg(separator.join)
    elif operation == "last":
        outcome = df[column_names].apply(lambda r: r[r.last_valid_index()], axis=1)
    if outcome.hasnans and (default_value is not None):
        outcome = outcome.fillna(default_value)
    return df.assign(**{target_column_name: outcome})
