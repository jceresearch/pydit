""" Scrap module to prototype tests"""
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
import numpy as np

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pydit


os.chdir(Path(__file__).resolve().parent)

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    handlers=[
        RotatingFileHandler("audit.log", maxBytes=50000, backupCount=5),
        logging.StreamHandler(),
    ],
)


logging.info("Started")
fm = pydit.filemanager.FileManager.getInstance()

fm.input_path = "./input"
fm.output_path = "./output"

d = {
    "col1": [1, 2, 3, 4, 5],
    "col2": ["Value 1", "Value 2", "", " ", "Value 5"],
    "col3": [np.nan, 2.0, 0.0, 4.0, 5.1],
    "col4": [np.nan, 2, 0, 4, 5],
    "col5": [np.nan, "    ", "  \t", "   \n", "Value 5"],
}
df = pd.DataFrame(data=d)
# tools.save(df, "test.xlsx")
# print(tools.output_path)

pydit.print_red("Alert")

print(pydit.profile_dataframe(df))

s = pd.Series([1, 2, 3, 4, 5])
s.to_excel("./output/test_saving_series.xlsx")
