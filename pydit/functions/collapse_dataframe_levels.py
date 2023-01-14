"""Implementation of the `collapse_levels` function."""
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def collapse_levels(obj: pd.DataFrame, sep: str = "_") -> pd.DataFrame:
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

    Parameters
    ----------
    obj : pandas.DataFrame
        The DataFrame to flatten.
    sep : str, optional, default "_"
        The separator to use when joining the column names.

    Returns
    -------
    pandas.DataFrame
        A pandas DataFrame with single-level column index

    """
    # noqa: E501
    if not isinstance(obj, pd.DataFrame):
        raise TypeError("obj must be a pandas DataFrame")
    if not isinstance(sep, str):
        raise TypeError("Invalid separator provided. Must be a string.")
    # if already single-level, just return the DataFrame
    if not isinstance(obj.columns, pd.MultiIndex):
        return obj.copy()
    # otherwise, flatten the multi-level index

    df = obj.copy()
    df.columns = [
        sep.join(str(el) for el in tup if str(el) != "") for tup in df  # noqa: PD011
    ]
    return df
