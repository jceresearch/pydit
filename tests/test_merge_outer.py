""" pytest version of tests"""

import os
import sys
import numpy as np
import pandas as pd


# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import merge_outer_and_split, setup_logging

logger = setup_logging()


def test_merge_outer():
    dffact = pd.DataFrame(
        {
            "KEY": ["K0", "K1", "K2", "K3", "K4", np.nan, "K6"],
            "B": ["B0", "B0", "B2", "B3", "B3", "B5", "B6"],
            "C": ["C0", "C0", "C2", "C3", "C4", "C5", "C6"],
            "D": ["D0", "D0", "D2", "D3", "D3", "D5", "D6"],
            "DKEY": ["A0", "A0", "A2", "A3", "A3", "A3", np.nan],
            "V": ["V1", "V1", "V1", "V1", "V2", "V1", "V1"],
        },
        index=[0, 1, 2, 3, 4, 5, 6],
    )
    dfdim = pd.DataFrame(
        {
            "DKEY": ["A0", "A1", "A2", "A4", "A4", np.nan],
            "E": ["E0", "E1", "E2", "E4", "E4", "E5"],
            "F": ["F0", "F1", "F2", "F4", "F4", "F5"],
            "G": ["G0", "G1", "G2", "G4", "G4", "G5"],
        },
        index=[0, 1, 2, 3, 4, 5],
    )

    res_tuple = merge_outer_and_split(
        dffact, dfdim.drop_duplicates(subset="DKEY"), left_on="DKEY", right_on="DKEY"
    )

    assert res_tuple[0].shape[0] == 3
    assert res_tuple[1].shape[0] == 3
    assert res_tuple[2].shape[0] == 2
    assert res_tuple[3].shape[0] == 1
    assert res_tuple[4].shape[0] == 1
