""" Transform and Munging functions"""

import logging
from datetime import datetime

from pandas.api.types import is_datetime64_any_dtype as is_datetime
from .common import CommonTools

logger = logging.getLogger(__name__)

tools = CommonTools()


def clean_columns_names(df):
    """ Cleanup the column names of a Pandas dataframe
        e.g. removes non alphanumeric chars, _ instead of space, perc instead
        of %, strips trailing spaces, converts to lowercase
        """
    df.columns = df.columns.str.replace(r"%", "perc", regex=True)
    df.columns = df.columns.str.replace(r"[^a-zA-Z0-9]", " ", regex=True)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" +", "_", regex=True)
    df.columns = df.columns.str.lower()
    # TODO: #20 Implement some truncation in the clean_columns_name functionif the field is too long TBC how long

    if len(df.columns) != len(set(df.columns)):
        print("Identified some duplicate columns, renaming them")
        new_cols = tools._deduplicate_list(list(df.columns))
        df.columns = new_cols
    if len(df.columns) != len(set(df.columns)):
        raise ValueError("Duplicated column names remain!!! check what happened")
    return True


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


def main():
    """ Transform routines routine"""


if __name__ == "__main__":
    main()
