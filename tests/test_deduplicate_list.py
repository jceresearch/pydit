""" test of base functions"""
import os
import sys

# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import deduplicate_list, setup_logging


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

log = setup_logging()
log.info("Started")


def test_deduplicate_list():
    """test the intermal function to cleanup dataframe column names"""
    assert deduplicate_list(["A", "B", "B"]) == ["A", "B", "B_2"]
    assert deduplicate_list([]) == []
    assert deduplicate_list([1, 2, 2]) == ["1", "2", "2_2"]


if __name__ == "__main__":
    test_deduplicate_list
    log.info("Tests Finished")
