import pandas as pd
import numpy as np
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

# pylint: disable=bare-except


def lookup_values(
    df, key, df_ref, key_ref, return_column, flatten_list=True, fillna=None, dropna=True
):
    """
    Lookup values from a reference dataframe and return values from a column
    If the key is a list, it will return a list of values

    Use case: the equivalent to a xlookup in MS Excel, but supporting multiple keys.
    It is useful for Airtables where external references come as lists of one element
    or even can have multiple values in the cell/field.
    It is also more flexible than using pandas.merge as it deals with duplicates in the
    reference table and NaNs, without creating a cartesian product.
    (it will return the first value found). It will warn about this case, but will not fail.




    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to lookup values from
    key : str
        Column name of the key to lookup
    df_ref : pandas.DataFrame
        External Reference Dataframe to lookup values
    key_ref : str
        Column name of the key to lookup
    return_column : str
        Column name of the value to return
    flatten_list : bool, optional
        If True, it will return a string with the values separated by a comma.
        The default is True.
    fillna : str or int, optional
        If not None, it will replace the NaN values with the value provided.
        The default is None.
    dropna: bool, optional
        If True, it will ignore the NaN values when looking up multiple keys.
            Only if none of the keys are found, it will return NaN.
        If False, it will bring every single NaN value to the result.
        The default is True.
    Returns
    -------
    res_series : pandas.Series
        Series with the values looked up


    """

    if not isinstance(df_ref, pd.DataFrame):
        raise TypeError("df_ref must be a pandas.DataFrame")
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if not isinstance(key_ref, str):
        raise TypeError("key_ref must be a string")
    if not isinstance(return_column, str):
        raise TypeError("return_column must be a string")
    if return_column not in df_ref.columns:
        raise ValueError("return_column must be a column in df_ref")
    if key_ref not in df_ref.columns:
        raise ValueError("key_ref must be a column in df_ref")
    if key not in df.columns:
        raise ValueError("key must be a column in df")

    def aux_lookup(keys):
        res_list = []
        if isinstance(keys, (int, str, float, date, datetime)):
            keys = [keys]
        if isinstance(keys, (list, tuple)):
            for element in keys:
                try:
                    res = df_ref.loc[df_ref[key_ref] == element, return_column].values
                    if len(res) > 1:
                        logger.warning(
                            "Multiple results found in reference table for key %s, taking the first one",
                            element,
                        )
                    res_list.append(res[0])

                except IndexError:
                    if not dropna:
                        res_list.append(np.nan)
            if not res_list:
                res_list = [np.nan]

        else:
            res_list = [np.nan]

        if fillna is not None:
            res_list = [fillna if pd.isna(e) else e for e in res_list]

        if flatten_list:
            res_list = ", ".join([str(e) for e in res_list])

        return res_list

    res_series = df[key].apply(aux_lookup)

    return res_series


if __name__ == "__main__":
    pass
