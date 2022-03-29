import logging

import pandas as pd


logger = logging.getLogger(__name__)


def check_duplicates(df, columns=None, keep=False, ascending=None):
    """
    Duplicate analysis
    Args:
        df (DataFrame): pandas dataframe

        columns (str or list, optional): column or list of column(s) to check
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
    if isinstance(columns, str):
        if columns in df.columns:
            cols=[columns]
        return
    else:
        if isinstance(columns,list):
            cols = columns
        else:
            cols = df.columns

    fields = ",".join(cols)
    df_duplicates = df[df.duplicated(subset=cols, keep=keep)]
    
    logger.info("Duplicates in fields: %s", fields)
    if len(df_duplicates) == 0:
        logger.info("No duplicates found")
        return None
    else:
        logger.info("(keep=%s)", keep)
        logger.info("%s of population %s", len(df_duplicates), len(df))
        if ascending is True:
            # Ascending
            df_ret = df_duplicates.sort_values(cols, ascending=True)
        elif ascending is False:
            # Descending
            df_ret = df_duplicates.sort_values(cols, ascending=False)
        else:
            # No sort
            df_ret = df_duplicates
    return df_ret
