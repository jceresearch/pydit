"""test suite"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pandas import Timestamp


from pydit import pydit_core

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
            "reinburse 10.5",
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


class Test01(unittest.TestCase):
    """ Test cases for the internal functions"""

    def setUp(self):
        """ Standard method for setting up the tests """
        self.tools = pydit_core.Tools()

    def test_deduplicate_list(self):
        """test the intermal function to cleanup dataframe column names"""
        # pylint: disable=protected-access
        self.assertEqual(
            self.tools._deduplicate_list(["A", "B", "B"]), ["A", "B", "B_2"]
        )

        self.assertEqual(self.tools._deduplicate_list([]), [])
        self.assertEqual(self.tools._deduplicate_list([1, 2, 2]), ["1", "2", "2_2"])

    def test_clean_string(self):
        """test the clean string function"""
        self.assertEqual(
            self.tools.clean_string(" John Smith 123  456 .  "), "john_smith_123_456"
        )
        self.assertEqual(
            self.tools.clean_string(
                " John Smith 123  456 .  ", space_to_underscore=False
            ),
            "john smith 123 456",
        )

    def test_check_dataframe(self):
        """test the function for checking/profiling a dataframe"""

        # test that passing one column will fail gracefully
        self.assertEqual(self.tools.check_dataframe(df["id"]), None)


if __name__ == "__main__":
    unittest.main()
