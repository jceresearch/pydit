""" Groupby text column into concatenated text, with extra smartness """

import logging

import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)


def groupby_text(
    df,
    key_cols,
    value_cols=None,
    target_col_name="groupby_text",
    field_separator=" ",
    row_separator="\n",
):
    """
    Groupby text column into concatenated text, with extra smartness

    Parameters
    ----------

    df: DataFrame
        DataFrame to group
    key_cols: list or str
        key columns used for grouping
    value_cols: list or str or None, optional
        Value colums to concatenate
        Defaults to None.
    target_col_name: str, optional
        name for the resulting column.
        Defaults to "groupby_text".
    field_separator: str, optional
        if multiple value_cols provided then how to concatenate.
        Defaults to " ".
    row_separator: str, optional
        separator for the rows.
        Defaults to "\n".

    Returns
    -------

    DataFrame
        A grouped dataframe with the concatenated text
        This function does not mutate the input dataframe.

    Examples
    --------

    See Also
    --------




    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(key_cols, (list, str)):
        raise TypeError("key_cols must be a list or string")
    if isinstance(key_cols, str):
        key_cols = [key_cols]
    if not set(key_cols).issubset(set(df.columns)):
        raise ValueError(f"Key column {key_cols} not in dataframe")
    if value_cols is None:
        value_cols = [
            x for x in df.columns if x not in key_cols and df[x].dtype == "object"
        ]
        logger.info(
            "No value columns provided, using all object columns: %s", value_cols
        )
    elif isinstance(value_cols, str):
        if value_cols in df.columns:
            value_cols = [value_cols]
        else:
            raise ValueError(f"Value column {value_cols} not in dataframe")
    elif isinstance(value_cols, list):
        if not set(value_cols).issubset(set(df.columns)):
            raise ValueError(f"One or more from {value_cols} not in dataframe")
    else:
        raise TypeError("value_cols must be a string or list of strings")

    # pick just the columns we need, remove nans and conver to string
    df = (
        df[key_cols + value_cols].fillna("").astype(str).copy()
    )  # copy() to avoid mutating original df

    df = df.apply(lambda x: x.str.strip())  # remove leading and trailing whitespace
    # here we join the value columns if we need to
    joined_col = df[value_cols].stack().groupby(level=0).agg(field_separator.join)
    df = df.assign(**{target_col_name: joined_col})

    # here is where the true row concatenation happens, reset_index() makes in to a flat dataframe
    df_groupby = (
        df.groupby(key_cols)[target_col_name].apply(row_separator.join).reset_index()
    )
    # possibly not needed, but just in case we trim the whitespaces
    df_groupby[target_col_name] = df_groupby[target_col_name].str.strip()
    return df_groupby


if __name__ == "__main__":
    pass
