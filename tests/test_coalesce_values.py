""" Test module for coalesce_columns"""
import os
import sys

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal


# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import coalesce_values
