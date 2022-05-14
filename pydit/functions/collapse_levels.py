"""Implementation of the `collapse_levels` function."""
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def collapse_levels(df: pd.DataFrame, sep: str = "_") -> pd.DataFrame:
    """Flatten multi-level column dataframe to a single level.

    This method mutates the original DataFrame.

    Given a DataFrame containing multi-level columns, flatten to single-level
    by string-joining the column labels in each level.

    After a `groupby` / `aggregate` operation where `.agg()` is passed a
    list of multiple aggregation functions, a multi-level DataFrame is
    returned with the name of the function applied in the second level.

    It is sometimes convenient for later indexing to flatten out this
    multi-level configuration back into a single level. This function does
    this through a simple string-joining of all the names across different
    levels in a single column.

    Args:

    :param df: A pandas DataFrame.
    :param sep: String separator used to join the column level names.
    :returns: A pandas DataFrame with single-level column index.
    """  # noqa: E501
    if not isinstance(sep, str):
        logger.debug("Invalid separator provider, defaulting to underscore")
        sep = "_"
    # if already single-level, just return the DataFrame
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    df.columns = [
        sep.join(str(el) for el in tup if str(el) != "") for tup in df  # noqa: PD011
    ]

    return df
