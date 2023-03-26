"""Example of using pydit"""

# %%
import sys
import os
import pandas as pd
from pandas import Timestamp


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pydit

logger = pydit.setup_logging()
logger.info("Started")

# %%

fm = pydit.FileManager.getInstance()
fm.input_path = "./demo_data/"
fm.output_path = "./demo_output"
fm.temp_path = "./demo_data"
fm.max_rows_to_excel = 10000

df = pd.DataFrame(
    [
        [1, "INV-220001", Timestamp("2022-01-01 00:00:00"), "OPEN", 35.94, ""],
        [2, "INV-220002", Timestamp("2022-01-02 00:00:00"), "OPEN", 99.99, "-5"],
        [
            3,
            "INV-220003",
            Timestamp("2022-01-03 00:00:00"),
            "CANCELLED",
            13.0,
            "reinbursed 10.5",
        ],
        [4, "INV-220003", Timestamp("2022-01-04 00:00:00"), "OPEN", float("nan"), ""],
        [5, "INV-220005", Timestamp("2022-01-04 00:00:00"), "OPEN", 204.2, ""],
        [6, "INV-220006", Timestamp("2022-01-15 00:00:00"), "OPEN", -4.2, "discount"],
        [7, float("nan"), Timestamp("2022-01-06 00:00:00"), float("nan"), 0.0, ""],
        [8, "INV-220007", Timestamp("2022-01-15 00:00:00"), "PENDING", 50.4, ""],
        [9, "", pd.NaT, "ERROR", 0.0, ""],
        [10, "INV-220007", Timestamp("2022-01-15 00:00:00"), "PENDING", 50.4, ""],
    ],
    columns=["id", "ref", "date_trans", "status", "amount", "notes"],
)

# %%

col1 = range(1, 100)
col2 = [1] * 30 + [2] * 50 + [3] * 20
col3 = [1] * 10 + [2] * 90
df = pd.DataFrame(zip(col1, col2, col3), columns=["col1", "col2", "col3"])
df

for i, r in df.iterrows():
    print(i, r)


# %%

print(pydit.add_percentile(df, "col1", ["col2", "col3"]))

print(pydit.add_percentile(df, "col1"))


# %%
