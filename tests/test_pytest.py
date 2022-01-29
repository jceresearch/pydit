""" pytest version of tests - WIP"""
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import pydit_core

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pandas import Timestamp


tools = pydit_core.Tools()


def test_init():
    """ testing the initiatlisation and setup"""
    assert tools.input_path == "."
