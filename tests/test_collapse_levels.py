""" test the collapse_levels function brought from pyjanitor"""
import os
import sys
import pandas as pd


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import collapse_levels


def test_collapse_levels():
    """ test function"""
    df = pd.DataFrame(
        {
            "class": ["bird", "bird", "bird", "mammal", "mammal"],
            "max_speed": [389, 389, 24, 80, 21],
            "type": ["falcon", "falcon", "parrot", "Lion", "Monkey"],
        }
    )
    grouped_df = df.groupby("class").agg(["mean", "median"])
    collapse_levels(grouped_df, sep="_")
    assert list(grouped_df.columns) == ["max_speed_mean", "max_speed_median"]


if __name__ == "__main__":
    # execute only if run as a script
    test_collapse_levels()
