"""Module to map/add various values like 1, 2, 3 to "High", "Medium", "Low"."""


import logging

import pandas as pd

logger = logging.getLogger(__name__)


def map_values(
    df: pd.DataFrame,
    column: str,
    mapping: str,
    inplace: bool = False,
    na_action=None,
    case: str = "lower",
):
    """Map common values to more descriptive values or values that are
    easier to sort/present/filter on.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to map values on
    column : str
        The column to map values on
    mapping : str
        One of the following pre defined mappings:
            - "high_medium_low"
            - "red_yellow_green"
            - "red_yellow_green_blue"
            - "red_amber_green"
            - "red_amber_yellow_green"

            suffixing _r will do a reverse the order of numeric mapping
            e.g. "high_medium_low_r" will map to 3, 2, 1
            e.g. "red_yellow_green_r" will map to 3, 2, 1

            prefixing to_ will do a mapping to the value
            e.g. "to_high_medium_low" will map 1, 2, 3 to "high", "medium", "low"
            e.g. "to_high_medium_low_r" will map 1, 2, 3 to "low", "medium", "high"

    inplace : bool, optional, default False
        Whether to modify the original dataframe or return a copy.
    na_action: str, optional, default None
        Parameter to pass to the pandas map function. See pandas documentation
    case : str, optional, default "lower"
        The output case to use for the mapping.
        One of "lower", "upper", "title", "capitalize"
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in DataFrame")
    if inplace is False:
        df = df.copy()

    MAPPINGS = {
        "red_yellow_green": {1: "red", 2: "yellow", 3: "green"},
        "red_yellow_green_r": {1: "green", 2: "yellow", 3: "red"},
        "to_red_yellow_green": {"red": 1, "yellow": 2, "green": 1},
        "to_red_yellow_green_r": {"red": 3, "yellow": 2, "green": 1},
        "red_yellow_green_blue": {1: "red", 2: "yellow", 3: "green", 4: "blue"},
        "red_yellow_green_blue_r": {1: "blue", 2: "green", 3: "yellow", 4: "red"},
        "to_red_yellow_green_blue": {"red": 1, "yellow": 2, "green": 3, "blue": 4},
        "to_red_yellow_green_blue_r": {"red": 4, "yellow": 3, "green": 2, "blue": 1},
        "red_amber_yellow_green": {1: "red", 2: "amber", 3: "yellow", 4: "green"},
        "red_amber_yellow_green_r": {1: "green", 2: "yellow", 3: "amber", 4: "red"},
        "to_red_amber_yellow_green": {"red": 1, "amber": 2, "yellow": 3, "green": 4},
        "to_red_amber_yellow_green_r": {"red": 4, "amber": 3, "yellow": 2, "green": 1},
        "high_medium_low": {1: "high", 2: "medium", 3: "low"},
        "high_medium_low_r": {1: "low", 2: "medium", 3: "high"},
        "to_high_medium_low": {"high": 1, "medium": 2, "low": 3},
        "to_high_medium_low_r": {"high": 3, "medium": 2, "low": 1},
    }
    TARGET = MAPPINGS[mapping]
    if case != "lower" and mapping[0:3] != "to_":
        if case == "upper":
            newDict = {k: v.upper() for k, v in TARGET.items()}
        elif case == "title":
            newDict = {k: v.title() for k, v in TARGET.items()}
        elif case == "capitalize":
            newDict = {k: v.capitalize() for k, v in TARGET.items()}
        else:
            raise ValueError(
                f"case must be one of 'lower', 'upper', 'title', 'capitalize'"
            )
        TARGET = newDict
    if mapping[0:3] == "to_":
        df[column] = df[column].str.lower.map(TARGET, na_action=na_action)
    else:
        df[column] = df[column].map(TARGET, na_action=na_action)
    if inplace is False:
        return df
    return None
