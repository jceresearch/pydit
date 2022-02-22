""" test of base functions"""
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import common


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

logger = common.setup_logging()
logger.info("Started")


def test_deduplicate_list():
    """test the intermal function to cleanup dataframe column names"""
    assert common.deduplicate_list(["A", "B", "B"]) == ["A", "B", "B_2"]
    assert common.deduplicate_list([]) == []
    assert common.deduplicate_list([1, 2, 2]) == ["1", "2", "2_2"]


def test_clean_string():
    """test the clean string function"""
    assert common.clean_string(" John Smith 123  456 .  ") == "john_smith_123_456"

    assert (
        common.clean_string(" John Smith 123  456 .  ", space_to_underscore=False)
        == "john smith 123 456"
    )


if __name__ == "__main__":
    pass
