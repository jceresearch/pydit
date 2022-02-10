"""' Demo of the use of these libraries"""

#%%

import logging
from logging.handlers import RotatingFileHandler


import pandas as pd
from pandas import Timestamp

from pydit import common


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = RotatingFileHandler("audit.log", maxBytes=50000, backupCount=5)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


logger.info("Started")

# %%
import pydit

config = pydit.common.Singleton.getInstance()
config.input_path = ".."

#%%
config.input_path = "test"


# %%

tools = common.CommonTools()
tools.input_path = "./demo_data/"
tools.output_path = "./demo_data"
tools.temp_path = "./demo_data"
tools.max_rows_to_excel = 10000

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


from pydit import profiling

col1 = range(1, 100)
col2 = [1] * 30 + [2] * 50 + [3] * 20
col3 = [1] * 10 + [2] * 90


df = pd.DataFrame(zip(col1, col2, col3), columns=["col1", "col2", "col3"])
print(profiling.add_percentile(df, "col1", ["col2", "col3"]))

print(profiling.add_percentile(df, "col1"))

