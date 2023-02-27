import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import map_values
import numpy as np
import pandas as pd


def test_check_map_values_advanced_cases():
    """testing with a mix of nas and various oddities"""
    d = {
        "col1": [1, 2, 3, np.nan, 0],
        "col2": ["red", "amber", "green", np.nan, "blue"],
    }
    df = pd.DataFrame(data=d)

    res = map_values(
        df,
        input_column="col1",
        mapping="to_red_amber_green",
        output_column="col_output",
        na_action="ignore",
    )
    print(
        res["col_output"].equals(pd.Series(["red", "amber", "green", np.nan, np.nan]))
    )

    res = map_values(
        df,
        input_column="col2",
        mapping="red_amber_green",
        output_column="col_output",
        na_action="ignore",
    )
    assert res["col_output"].equals(pd.Series([1, 2, 3, np.nan, np.nan])) == True


test_check_map_values_advanced_cases()
