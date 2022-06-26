"""Module to merge dataframes

"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def merge_force_suffix(left, right, **kwargs):
    """Merge two dataframes, forcing the suffix of the left dataframe to the right dataframe.

    This is useful when merging two dataframes with the same column names,
    to ensure all columns are tagged with suffixes, even if they don't have
    collissions. This is particularly important when merging many dataframes,
    to keep track of columns.
    The normal behaviour of merge would add suffixes just on collission.
    There is a feature in pandas to .add_suffix() to all columns but that
    also renames the key columns and you need to do it before merging.
    This function does not add suffixes to the key columns.


    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe
    right : pandas.DataFrame
        The right dataframe
    kwargs : the keyword arguments to pass to pandas.DataFrame.merge()

    Note: left_on and right_on are not supported by this function.

    Returns
    -------
    pandas.DataFrame
        A new merged dataframe



    """
    left_on = []
    right_on = []

    try:
        on_col = kwargs["on"]
    except Exception:
        on_col = []
        try:
            left_on = kwargs["left_on"]
            right_on = kwargs["right_on"]
        except Exception:
            pass

    left_cols = [*on_col, *left_on]
    right_cols = [*on_col, *right_on]

    suffix_tuple = kwargs["suffixes"]

    def _left_suffix_col(col, suffix):
        if col not in left_cols:
            return str(col) + suffix
        else:
            return col

    def _right_suffix_col(col, suffix):
        if col not in right_cols:
            return str(col) + suffix
        else:
            return col

    left_suffixed = left.rename(columns=lambda x: _left_suffix_col(x, suffix_tuple[0]))
    right_suffixed = right.rename(
        columns=lambda x: _right_suffix_col(x, suffix_tuple[1])
    )
    del kwargs["suffixes"]
    return pd.merge(left_suffixed, right_suffixed, **kwargs)
