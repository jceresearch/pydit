""" Validation functions"""

import logging
from datetime import timedelta
from collections import Counter

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_string_dtype, is_numeric_dtype
from pandas import Series, DataFrame
import numpy as np


logger = logging.getLogger(__name__)


def check_duplicates(df, columns=None, keep=False, ascending=None):
    """
    Duplicate analysis
    Args:
        df (DataFrame): pandas dataframe
        
        columns (list, optional): column(s) to check between square brackets,
        even if it is one column only, if multiple columns provided
        the check is combined duplicates, exactly as pandas duplicated().

        keep ('first','last' or False, optional): Argument for pandas df.duplicated() method.
        Defaults to 'first'.

        ascending (True, False or None, optional): Argument for DataFrame.value_counts()
        Defaults to None.

    Returns:
        DataFrame or None: Returns the DataFrame with the duplicates.
        If no duplicates, returns None.
    """

    if not isinstance(df, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        # TODO: #17 Add support for Series in the duplicate check
        return
    if not isinstance(columns, list):
        logger.error("Expecting a list, even a list of one element")
        return
    else:
        if not columns:
            cols = df.columns
        else:
            cols = columns

    fields = ",".join(cols)
    df_duplicates = df[df.duplicated(subset=cols, keep=keep)]
    print(
        "Duplicates in",
        fields,
        "(keep=",
        keep,
        "):",
        len(df_duplicates),
        " of population: ",
        len(df),
    )
    if len(df_duplicates) == 0:
        return None
    else:
        if ascending is True:
            print("Ascending")
            df_ret = df_duplicates.sort_values(cols, ascending=True)
        elif ascending is False:
            print("Descending")
            df_ret = df_duplicates.sort_values(cols, ascending=False)
        else:
            print("No sort")
            df_ret = df_duplicates

    return df_ret


def check_sequence(obj_in, col=""):
    """ to check the numerical sequence of a series including dates
    and numbers within an text ID """
    if col:
        obj = obj_in[col]
    else:
        if isinstance(obj_in, Series):
            obj = obj_in.copy()
        elif isinstance(obj_in, DataFrame):
            obj = obj_in.iloc[:, 0].copy()
        elif isinstance(obj_in, list):
            obj = pd.Series(obj_in)
        else:
            logging.error("Type not recognised")
            return None
    typ = obj.dtype
    if "int" in str(typ):
        unique = set([i for i in obj[pd.notna(obj)]])
        fullrng = set(range(min(unique), max(unique) + 1))
        diff = fullrng.difference(unique)
        if diff:
            print("Missing in sequence: ", list(diff)[0:10])
            return list(diff)
        else:
            print("Full sequence")
            return []
    elif is_datetime(obj):
        unique = set([i.date() for i in obj[pd.notna(obj)]])
        fullrng = set(
            pd.date_range(
                min(unique), max(unique) - timedelta(days=1), freq="d"
            ).to_list()
        )
        diff = fullrng.difference(unique)
        if diff:
            print(
                len(diff),
                " missing, first ",
                min(len(diff), 10),
                ":",
                list(diff)[0:10],
            )
            working_days = [wd for wd in diff if wd.weekday() < 5]
            print(
                len(working_days),
                " missing working days",
                min(len(diff), 10),
                ":",
                list(diff)[0:10],
            )

            return list(diff)
        else:
            print("Full sequence")
            return []
    elif typ == "object":
        values = obj[pd.notna(obj)]
        numeric_chars = values.str.replace(r"[^0-9^-^.]+", "", regex=True)
        numeric_chars_no_blank = numeric_chars[numeric_chars.str.len() > 0]
        numeric = pd.to_numeric(
            numeric_chars_no_blank, errors="coerce", downcast="integer"
        )
        if pd.api.types.is_float_dtype(numeric):
            # we have floats so it wont likely be a sequence
            print("Contains floats, no sequence to check")
        else:
            unique = set(numeric)
            print(list(unique))
            if unique:
                fullrng = set(range(min(unique), max(unique)))
                diff = fullrng.difference(unique)
                if diff:
                    print(
                        len(diff), " missing in sequence, fist 10:", list(diff)[0:10],
                    )
                    return list(diff)
                else:
                    print("Full sequence")
                    return []
            else:
                print("No sequence to check")
                return None
    return


def check_blanks(
    df_in, columns=None, zeroes=True, null_strings_and_spaces=True, totals_only=False,
):
    """ Reports on blanks in the Dataframe and optionally saves to an excel file

    Args:
        df_in ([type]): [description]
        columns ([type], optional): [description]. Defaults to None.
        zeroes (bool, optional): [description]. Defaults to True.
        null_strings_and_spaces (bool, optional): [description]. Defaults to True.
        totals_only (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """

    if not isinstance(df_in, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        return
    df = df_in.copy()
    if columns and isinstance(columns, list):
        cols = columns
    elif not columns:
        cols = df.columns
    else:
        logger.error("Expecting a list, even a list of one element")
        return

    fields = ",".join(cols)
    logger.info("Checking for blanks in %s", fields)
    total_results = []
    for c in cols:
        if is_numeric_dtype(df[c]) and zeroes:
            df[c + "_blanks"] = (pd.isna(df[c])) | (df[c] == 0)
        elif is_string_dtype(df[c]) and null_strings_and_spaces:
            logger.debug("Checking for spaces and nullstring too in %s", c)
            df[c + "_blanks"] = (pd.isna(df[c])) | (df[c].str.strip() == "")
        else:
            logger.debug("Checking just for NaN or NaT in %s", c)
            df[c + "_blanks"] = pd.isna(df[c])
        total_results.append(df[c + "_blanks"].sum())
    new_cols = [c + "_blanks" for c in cols]
    df["has_blanks"] = np.any(df[new_cols], axis=1)

    print("Total blanks found in each columns:", total_results)

    if totals_only:
        return total_results

    return df


def add_counts_in_each_row(df1, df2, left_on=None, right_on=None, on=None):
    """Add a count column that will bring the count of that key in the
    other table.

    Args:
        df1 (DataFrame): Pandas DataFrame
        df2 (DataFrame): Pandas DataFrame
        left_on (str, optional): Name of the column to use as key for df1. Defaults to None.
        right_on (str, optional): Name of the column to use as key for df2. Defaults to None.
        on (str, optional): Name of the column to use as key for df1 and df2 if they are the same. Defaults to None.
    Either on is needed, or left_on and right_on have to provide a value

    Returns:
        True: if sucessfull
        The calling DataFrames will have a new column 
        with the count of records (0 if not found). 
        In df1 it will be "count_[key2]" and in df2 it will be "count_[key1]"

    """
    if on:
        left_on = on
        right_on = on
    if (not left_on) or (not right_on):
        print("Missing key")
        return None
    # df1["count"]= df1['mkey'].map(df2.groupby('mkey')['mkey'].count())
    # df2["count"]= df2['mkey'].map(df1.groupby('mkey')['mkey'].count())
    df1["count_" + right_on] = df1["mkey"].map(df2[right_on].value_counts())
    df2["count_" + left_on] = df2["mkey"].map(df1[left_on].value_counts())
    df1["count_" + right_on] = df1["count_" + left_on].fillna(0).astype("Int64")
    df2["count_" + left_on] = df2["count_" + right_on].fillna(0).astype("Int64")
    # TODO: #22 Add_counts_in_each_row: add option for not overwriting the column but creating a new one
    # TODO: #23 Add_counts_in_each_row: add more checks for when not providing a DataFrame or no records

    return True


def check_referential_integrity(a1, a2, verbose=False):
    """Check what relationship two hashable arrays/lists have ("one to one",
    "many to many" etc.)
    Optionally, explains in a verbose way that relationship

    Args:
        a1 (List or Array): Anything that can be iterated and converted to set
        a2 (List or Array): Same as a1
        verbose (bool, optional): Provide extra explanation. Defaults to False.
    """

    def explain(*args, verbose=verbose):
        """' Prints/logs these messages if verbose is True"""
        if verbose:
            print(*args)

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
            return "1-to-1"
        elif not key1_is_unique and not key2_is_unique:
            explain(expl, "Many-to-many, all values in both, but both have duplicates")
            return "n-to-n"
        elif key1_is_unique and not key2_is_unique:
            explain(
                expl,
                "One-to-many, all values in both,\
                key2 is facts (has duplicates)\
                , key1 is the dimension/master table",
            )
            return "1-to-n"
        elif key2_is_unique and not key1_is_unique:
            explain(
                expl,
                "Many-to-one, all values in both, \
                key1 is facts (has duplicates),\
                key2 is dimension/master table",
            )
            return "n-to-1"
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
                    return "*-to-1"
                else:  # key2 has duplicates, so it is likely a fact table
                    if key1_is_unique:
                        explain(
                            expl,
                            "key1 is possible dimension (no duplicates) but misses values in key2",
                        )
                        return "1-to-* - need fix incomplete key1"
                    else:
                        explain(
                            expl,
                            "key1 and key2 have duplicates, key1 is likely facts as is subset of key2",
                        )
                        return "*-to-1 - need fix duplicate keys in key2"
            if set2_in_set1:
                if key1_is_unique:
                    explain(
                        expl,
                        "One-to-Many, key1 is dimension, no duplicates but has values not in key2",
                    )
                    return "1-to-*"
                else:
                    if key2_is_unique:
                        explain(
                            expl,
                            "key2 is possible dimension (no duplicates) but misses values in key1",
                        )
                        return "*-to-1 - need fix incomplete key2"
                    else:
                        explain(
                            expl,
                            "key1 and key2 have duplicates, key2 is likely facts as is subset of key1",
                        )
                        return "1-to-* - need fix duplicate keys in key1"
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


def main():
    """ Validation functions"""


if __name__ == "__main__":
    main()
