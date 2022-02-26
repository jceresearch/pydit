""" Transform and Munging functions"""

import logging


import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime

logger = logging.getLogger(__name__)


def coalesce_values(
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
