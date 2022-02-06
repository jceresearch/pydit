""" Scrap module to prototype tests"""
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import file_tools, profiling_tools

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
tools = file_tools.FileTools()
profile = profiling_tools.ProfilingTools()

tools.input_path = "./input"
tools.output_path = "./output"

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


print(profile.profile_dataframe(df))
tools.print_red("Alert")
