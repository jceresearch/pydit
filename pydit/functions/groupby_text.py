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
    """Groupby text column into concatenated text, with extra smartness

    Args:
        df (DataFrame): _description_
        key_cols (list or str): key columns used for grouping
        value_cols (list or str or None, optional): Value colums to concatenate Defaults to None.
        target_col_name (str, optional): name for the resulting column. Defaults to "groupby_text".
        field_separator (str, optional): if multiple value_cols provided then how to concatenate. Defaults to " ".
        row_separator (str, optional): separator for the rows. Defaults to "\n".

    This function does not mutate the input dataframe.

    Returns:
        DataFrame: a grouped dataframe with the concatenated text
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
    elif isinstance(value_cols, str) and value_cols in df.columns:
        value_cols = [value_cols]
    elif isinstance(value_cols, list):
        if not set(value_cols).issubset(set(df.columns)):
            raise ValueError(f"One or more from {value_cols} not in dataframe")
    else:
        raise TypeError("text_cols must be a string or list of strings")

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
    # some examples of use, see the test suite for further details
    data = {
        "team": ["teamA", "teamA", "teamA", "teamA", "teamA", "teamB", "teamC"],
        "purid": ["P01", "P01", "P01", "P02", "P02", "P03", "P03"],
        "apprid": [1, 2, 3, 4, 5, 6, 7],
        "appr": ["ok", "ok", "rejected", "ok", " ", "Error", "ok",],
        "user": ["user1", "user2", "user1", "user2", "", np.nan, "user3"],
    }
    dftest = pd.DataFrame(data)
    df1 = groupby_text(dftest, "purid", value_cols=["appr", "user"])
    df2 = groupby_text(dftest, ["team", "purid"], value_cols=["apprid", "appr", "user"])
    df3 = groupby_text(dftest, ["team", "purid"], value_cols=["appr", "user"])
    df4 = groupby_text(dftest, ["team"], value_cols=["user"], row_separator=" ")
    df5 = groupby_text(
        dftest, ["team"], value_cols=["purid", "appr"], row_separator=" "
    )
    df6 = groupby_text(
        dftest, ["purid"], value_cols=["apprid", "appr"], row_separator="|"
    )
    df7 = groupby_text(dftest, "purid", value_cols="appr", row_separator="|")
    dflist = [df1, df2, df3, df4, df5, df6, df7]
    for df in dflist:
        print(df)
