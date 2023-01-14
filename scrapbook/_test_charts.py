""" test of charts"""
import os
import sys
import numpy as np
import pandas as pd

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import chart_bar, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

logger = setup_logging()


if __name__ == "__main__":
    df = pd.DataFrame(np.random.randn(1000, 4), columns=list("ABCD"))
    # print(df.head())
    # chart_bar(df, "Test", "A", "B")
