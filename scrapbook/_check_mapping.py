import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import map_values
import numpy as np
import pandas as pd

d = {
    "col1": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, np.nan],
    "col2": [
        "red",
        "amber",
        "green",
        "blue",
        np.nan,
        0,
        "Amber",
        "AMBER",
        "amber",
        "amber",
        "amber",
    ],
    "col3": [
        "high",
        "medium",
        "low",
        "medium",
        "medium",
        "medium",
        "medium",
        "medium",
        "medium",
        "medium",
        "medium",
    ],
    "col4": [
        "red",
        "red",
        "red",
        "red",
        "red",
        "red",
        "red",
        "red",
        "red",
        "red",
        "red",
    ],
}
df = pd.DataFrame(data=d)
res = map_values(
    df,
    input_column="col4",
    mapping="red_amber_green",
    output_column="col_output",
    na_action="ignore",
)
print(res["col_output"].to_list())
res = map_values(
    df,
    input_column="col1",
    mapping="to_red_amber_green",
    output_column="col_output",
    na_action="ignore",
)
assert np.array_equal(
    res["col_output"].to_array(), res["col_output"].to_array(), equal_nan=True
)
