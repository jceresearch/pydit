"""Module to map/add various values like 1, 2, 3 to "High", "Medium", "Low"."""


import logging

import pandas as pd

logger = logging.getLogger(__name__)


def map_values(
    df: pd.DataFrame,
    column: str,
    mapping: str,
    mapping_dict: dict,
    inplace: bool = False,
    na_action: str = None,
    nan_value: int = 0,
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
            - "yes_no"
            - "true_false"
            - "positive_negative"
            - "positive_neutral_negative"
            - "red_yellow_green"
            - "red_yellow_green_blue"
            - "red_amber_green"
            - "red_amber_green_blue"

            adding _r will do a reverse mapping
    mapping_dict : dict
        A dictionary to use for manual translation/coalescing.
    inplace : bool, optional, default False
        Whether to modify the original dataframe or return a copy.
    na_action: str, optional, default None
        How to handle missing values. Options are:
            - None: ignore missing values
            -
    nan_value : str, optional, default 0

    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(column, str):
        raise TypeError("column must be a string")  
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in DataFrame")
    
    MAPPINGS={
        "red_yellow_green": {1: "red", 2: "yellow", 3: "green"},
        "red_yellow_green_r": {1: "green", 2: "yellow", 3: "red"},
        "red_yellow_green_blue": {1: "red", 2: "yellow", 3: "green", 4: "blue"},
        "red_yellow_green_blue_r": {1: "blue", 2: "green", 3: "yellow", 4: "red"},
        "to_red_yellow_green":{"red":1,"yellow":2,"green":1},
    }
    
    if na_action=="ignore":
        df[column]=df[column].map(MAPPINGS[mapping],na_action='ignore')
    

    return
