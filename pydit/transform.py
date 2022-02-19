""" Transform and Munging functions"""

import logging
from datetime import datetime

import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pydit import common

logger = logging.getLogger(__name__)


def clean_columns_names(df, max_field_name_len=40):
    """ Cleanup the column names of a Pandas dataframe
        e.g. removes non alphanumeric chars, _ instead of space, perc instead
        of %, strips trailing spaces, converts to lowercase
        """
    df.columns = df.columns.str.replace(r"%", "pc", regex=True)
    df.columns = df.columns.str.replace(r"[^a-zA-Z0-9]", " ", regex=True)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" +", "_", regex=True)
    df.columns = df.columns.str.lower()
    # arbitrary limit of field names to avoid some random issues with importing in
    # other systems, for example PowerBI has a limit of 80 charts for importing column
    # names, just in case keeping this quite low, feel free to increase or remove
    df.column = df.columns.str[0:max_field_name_len]
    if len(df.columns) != len(set(df.columns)):
        print("Identified some duplicate columns, renaming them")
        new_cols = common.deduplicate_list(list(df.columns))
        df.columns = new_cols

    logger.info("New columns names:%s", list(df.columns))
    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicated column names remain!!! check what happened")

    return list(df.columns)


def clean_cols(in_df, date_fillna="latest"):
    """Cleanup the actual values of the dataframe with sensible
    nulls handling.

    Args:
        in_df ([type]): Input DataFrame
        date_fillna ('latest','first' or datetime, optional):
        What to put in NaT values, takes the first, last or a specified
        date to fill the gaps.
        Defaults to "latest".

    Returns:
        DataFrame: Returns copy of the original dataframe with modifications
        Beware if the dataframe is large you may have memory issues.
    """

    df = in_df.copy()
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


def group_categories(
    df_in, cols, top_n_values_to_keep=0, translation_dict=None, other_label="OTHER"
):
    """Creates a new column with a translation of the top N most frequent values
    and the rest are replaced by Other.
    Also can take a translation dictionary to do the manual translation prior
    to applying that top N limit.
    Returns a copy of the DataFrame with the new column
    
    Args:
        df_in (DataFrame): Pandas DataFrame to transform
        
        cols (Str or List): Column or list of columns to apply the selection
        
        top_n_values_to_keep (int, optional): Top frequent categories to keep. 
        Defaults to 0 (means that all categories are kept. Useful if we provided
        a translation dictionary to keep all the translated values with no further 
        consolidation.
        
        translation_dict (dict, optional): Key>Value dictionary with the 
        translation from original category to desired category. 
        Defaults to None.
        
        other_label (string,optional): What to put on the other categories.
        Defaults to "OTHER"
        
        Example:
        translation={"OPEN":"OPEN","PENDING":"OPEN","Completed":"COMPLETED","CLOSED":"CLOSED"}
        df=group_categories(df_in=dfraw, 
        cols=["status"],t
        op_n_values_to_keep=2,
        translation_dict=translation
        )

    Returns:
        DataFrame: Copy of the original Pandas DataFrame with the extra columns
    """

    df = df_in.copy()
    if isinstance(cols, str):
        if not cols in df.columns:
            return "Not found"
        else:
            col = cols
    else:
        if not isinstance(cols, list):
            return "Please provide a list or a string"

        check = all(item in df.columns for item in cols)
        if not check:
            return "not all columns provided are in the dataframe, check for typos"
        if len(cols) == 1:
            col = cols[0]
        elif len(cols) > 1:

            def concat_categories(r, cols):
                try:
                    v = "_".join([str(v) for v in r[cols].values])
                except:
                    v = np.NAN
                return v

            col = "_".join(cols)
            df[col] = df.apply(lambda r: concat_categories(r, cols), axis=1)

        else:
            return "empty list"

    if translation_dict:
        df[col + "_translate"] = df.apply(
            lambda r: translation_dict[r[col]]
            if r[col] in translation_dict
            else other_label,
            axis=1,
        )
        col = col + "_translate"

    if top_n_values_to_keep > 0:
        print(col)
        print(df[col].value_counts())
        value_counts = df[col].value_counts().reset_index()
        value_counts_topN = list(value_counts[0:top_n_values_to_keep]["index"])
        df[col + "_collapsed"] = df.apply(
            lambda r: str.strip(str.upper(str(r[col])))
            if r[col] in value_counts_topN
            else other_label,
            axis=1,
        )

        print(value_counts_topN)

    return df


def main():
    """ Transform routines routine"""


if __name__ == "__main__":
    main()
