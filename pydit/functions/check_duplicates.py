import logging

import pandas as pd


logger = logging.getLogger(__name__)


def check_duplicates(df, columns=None, keep=False, ascending=None):
    """
    Duplicate analysis
    Args:
        df (DataFrame): pandas dataframe
        
        columns (list, optional): column(s) to check between square brackets,
        even if it is one column only, if multiple columns provided
        the check is combined duplicates, exactly as pandas duplicated().

        keep ('first','last' or False, optional): Argument for pandas df.duplicated() method.
        Defaults to 'first'.

        ascending (True, False or None, optional): Argument for DataFrame.value_counts()
        Defaults to None.

    Returns:
        DataFrame or None: Returns the DataFrame with the duplicates.
        If no duplicates, returns None.
    """

    if not isinstance(df, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        # TODO: #17 Add support for Series in the duplicate check
        return
    if not isinstance(columns, list):
        logger.error("Expecting a list, even a list of one element")
        return
    else:
        if not columns:
            cols = df.columns
        else:
            cols = columns

    fields = ",".join(cols)
    df_duplicates = df[df.duplicated(subset=cols, keep=keep)]
    print(
        "Duplicates in",
        fields,
        "(keep=",
        keep,
        "):",
        len(df_duplicates),
        " of population: ",
        len(df),
    )
    if len(df_duplicates) == 0:
        return None
    else:
        if ascending is True:
            print("Ascending")
            df_ret = df_duplicates.sort_values(cols, ascending=True)
        elif ascending is False:
            print("Descending")
            df_ret = df_duplicates.sort_values(cols, ascending=False)
        else:
            print("No sort")
            df_ret = df_duplicates

    return df_ret

