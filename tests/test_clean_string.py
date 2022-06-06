""" test of base functions"""
import os
import sys

import numpy as np


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import setup_logging, clean_string


# import numpy as np
# from datetime import datetime, date, timedelta
# from pandas import Timestamp

logger = setup_logging()


def test_clean_string():
    """test the clean string function"""
    assert clean_string(" John Smith 123  456 .  ") == "john_smith_123_456"

    assert (
        clean_string(" John Smith 123  456 .  ", space_to_underscore=False)
        == "john smith 123 456"
    )

    assert clean_string("") == ""
    assert clean_string(np.nan) == ""
    assert clean_string(None) == ""
    assert clean_string(123) == "123"
    assert clean_string() == ""


if __name__ == "__main__":
    # test_clean_string
    pass
