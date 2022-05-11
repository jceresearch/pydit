"""Function for performing coalesce."""
import logging
from typing import Optional, Union

import pandas as pd

logger = logging.getLogger(__name__)


def _check_types(varname: str, value, expected_types: list):
    """
    Function for checking types.
    It can also check callables.

    Example usage:

    ```python
    check('x', x, [int, float])
    ```

    :param varname: The name of the variable (for diagnostic error message).
    :param value: The value of the `varname`.
    :param expected_types: The type(s) the item is expected to be.
    :raises TypeError: if data is not the expected type.
    """
    is_expected_type: bool = False
    for t in expected_types:
        if t is callable:
            is_expected_type = t(value)
        else:
            is_expected_type = isinstance(value, t)
        if is_expected_type:
            break

    if not is_expected_type:
        raise TypeError(
            "{varname} should be one of {expected_types}".format(
                varname=varname, expected_types=expected_types
            )
        )


def coalesce_columns(
    df: pd.DataFrame,
    *column_names,
    target_column_name: Optional[str] = None,
    default_value: Optional[Union[int, float, str]] = None,
) -> pd.DataFrame:
    """Coalesce two or more columns of data in order of column names provided.

    Given the list of column names, `coalesce` finds and returns the first
    non-missing value from these columns, for every row in the input dataframe.
    If all the column values are null for a particular row, then the
    `default_value` will be filled in.

    This method does not mutate the original DataFrame.
    """

    if not column_names:
        return df

    if len(column_names) < 2:
        raise ValueError("The number of columns to coalesce should be a minimum of 2.")

    if isinstance(column_names, list) or isinstance(column_names, tuple):
        wrong_columns = [x for x in column_names if x not in df.columns]
        if wrong_columns:
            raise ValueError("Columns not in the dataframe:" + " ".join(wrong_columns))

    else:
        raise TypeError("Please provide a list of columns")

    if target_column_name:
        _check_types("target_column_name", target_column_name, [str])

    if default_value:
        _check_types("default_value", default_value, [int, float, str])

    if target_column_name is None:
        target_column_name = column_names[0]

    # bfill/ffill combo is faster than combine_first
    outcome = (
        df.filter(column_names).bfill(axis="columns").ffill(axis="columns").iloc[:, 0]
    )
    if outcome.hasnans and (default_value is not None):
        outcome = outcome.fillna(default_value)
    # TODO: #24 coalesce_columns() add options for summing values, concatenate strings, or maybe max or other operation.

    # Using assign creates a new dataframe.
    return df.assign(**{target_column_name: outcome})
