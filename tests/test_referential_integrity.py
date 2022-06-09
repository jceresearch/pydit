""" pytest version of tests - WIP"""
import os
import sys

import numpy as np
import pandas as pd

# import numpy as np
# from datetime import datetime, date, timedelta
# pylint: disable=import-error disable=wrong-import-position
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydit import check_referential_integrity as check
from pydit import setup_logging


logger = setup_logging()


def test_check_referential_integrity():
    """ test for the referencial integrity checker"""
    A = [10, 20, 30, 40, 50]
    Ax = [10, 10, 20, 30, 40, 50]
    B = [10, 20, 30, 40, 50, 60, 70]
    Bx = [10, 10, 20, 30, 40, 50, 60, 60, 60, 60]
    By = [10, 20, 30, 40, 50, 50, 60, 60, 70, 70]
    C = [10, 20, 30, 40, 50]
    Cx = [10, 10, 30, 20, 40, 50]
    D = [100, 200, 300, 400, 500]
    Dx = [100, 200, 300, 400, 400, 500, 500]
    E = [10, 20, 60, 70, 80, 90]
    Ex = [10, 20, 60, 60, 70, 80, 90, 90, 90]

    assert check(A, C) == "1:1"
    assert check(C, A) == "1:1"
    assert check(A, B) == "*:1"
    assert check(B, A) == "1:*"
    assert check(B, By) == "1:m"
    assert check(A, Cx) == "1:m"
    assert check(By, B) == "m:1"
    assert check(Ax, Ax) == "m:m"
    assert check(Ax, Bx) == "*:1 - need fix duplicate keys in key2"
    assert check(Bx, Ax) == "1:* - need fix duplicate keys in key1"
    assert check(A, Bx) == "1:* - need fix incomplete key1"
    assert check(Bx, A) == "*:1 - need fix incomplete key2"
    assert check(A, E) == "partial overlap and no duplicates in either"
    assert check(A, Ex) == "partial overlap and key2 has duplicates"
    assert check(Ex, A) == "partial overlap and key1 has duplicates"
    assert check(Ex, Ax) == "partial overlap and both have duplicates"
    assert check(A, D) == "disjoint - no duplicates"
    assert check(D, A) == "disjoint - no duplicates"
    assert check(A, Dx) == "disjoint - duplicates in key2"
    assert check(Dx, A) == "disjoint - duplicates in key1"
    assert check(Dx, Ax) == "disjoint - both have duplicates"
    assert check(Ax, Dx) == "disjoint - both have duplicates"
    assert check(D, Dx) == "1:m"


def test_check_referential_integrity_load():
    """ Load test for referential integrity checker
    now the arrays are generated dynamically based on n
    the number of elements from the initial A array
    
    """
    n = 10000
    n80 = int(n * 0.8)
    n50 = int(n * 0.5)
    n20 = int(n * 0.2)
    n150 = int(n * 1.5)
    n200 = int(n * 2)
    A = list(range(1, int(n)))
    B = list(range(1, n200))
    Ax = A + A
    Bx = list(range(n20, n150)) + B
    By = B + B
    C = list(range(1, int(n)))
    Cx = C + C[n20:n80]
    D = list(range(n + 1, n200))
    Dx = D + D[1:n50] + D[n50:n80]
    E = list(range(n80, n)) + list(range(n150, n200))
    Ex = E + list(range(n150, n200))
    assert check(A, C) == "1:1"
    assert check(C, A) == "1:1"
    assert check(A, B) == "*:1"
    assert check(B, A) == "1:*"
    assert check(B, By) == "1:m"
    assert check(A, Cx) == "1:m"
    assert check(By, B) == "m:1"
    assert check(Ax, Ax) == "m:m"
    assert check(Ax, Bx) == "*:1 - need fix duplicate keys in key2"
    assert check(Bx, Ax) == "1:* - need fix duplicate keys in key1"
    assert check(A, Bx) == "1:* - need fix incomplete key1"
    assert check(Bx, A) == "*:1 - need fix incomplete key2"
    assert check(A, E) == "partial overlap and no duplicates in either"
    assert check(A, Ex) == "partial overlap and key2 has duplicates"
    assert check(Ex, A) == "partial overlap and key1 has duplicates"
    assert check(Ex, Ax) == "partial overlap and both have duplicates"
    assert check(A, D) == "disjoint - no duplicates"
    assert check(D, A) == "disjoint - no duplicates"
    assert check(A, Dx) == "disjoint - duplicates in key2"
    assert check(Dx, A) == "disjoint - duplicates in key1"
    assert check(Dx, Ax) == "disjoint - both have duplicates"
    assert check(Ax, Dx) == "disjoint - both have duplicates"
    assert check(D, Dx) == "1:m"

