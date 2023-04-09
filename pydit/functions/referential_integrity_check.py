"""Module to perform referential integrity checks on two dataframes.

The purpose of these tools is to quickly ascertain what kind of relationship exists
between two dataframe, e.g. many to many, one to many, one to one, etc.
This is useful in an audit scenario as oftentimes the data is not clean and we
may have missing detail records or blanks or duplicates. 

Currently this module only supports providing a list or series of keys to check.

"""

import logging
from collections import Counter

import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)


def check_referential_integrity(a1, a2, verbose=False):
    """Check what relationship two hashable list have ("one to one",
    "many to many" etc.)
    Optionally, explains in a verbose way that relationship

    Parameters
    ----------
    a1 : list or pandas.Series
        First list to check
    a2 : list or pandas.Series
        Second list to check
    verbose : bool, optional, default False
        If True, prints a verbose explanation of the relationship.

    Returns
    -------
    str
        A string describing the relationship.

    """

    def explain(*args, verbose=verbose):
        """' Prints/logs these messages if verbose is True"""
        if verbose:
            text = " ".join(args)
            logger.info(text)

    expl = ""
    key1_nans = np.count_nonzero(pd.isna(a1))
    key2_nans = np.count_nonzero(pd.isna(a2))
    if key1_nans > 0:
        expl = expl + "Key1 has " + str(key1_nans) + " nan/None values\n"

    if any(pd.isna(a2)):
        expl = expl + "Key2 has " + str(key2_nans) + " nan/None values\n"

    set1 = set(a1)
    key1_is_unique = len(set1) == len(a1)
    set2 = set(a2)
    key2_is_unique = len(set2) == len(a2)
    two_sets_equal = set1 == set2
    if two_sets_equal:
        # key1 and key2 unique values are the same"
        if key1_is_unique and key2_is_unique:
            explain(expl, "One-to-one, key1 and key2 match")
            return "1:1"
        elif not key1_is_unique and not key2_is_unique:
            explain(expl, "Many-to-many, all values in both, but both have duplicates")
            return "m:m"
        elif key1_is_unique and not key2_is_unique:
            explain(
                expl,
                "One-to-many, all values in both,\
                key2 is facts (has duplicates)\
                , key1 is the dimension/master table",
            )
            return "1:m"
        elif key2_is_unique and not key1_is_unique:
            explain(
                expl,
                "Many-to-one, all values in both, \
                key1 is facts (has duplicates),\
                key2 is dimension/master table",
            )
            return "m:1"
    else:  # two sets are not equal, we need to find out how so
        intersection = set1.intersection(set2)
        if len(intersection) == 0:  # Disjoint sets, no commonalities
            if key1_is_unique:
                if key2_is_unique:
                    explain(expl, "No common values, and both have no duplicates")
                    return "disjoint - no duplicates"
                else:
                    explain(
                        expl,
                        "No common values, key1 has no duplicates, key2 has duplicates",
                    )
                    return "disjoint - duplicates in key2"
            else:
                if key2_is_unique:
                    explain(
                        expl,
                        "No common values, key2 has no duplicate values, key1 has duplicates",
                    )
                    return "disjoint - duplicates in key1"
                else:
                    explain(
                        expl, "No common values, both have duplicates also in the data"
                    )
                    return "disjoint - both have duplicates"
        else:  # intersection is not null, so there are some common elements
            set1_in_set2 = set1.issubset(set2)
            set2_in_set1 = set2.issubset(set1)
            count1 = Counter(a1)
            count2 = Counter(a2)
            if set1_in_set2:
                if key2_is_unique:
                    explain(
                        expl,
                        "Many-to-one, key2 is dimension (no duplicates) but has values not in key1",
                    )
                    return "*:1"
                else:  # key2 has duplicates, so it is likely a fact table
                    if key1_is_unique:
                        explain(
                            expl,
                            "key1 is possible dimension (no duplicates) but misses values in key2",
                        )
                        return "1:* - need fix incomplete key1"
                    else:
                        explain(
                            expl,
                            "key1 and key2 have duplicates, key1 is likely facts as is subset of key2",
                        )
                        return "*:1 - need fix duplicate keys in key2"
            if set2_in_set1:
                if key1_is_unique:
                    explain(
                        expl,
                        "One-to-Many, key1 is dimension, no duplicates but has values not in key2",
                    )
                    return "1:*"
                else:
                    if key2_is_unique:
                        explain(
                            expl,
                            "key2 is possible dimension (no duplicates) but misses values in key1",
                        )
                        return "*:1 - need fix incomplete key2"
                    else:
                        explain(
                            expl,
                            "key1 and key2 have duplicates, key2 is likely facts as is subset of key1",
                        )
                        return "1:* - need fix duplicate keys in key1"
            explain("Both key1 and key2 have values not shared between them")
            set1diffset2 = set1 - set2
            set2diffset1 = set2 - set1
            if key1_is_unique:
                if key2_is_unique:
                    explain(
                        expl,
                        "Both have no duplicates values.\nThey share",
                        len(intersection),
                        " unique values.\nKey1 has ",
                        len(set1diffset2),
                        " unique values non shared.\nKey2 has ",
                        len(set2diffset1),
                        " unique values non shared",
                    )
                    return "partial overlap and no duplicates in either"
                else:
                    key2_all_non_shared = [x for x in a2 if x in set2diffset1]
                    key2_all_non_shared_dup = [
                        x for x in a2 if ((count2[x] > 1) and (x in set2diffset1))
                    ]
                    explain(
                        expl,
                        "Key1 has unique values but key2 has duplicates.\nThey share",
                        len(intersection),
                        " unique values.\nKey1 has ",
                        len(set1diffset2),
                        " unique values non shared.\nKey2 has ",
                        len(set2diffset1),
                        " unique values non shared.\nKey2 has ",
                        len(key2_all_non_shared),
                        " elements non shared.\nKey2 has ",
                        len(key2_all_non_shared_dup),
                        " elements duplicated and non shared",
                    )

                    return "partial overlap and key2 has duplicates"

            else:
                if key2_is_unique:
                    key1_all_non_shared = [x for x in a1 if x in set1diffset2]
                    key1_all_non_shared_dup = [
                        x for x in a1 if ((count1[x] > 1) and (x in set1diffset2))
                    ]
                    explain(
                        expl,
                        "Key2 has unique values but key1 has duplicates.\nThey share",
                        len(intersection),
                        " unique values.\nKey1 has ",
                        len(set1diffset2),
                        " unique values non shared.\nKey2 has ",
                        len(set2diffset1),
                        " unique values non shared.\nKey1 has ",
                        len(key1_all_non_shared),
                        " elements non shared.\nKey1 has ",
                        len(key1_all_non_shared_dup),
                        " elements duplicated and non shared",
                    )

                    return "partial overlap and key1 has duplicates"
                else:
                    explain(
                        expl,
                        "Both have duplicates and values non shared with each other",
                    )

                    return "partial overlap and both have duplicates"
