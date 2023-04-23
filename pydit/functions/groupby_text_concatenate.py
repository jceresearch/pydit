"""Groupby text column into concatenated text
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def groupby_text(
    df,
    key_cols,
    value_cols=None,
    target_col_name="groupby_text",
    field_separator=" ",
    row_separator="\n",
    unique=False,
):
    """Groupby text column into concatenated text

    Parameters
    ----------
    df : DataFrame
        Pandas DataFrame to apply the function to
    key_cols : list or str
        Key columns used for grouping
    value_cols : list or str or None, optional, default None
        Value colums to concatenate.
    target_col_name : str, optional, default "groupby_text"
        Name for the resulting column.
    field_separator : str, optional, default " "
        If multiple value_cols provided then how to concatenate.
    row_separator : str, optional, default newline
        Separator for the rows.
    unique : bool, optional, default False
        If True, concatenate only unique values.


    Returns
    -------
    DataFrame
        A grouped dataframe with the concatenated text.

        This function does not mutate the input dataframe.

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
        logger.debug("No value columns provided, using all columns: %s", value_cols)
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

    # pick just the columns we need, remove nans and convert to string
    dfkeys = df[key_cols].copy()
    dfvalues = df[value_cols].fillna("").astype(str).copy()
    dfvalues = dfvalues.apply(
        lambda x: x.str.strip()
    )  # remove leading and trailing whitespace
    # here we join the value columns if we need to
    if len(dfvalues.columns) > 1:
        dfvalues = dfvalues.apply(lambda x: str.strip(field_separator.join(x)), axis=1)
        # dfvalues = dfvalues.stack().groupby(level=0).agg(field_separator.join)

    dfjoined = dfkeys.assign(**{target_col_name: dfvalues})

    # here is where the true row concatenation happens, reset_index() makes in to a flat dataframe
    if unique:
        df_groupby = (
            dfjoined.groupby(key_cols)[target_col_name]
            .apply(set)
            .apply(lambda s: row_separator.join(sorted(list(s))))
            .reset_index()
        )

    else:
        df_groupby = (
            dfjoined.groupby(key_cols)[target_col_name]
            .apply(row_separator.join)
            .reset_index()
        )

    # possibly not needed, but just in case we trim the whitespaces
    df_groupby[target_col_name] = df_groupby[target_col_name].str.strip()
    return df_groupby


if __name__ == "__main__":
    pass
