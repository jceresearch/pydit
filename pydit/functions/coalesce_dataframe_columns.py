"""Function for performing coalesce."""

import logging
from typing import Optional, Union
import pandas as pd

logger = logging.getLogger(__name__)


def coalesce_columns(
    df: pd.DataFrame,
    *column_names,
    target_column_name: Optional[str] = None,
    default_value: Optional[Union[int, float, str]] = None,
    operation=None,
    separator=" "
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
    operation : str, optional, "concatenate" or None, default None 
        If None, the values will be overwritten and the latest column will prevail
        If "concatenate", the values will be concatenated
    separator : str, optional, default " "
        The separator to use when concatenating values
    
    Returns
    -------
    pandas.DataFrame
        Pandas DataFrame with coalesced column.

"""

    # TODO: #33 coalesce_columns(): Check exactly how the overwrite works when operation is None and document in the help

    if not column_names:
        return df
    print(column_names)
    if len(column_names) < 2:
        if isinstance(column_names[0], list) and len(column_names[0]) > 1:
            column_names = column_names[0]
        else:
            raise ValueError(
                "The number of columns to coalesce should be a minimum of 2."
            )

    if isinstance(column_names, list) or isinstance(column_names, tuple):
        wrong_columns = [x for x in column_names if x not in df.columns]
        if wrong_columns:
            raise ValueError("Columns not in the dataframe:" + " ".join(wrong_columns))

    else:
        raise TypeError("Please provide a list of columns")

    if target_column_name:
        if not isinstance(target_column_name, str):
            raise TypeError("Please provide a string for the target column name")

    if default_value:
        if not isinstance(default_value, (int, float, str)):
            raise TypeError("Please provide a default value int, str or float")

    if target_column_name is None:
        target_column_name = column_names[0]
    print("Target column name:", target_column_name)
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
    if outcome.hasnans and (default_value is not None):
        outcome = outcome.fillna(default_value)
    return df.assign(**{target_column_name: outcome})
