"""test suite"""
import unittest


from pydit import pydit_core


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


if __name__ == "__main__":
    unittest.main()
