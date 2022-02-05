from pydit import pydit_core
import pandas as pd
from pandas import Timestamp
import logging

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
    handlers=[

        RotatingFileHandler("audit.log", maxBytes=50000, backupCount=5),

        logging.StreamHandler(),

    ]   
)


logging.info("Started")
tools = pydit_core.Tools()
tools.input_path = "./demo_data/"
tools.output_path = "./demo_data"
tools.temp_path = "./demo_data"
tools.max_rows_to_excel = 10000
conf = tools.config()

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
res = tools.check_duplicates(df, ["ref"], keep=False)
print(res)

