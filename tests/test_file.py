""" test of convenience functions"""
import os
import sys

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import file_tools

import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp
import logging

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
)
logging.info("Started")

tools = file_tools.FileTools()


def test_init():
    """ testing the initiatlisation and setup"""
    assert tools.input_path == "./"
    tools.input_path = "./input"
    assert tools.input_path == "./input/"


def test_stem_name():
    """ test the internal function to find the stemp of a filename"""
    assert tools._stem_name("Test.xlsx") == "test"
    assert tools._stem_name(r"c:\test\test.xlsx") == "test"
    assert tools._stem_name(r".\Test.xls") == "test"


if __name__ == "__main__":
    pass
