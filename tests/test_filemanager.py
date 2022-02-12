""" test of base functions"""

#%%

import os
import sys
import logging


import numpy as np
import pandas as pd


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pydit


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp


logger = logging.getLogger()
pydit.setup_logging(logger)
logger.info("Started")

fm = pydit.filemanager.FileManager().getInstance()


def test_stem_name():
    """ test the internal function to find the stemp of a filename"""
    assert fm._stem_name("Test.xlsx") == "test"
    assert fm._stem_name(r"c:\test\test.xlsx") == "test"
    assert fm._stem_name(r".\Test.xls") == "test"


def test_save():
    d = {
        "col1": [1, 2, 3, 5, 6],
        "col2": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data=d)
    s1 = pd.Series((1, 2, 3, 4))
    s2 = df[df.col1 == 10]["col1"]
    df1 = df[df["col1"] == 10]
    t1 = ""
    l1 = []
    d1 = {}
    assert fm.save(s2, "test_zero_len.xlsx") == False
    assert fm.save(df1, "test_zero_len.xlsx") == False
    assert fm.save(t1, "test_zero_len.pickle") == False
    assert fm.save(l1, "test_zero_len.pickle") == False
    assert fm.save(s1, "test_nonzero_len.xlsx") == True
    assert fm.save(d1, "test_zero_len.xlsx") == False
    assert fm.save(df, "test_zero_len.xlsx") == True
    return


#%%

test_save()

# %%

# %%

# %%
fm.output_path
# %%
